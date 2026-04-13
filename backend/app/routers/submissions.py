"""
Submissions router — POST /submissions
Accepts code, performs basic static analysis, returns categorised feedback.
"""
import difflib
import re
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends

from app.data import SUBMISSIONS, EXERCISES
from app.models import SubmitRequest, SubmissionResult, SubmissionHistory, DiffLine
from app.routers.deps import get_current_user

router = APIRouter(prefix="/submissions", tags=["submissions"])


def _build_diff(submitted: str, solution: str) -> list[DiffLine]:
    """Return a structured line-by-line diff of submitted vs solution."""
    sub_lines = submitted.splitlines()
    sol_lines = solution.splitlines()
    diff: list[DiffLine] = []
    matcher = difflib.SequenceMatcher(None, sol_lines, sub_lines, autojunk=False)
    sol_line_no = 1
    sub_line_no = 1
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for line in sol_lines[i1:i2]:
                diff.append(DiffLine(type="equal", line_no_left=sol_line_no, line_no_right=sub_line_no, content=line))
                sol_line_no += 1
                sub_line_no += 1
        elif tag == "replace":
            for line in sol_lines[i1:i2]:
                diff.append(DiffLine(type="replace_old", line_no_left=sol_line_no, content=line))
                sol_line_no += 1
            for line in sub_lines[j1:j2]:
                diff.append(DiffLine(type="replace_new", line_no_right=sub_line_no, content=line))
                sub_line_no += 1
        elif tag == "delete":
            for line in sol_lines[i1:i2]:
                diff.append(DiffLine(type="delete", line_no_left=sol_line_no, content=line))
                sol_line_no += 1
        elif tag == "insert":
            for line in sub_lines[j1:j2]:
                diff.append(DiffLine(type="insert", line_no_right=sub_line_no, content=line))
                sub_line_no += 1
    return diff


def _compute_grade(submitted: str, solution: str, status: str) -> tuple[int, str]:
    """Return (0-100 similarity score, letter grade) based on diff vs. solution and submission status."""
    # No reference solution — fall back to binary pass/fail
    if not solution.strip():
        pct = 100 if status == "correct" else 0
        return pct, ("A+" if pct == 100 else "F")

    def _normalize(code: str) -> list[str]:
        """Strip blank lines and line comments for a fairer structural comparison."""
        out = []
        for line in code.splitlines():
            s = line.strip()
            if s and not s.startswith("//") and not s.startswith("*") and not s.startswith("/*"):
                out.append(s)
        return out

    ratio = difflib.SequenceMatcher(
        None, _normalize(solution), _normalize(submitted), autojunk=False
    ).ratio()
    sim_pct = round(ratio * 100)

    # Status caps — even a near-perfect copy can't earn top marks if it doesn't compile/run correctly
    STATUS_CAPS: dict[str, int] = {
        "compiler_error": 44,  # ≤ F ceiling
        "runtime_error":  64,  # ≤ D ceiling
        "wrong_output":   79,  # ≤ B- ceiling
        "correct":       100,
    }
    final_pct = min(sim_pct, STATUS_CAPS.get(status, 100))

    # Standard +/- letter scale
    if final_pct == 100: grade = "A+"
    elif final_pct >= 95: grade = "A"
    elif final_pct >= 90: grade = "A-"
    elif final_pct >= 87: grade = "B+"
    elif final_pct >= 83: grade = "B"
    elif final_pct >= 80: grade = "B-"
    elif final_pct >= 77: grade = "C+"
    elif final_pct >= 73: grade = "C"
    elif final_pct >= 70: grade = "C-"
    elif final_pct >= 67: grade = "D+"
    elif final_pct >= 60: grade = "D"
    elif final_pct >= 50: grade = "D-"
    else:                  grade = "F"

    return final_pct, grade


def _analyze(code: str, exercise_id: str) -> SubmissionResult:
    sid = str(uuid.uuid4())[:8]
    ex = EXERCISES.get(exercise_id)
    solution_code = ex.get("solution_code", "") if ex else ""
    course_id = ex.get("course_id", "") if ex else ""

    def _result(**kwargs) -> SubmissionResult:
        status = kwargs.get("status", "")
        diff = _build_diff(code, solution_code) if solution_code else []
        score, grade = _compute_grade(code, solution_code, status)
        # Strip any hardcoded score — always computed from similarity
        kwargs.pop("score", None)
        return SubmissionResult(
            solution_code=solution_code,
            course_id=course_id,
            diff=diff,
            score=score,
            grade=grade,
            **kwargs,
        )

    # Empty submission
    if not code.strip():
        return _result(
            submission_id=sid, exercise_id=exercise_id,
            status="compiler_error",
            message="Compilation failed: no code was submitted.",
            compiler_output="error: empty submission — no code was provided.",
            your_code=code, score=0,
        )

    compiler_issues: list[str] = []

    # Unmatched braces
    opens  = code.count("{")
    closes = code.count("}")
    if opens != closes:
        compiler_issues.append(
            f"error: reached end of file while parsing\n"
            f"{code.strip()[:60]}\n^\n{abs(opens - closes)} error(s)"
        )

    # Missing semicolons (heuristic — first offending statement only)
    if not compiler_issues:
        for i, line in enumerate(code.strip().splitlines(), 1):
            s = line.strip()
            if (
                s
                and not s.startswith("//")
                and not s.startswith("/*")
                and not s.endswith("{")
                and not s.endswith("}")
                and not s.endswith(";")
                and not s.startswith("@")
                and not s.startswith("import")
                and not s.startswith("package")
                and re.search(r"\w", s)
                and re.match(r"^(int|double|String|boolean|char|float|long|return|System)\b", s)
            ):
                compiler_issues.append(
                    f"{exercise_id}.java:{i}: error: ';' expected\n{s}\n^\n1 error"
                )
                break

    if compiler_issues:
        return _result(
            submission_id=sid, exercise_id=exercise_id,
            status="compiler_error",
            message="Compilation failed: code has syntax errors.",
            compiler_output="\n".join(compiler_issues),
            your_code=code, score=0,
        )

    # Runtime error patterns
    for pattern, msg in [
        (r"\.get\(\s*\d+\s*\)", "IndexOutOfBoundsException — check list size before access"),
        (r"\[\s*\d+\s*\]",      "ArrayIndexOutOfBoundsException — check array length"),
    ]:
        if re.search(pattern, code):
            return _result(
                submission_id=sid, exercise_id=exercise_id,
                status="runtime_error",
                message=f"Runtime error: {msg}",
                compiler_output=f"Exception in thread \"main\" java.lang.{msg}",
                your_code=code, score=0,
            )

    # Correctness check
    if ex and ex.get("sample_runs"):
        expected = ex["sample_runs"][0]["output"]
        has_main  = "public static void main" in code
        has_print = "System.out.print" in code or "println" in code
        if has_main and has_print:
            return _result(
                submission_id=sid, exercise_id=exercise_id,
                status="correct",
                message="All tests passed!",
                compiler_output="",
                your_code=code, score=100,
            )
        return _result(
            submission_id=sid, exercise_id=exercise_id,
            status="wrong_output",
            message="Your output did not match the expected output.",
            compiler_output=f"Expected: {expected}\nActual:   (no output — missing print statement)",
            your_code=code, score=0,
        )

    # Default: accepted
    return _result(
        submission_id=sid, exercise_id=exercise_id,
        status="correct",
        message="Submission accepted.",
        compiler_output="",
        your_code=code, score=100,
    )


@router.post("", response_model=SubmissionResult)
def submit_code(body: SubmitRequest, current_user: dict = Depends(get_current_user)):
    result = _analyze(body.code, body.exercise_id)
    SUBMISSIONS.append({
        "submission_id": result.submission_id,
        "user_id": current_user["id"],
        "exercise_id": body.exercise_id,
        "code": body.code,
        "status": result.status,
        "score": result.score,
        "grade": result.grade,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    })
    return result


@router.get("/history/{exercise_id}", response_model=list[SubmissionHistory])
def get_history(exercise_id: str, current_user: dict = Depends(get_current_user)):
    return [
        SubmissionHistory(
            submission_id=s["submission_id"],
            exercise_id=s["exercise_id"],
            status=s["status"],
            score=s.get("score", 0),
            grade=s.get("grade", ""),
            submitted_at=s["submitted_at"],
            code=s["code"],
        )
        for s in SUBMISSIONS
        if s["user_id"] == current_user["id"] and s["exercise_id"] == exercise_id
    ]


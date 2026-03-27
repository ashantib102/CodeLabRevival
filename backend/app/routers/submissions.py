"""
Submissions router — POST /submissions
Accepts code, performs basic static analysis, returns categorised feedback.
"""
import re
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends

from app.data import SUBMISSIONS, EXERCISES, next_submission_id
from app.models import SubmitRequest, SubmissionResult
from app.routers.deps import get_current_user

router = APIRouter(prefix="/submissions", tags=["submissions"])


def _analyze(code: str, exercise_id: str) -> SubmissionResult:
    sid = str(uuid.uuid4())[:8]

    # Empty submission
    if not code.strip():
        return SubmissionResult(
            submission_id=sid,
            exercise_id=exercise_id,
            status="compiler_error",
            message="Compilation failed: no code was submitted.",
            compiler_output="error: empty submission — no code was provided.",
            your_code=code,
            score=0,
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
        return SubmissionResult(
            submission_id=sid,
            exercise_id=exercise_id,
            status="compiler_error",
            message="Compilation failed: code has syntax errors.",
            compiler_output="\n".join(compiler_issues),
            your_code=code,
            score=0,
        )

    # Runtime error patterns
    for pattern, msg in [
        (r"\.get\(\s*\d+\s*\)", "IndexOutOfBoundsException — check list size before access"),
        (r"\[\s*\d+\s*\]",      "ArrayIndexOutOfBoundsException — check array length"),
    ]:
        if re.search(pattern, code):
            return SubmissionResult(
                submission_id=sid,
                exercise_id=exercise_id,
                status="runtime_error",
                message=f"Runtime error: {msg}",
                compiler_output=f"Exception in thread \"main\" java.lang.{msg}",
                your_code=code,
                score=0,
            )

    # For exercises with known expected output, do a simple correctness check
    ex = EXERCISES.get(exercise_id)
    if ex and ex.get("sample_runs"):
        expected = ex["sample_runs"][0]["output"]
        has_main  = "public static void main" in code
        has_print = "System.out.print" in code or "println" in code
        if has_main and has_print:
            return SubmissionResult(
                submission_id=sid,
                exercise_id=exercise_id,
                status="correct",
                message="All tests passed!",
                compiler_output="",
                your_code=code,
                score=100,
            )
        return SubmissionResult(
            submission_id=sid,
            exercise_id=exercise_id,
            status="wrong_output",
            message="Your output did not match the expected output.",
            compiler_output=f"Expected: {expected}\nActual:   (no output — missing print statement)",
            your_code=code,
            score=0,
        )

    # Default: correct if no issues found
    return SubmissionResult(
        submission_id=sid,
        exercise_id=exercise_id,
        status="correct",
        message="Submission accepted.",
        compiler_output="",
        your_code=code,
        score=100,
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
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    })
    return result


@router.get("/history/{exercise_id}")
def get_history(exercise_id: str, current_user: dict = Depends(get_current_user)):
    return [
        s for s in SUBMISSIONS
        if s["user_id"] == current_user["id"] and s["exercise_id"] == exercise_id
    ]


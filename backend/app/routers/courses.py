"""
Courses router — GET /courses
Returns semesters + courses filtered by the authenticated user's role:
  - instructor : sees the main course (59094) + their own sections
  - student    : sees only their enrolled courses
"""
from fastapi import APIRouter, Depends

from app.data import SEMESTERS, USERS
from app.models import CoursesResponse, Semester, Course, EnrollRequest
from app.routers.deps import get_current_user

router = APIRouter(prefix="/courses", tags=["courses"])

# The main/aggregate course that every instructor can always see
MAIN_COURSE_ID = "59094"


def _build_response(user: dict) -> CoursesResponse:
    role = user["role"]
    enrolled: set[str] = set()

    if role == "student":
        enrolled = set(user.get("enrolled_courses", []))
    elif role == "instructor":
        instructor_key = user.get("instructor_key", "")
        # instructors see: the main course + any course where they are the instructor
        for sem in SEMESTERS:
            for c in sem["courses"]:
                if c["course_id"] == MAIN_COURSE_ID or c["instructor"] == instructor_key:
                    enrolled.add(c["course_id"])

    semesters = []
    total = 0
    for sem in SEMESTERS:
        courses = [Course(**c) for c in sem["courses"] if c["course_id"] in enrolled]
        if courses:
            semesters.append(Semester(term=sem["term"], courses=courses))
            total += len(courses)

    return CoursesResponse(role=role, total=total, semesters=semesters)


@router.get("", response_model=CoursesResponse)
def list_courses(current_user: dict = Depends(get_current_user)):
    return _build_response(current_user)


@router.post("/enroll")
def enroll_in_course(request: EnrollRequest, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "student":
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Only students can self-enroll")

    # Find course by access code
    target_course = None
    for sem in SEMESTERS:
        for course in sem["courses"]:
            if course["access_code"] == request.access_code:
                target_course = course
                break
        if target_course:
            break

    if not target_course:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Invalid access code")

    course_id = target_course["course_id"]
    enrolled_courses = current_user.get("enrolled_courses", [])

    if course_id in enrolled_courses:
        from fastapi import HTTPException
        raise HTTPException(status_code=409, detail="Already enrolled in this course")

    enrolled_courses.append(course_id)
    current_user["enrolled_courses"] = enrolled_courses

    return {"message": f"Successfully enrolled in {target_course['title']} (Section {target_course['section']})"}

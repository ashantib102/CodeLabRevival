"""
Courses router — GET /courses
Returns all semesters + courses for the authenticated user.
"""
from fastapi import APIRouter, Depends

from app.data import SEMESTERS
from app.models import CoursesResponse, Semester, Course
from app.routers.deps import get_current_user

router = APIRouter(prefix="/courses", tags=["courses"])


def _build_response(user: dict) -> CoursesResponse:
    semesters = []
    total = 0
    for sem in SEMESTERS:
        courses = []
        for c in sem["courses"]:
            courses.append(Course(**c))
            total += 1
        semesters.append(Semester(term=sem["term"], courses=courses))
    return CoursesResponse(role=user["role"], total=total, semesters=semesters)


@router.get("", response_model=CoursesResponse)
def list_courses(current_user: dict = Depends(get_current_user)):
    return _build_response(current_user)

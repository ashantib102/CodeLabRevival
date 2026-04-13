"""
Exercises router
  GET  /labs/{course_id}/structure  — lab TOC (auth required; students must be enrolled)
  GET  /exercises/{exercise_id}     — single exercise (public)
  POST /exercises                   — create exercise (instructor only)
"""
from fastapi import APIRouter, Depends, HTTPException, status

from app.data import LAB_STRUCTURES, EXERCISES, next_exercise_id, add_exercise_to_course
from app.models import LabStructure, Exercise, TopicNode, ExerciseRef, CreateExerciseRequest
from app.routers.deps import get_current_user

MAIN_COURSE_ID = "59094"

router = APIRouter(tags=["exercises"])


def _build_topic(t: dict) -> TopicNode:
    return TopicNode(
        id=t["id"],
        label=t["label"],
        children=[_build_topic(c) for c in t.get("children", [])],
        exercises=[ExerciseRef(**e) for e in t.get("exercises", [])],
    )


@router.get("/labs/{course_id}/structure", response_model=LabStructure)
def get_lab_structure(course_id: str, current_user: dict = Depends(get_current_user)):
    # Access check: students must be enrolled; instructors must own or it must be main
    if current_user["role"] == "student":
        enrolled = set(current_user.get("enrolled_courses", []))
        if course_id not in enrolled:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not enrolled in this course.",
            )
    elif current_user["role"] == "instructor":
        instructor_key = current_user.get("instructor_key", "")
        # Must be main course or one they teach
        from app.data import SEMESTERS
        owned = {
            c["course_id"]
            for sem in SEMESTERS
            for c in sem["courses"]
            if c["course_id"] == MAIN_COURSE_ID or c["instructor"] == instructor_key
        }
        if course_id not in owned:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this course.",
            )

    lab = LAB_STRUCTURES.get(course_id)
    if not lab:
        raise HTTPException(status_code=404, detail=f"Lab not found for course {course_id}")
    tree = [_build_topic(t) for t in lab["tree"]]
    return LabStructure(course_id=lab["course_id"], title=lab["title"], tree=tree)


@router.get("/exercises/{exercise_id}", response_model=Exercise)
def get_exercise(exercise_id: str):
    ex = EXERCISES.get(exercise_id)
    if not ex:
        raise HTTPException(status_code=404, detail=f"Exercise {exercise_id} not found")
    return Exercise(**ex)


@router.post("/exercises", response_model=Exercise, status_code=status.HTTP_201_CREATED)
def create_exercise(body: CreateExerciseRequest, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "instructor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors can create exercises.",
        )

    # Resolve the instructor's primary course (first course they own, not main)
    from app.data import SEMESTERS
    instructor_key = current_user.get("instructor_key", "")
    instructor_course_id = next(
        (
            c["course_id"]
            for sem in SEMESTERS
            for c in sem["courses"]
            if c["instructor"] == instructor_key and c["course_id"] != MAIN_COURSE_ID
        ),
        MAIN_COURSE_ID,
    )

    new_id = next_exercise_id()
    new_exercise = {
        "id": new_id,
        "title": body.title,
        "instructions": body.instructions,
        "sample_runs": [sr.model_dump() for sr in body.sample_runs],
        "starter_code": body.starter_code,
        "course_id": instructor_course_id,
        "topic": body.topic,
        "instructor_key": instructor_key,
    }
    EXERCISES[new_id] = new_exercise

    # Add to the instructor's own course TOC and to the main aggregate course
    add_exercise_to_course(instructor_course_id, new_id, body.title)
    if instructor_course_id != MAIN_COURSE_ID:
        add_exercise_to_course(MAIN_COURSE_ID, new_id, body.title)

    return Exercise(**new_exercise)

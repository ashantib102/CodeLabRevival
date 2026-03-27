"""
Exercises router — GET /labs/{course_id}/structure, GET /exercises/{exercise_id}
"""
from fastapi import APIRouter, HTTPException

from app.data import LAB_STRUCTURES, EXERCISES
from app.models import LabStructure, Exercise, TopicNode, ExerciseRef

router = APIRouter(tags=["exercises"])


def _build_topic(t: dict) -> TopicNode:
    return TopicNode(
        id=t["id"],
        label=t["label"],
        children=[_build_topic(c) for c in t.get("children", [])],
        exercises=[ExerciseRef(**e) for e in t.get("exercises", [])],
    )


@router.get("/labs/{course_id}/structure", response_model=LabStructure)
def get_lab_structure(course_id: str):
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

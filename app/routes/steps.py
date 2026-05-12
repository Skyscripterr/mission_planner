from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import session_factory
from app.models import Mission, MissionStep
from app.schemas import MissionStepCreate, MissionStepResponse
from app.algorithms.topological_sort import topological_sort, CircularDependencyError

router = APIRouter(prefix="/missions", tags=["Mission Steps"])

def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()

@router.post("/{mission_id}/steps", response_model=MissionStepResponse)
def add_mission_step(mission_id: int, step: MissionStepCreate, db: Session = Depends(get_db)):
    """Add a new step to a specific mission, optionally with prerequisites."""
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    new_step = MissionStep(
        mission_id=mission.id,
        name=step.name,
        command=step.command,
        latitude=step.latitude,
        longitude=step.longitude,
        altitude=step.altitude
    )
    
    # Add prerequisites if any exist
    if step.prerequisite_ids:
        prereqs = db.query(MissionStep).filter(MissionStep.id.in_(step.prerequisite_ids)).all()
        if len(prereqs) != len(step.prerequisite_ids):
            raise HTTPException(status_code=400, detail="One or more prerequisite IDs are invalid.")
        new_step.prerequisites.extend(prereqs)

    db.add(new_step)
    db.commit()
    db.refresh(new_step)
    
    # Return the response with prerequisite_ids populated manually to match the schema
    return MissionStepResponse(
        id=new_step.id,
        mission_id=new_step.mission_id,
        name=new_step.name,
        command=new_step.command,
        latitude=new_step.latitude,
        longitude=new_step.longitude,
        altitude=new_step.altitude,
        prerequisite_ids=[p.id for p in new_step.prerequisites]
    )

@router.get("/{mission_id}/steps/validate", response_model=List[int])
def validate_mission_steps(mission_id: int, db: Session = Depends(get_db)):
    """
    Validates that the mission's steps have no circular dependencies, 
    and returns the execution order!
    """
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    # Get all steps for this mission
    steps = db.query(MissionStep).filter(MissionStep.mission_id == mission_id).all()
    if not steps:
        return []

    # Build the data structures for our Topological Sort
    vertices = [step.id for step in steps]
    edges = []
    for step in steps:
        for prereq in step.prerequisites:
            # prerequisite must happen BEFORE this step
            edges.append((prereq.id, step.id))
            
    try:
        # Validate dependency graph for cycles and determine execution order
        sorted_order = topological_sort(vertices, edges)
        return sorted_order
    except CircularDependencyError as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import session_factory
from app.models import AirspaceRestriction
from app.schemas import AirspaceRestrictionCreate, AirspaceRestrictionResponse, ScheduleMissionRequest
from app.algorithms.interval_tree import IntervalTree

router = APIRouter(prefix="/airspace", tags=["Airspace Restrictions"])

def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AirspaceRestrictionResponse)
def create_restriction(restriction: AirspaceRestrictionCreate, db: Session = Depends(get_db)):
    """Create a new time window where drones are NOT allowed to fly."""
    if restriction.end_time <= restriction.start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")
        
    new_restriction = AirspaceRestriction(
        name=restriction.name,
        start_time=restriction.start_time,
        end_time=restriction.end_time
    )
    db.add(new_restriction)
    db.commit()
    db.refresh(new_restriction)
    return new_restriction

@router.post("/check")
def check_airspace(schedule: ScheduleMissionRequest, db: Session = Depends(get_db)):
    """
    Check if a proposed mission time window conflicts with any airspace restrictions.
    """
    restrictions = db.query(AirspaceRestriction).all()
    
    # 1. Build the Interval Tree
    tree = IntervalTree()
    for r in restrictions:
        tree.insert(r.start_time, r.end_time, r.id)
        
    # Query the interval tree for overlaps in O(log N)
    conflict_id = tree.find_overlap(schedule.start_time, schedule.end_time)
    
    if conflict_id:
        conflict = db.query(AirspaceRestriction).filter(AirspaceRestriction.id == conflict_id).first()
        raise HTTPException(
            status_code=400, 
            detail=f"Airspace Conflict! The time window overlaps with restriction: '{conflict.name}'"
        )
        
    return {"message": "Airspace is clear! You are good to schedule the mission."}

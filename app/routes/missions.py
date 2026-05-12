from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import session_factory
from app.models import Mission
from app.schemas import MissionCreate, MissionResponse

router = APIRouter()


# --- Database Dependency ---
def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


# --- Create a Mission ---
@router.post("/missions", response_model=MissionResponse)
def create_mission(mission: MissionCreate, db: Session = Depends(get_db)):
    new_mission = Mission(name=mission.name, description=mission.description)
    db.add(new_mission)
    db.commit()
    db.refresh(new_mission)
    return new_mission


# --- List All Missions ---
@router.get("/missions", response_model=list[MissionResponse])
def list_missions(db: Session = Depends(get_db)):
    return db.query(Mission).all()


# --- Get One Mission ---
@router.get("/missions/{mission_id}", response_model=MissionResponse)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


# --- Update a Mission ---
@router.put("/missions/{mission_id}", response_model=MissionResponse)
def update_mission(mission_id: int, data: MissionCreate, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    mission.name = data.name
    mission.description = data.description
    db.commit()
    db.refresh(mission)
    return mission


# --- Delete a Mission ---
@router.delete("/missions/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    db.delete(mission)
    db.commit()
    return {"detail": "Mission deleted"}
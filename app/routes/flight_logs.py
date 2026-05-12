from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import session_factory
from app.models import Mission, FlightLog
from app.schemas import FlightLogCreate, FlightLogResponse

router = APIRouter()


# --- Database Dependency ---
def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


# --- Add a Flight Log to a Mission ---
@router.post("/missions/{mission_id}/logs", response_model=FlightLogResponse)
def create_flight_log(mission_id: int, log: FlightLogCreate, db: Session = Depends(get_db)):
    # Make sure the mission exists
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    new_log = FlightLog(
        mission_id=mission_id,
        speed=log.speed,
        mode=log.mode,
        latitude=log.latitude,
        longitude=log.longitude,
    )
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log


# --- List All Logs for a Mission ---
@router.get("/missions/{mission_id}/logs", response_model=list[FlightLogResponse])
def list_flight_logs(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    return db.query(FlightLog).filter(FlightLog.mission_id == mission_id).all()
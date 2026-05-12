from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.database import session_factory
from app.models import Mission, MissionStep
from app.schemas import MissionExportResponse
from app.algorithms.topological_sort import topological_sort, CircularDependencyError

router = APIRouter()

def get_db():
    db = session_factory()
    try:
        yield db
    finally:
        db.close()

@router.get("/missions/{mission_id}/export", response_model=MissionExportResponse)
def export_mission_data(mission_id: int, db: Session = Depends(get_db)):

    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
        
    return {
        "mission": mission,
        "flight_logs": mission.flight_logs
    }

@router.get("/missions/{mission_id}/export/waypoints", response_class=PlainTextResponse)
def export_mission_waypoints(mission_id: int, db: Session = Depends(get_db)):
   
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    steps = db.query(MissionStep).filter(MissionStep.mission_id == mission_id).all()
    if not steps:
      
        return PlainTextResponse("QGC WPL 110\n")

   
    vertices = [step.id for step in steps]
    edges = []
    step_dict = {step.id: step for step in steps}
    
    for step in steps:
        for prereq in step.prerequisites:
            edges.append((prereq.id, step.id))
            
   
    try:
        sorted_ids = topological_sort(vertices, edges)
    except CircularDependencyError as e:
        raise HTTPException(status_code=400, detail=f"Cannot export: {str(e)}")
        

    lines = ["QGC WPL 110"]
    
    for i, step_id in enumerate(sorted_ids):
        step = step_dict[step_id]
        
  
        command_id = 16 
        if step.command.upper() == "TAKEOFF":
            command_id = 22
        elif step.command.upper() == "LAND":
            command_id = 21
            
        
        index = i
        current_wp = 1 if i == 0 else 0 
        coord_frame = 3 
        param1 = 0.0
        param2 = 0.0
        param3 = 0.0
        param4 = 0.0
        lat = step.latitude
        lon = step.longitude
        alt = step.altitude
        autocontinue = 1
        
        # We use tabs/spaces to separate the columns just like a real .waypoints file
        line = f"{index}\t{current_wp}\t{coord_frame}\t{command_id}\t{param1:.6f}\t{param2:.6f}\t{param3:.6f}\t{param4:.6f}\t{lat:.7f}\t{lon:.7f}\t{alt:.6f}\t{autocontinue}"
        lines.append(line)
        
    return PlainTextResponse("\n".join(lines))

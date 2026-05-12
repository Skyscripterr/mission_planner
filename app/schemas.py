from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class MissionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class MissionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class FlightLogCreate(BaseModel):
    speed: float
    mode: str
    latitude: float
    longitude: float

class FlightLogResponse(BaseModel):
    id: int
    mission_id: int
    speed: float
    mode: str
    latitude: float
    longitude: float
    timestamp: datetime

    class Config:
        from_attributes = True


# --- NEW SCHEMAS FOR DSA ---

class MissionStepCreate(BaseModel):
    name: str
    command: str
    latitude: float = 0.0
    longitude: float = 0.0
    altitude: float = 0.0
    prerequisite_ids: List[int] = [] # The IDs of steps that MUST happen before this one

class MissionStepResponse(BaseModel):
    id: int
    mission_id: int
    name: str
    command: str
    latitude: float
    longitude: float
    altitude: float

    class Config:
        from_attributes = True


class AirspaceRestrictionCreate(BaseModel):
    name: str
    start_time: int
    end_time: int

class AirspaceRestrictionResponse(BaseModel):
    id: int
    name: str
    start_time: int
    end_time: int

    class Config:
        from_attributes = True

class ScheduleMissionRequest(BaseModel):
    start_time: int
    end_time: int

class MissionExportResponse(BaseModel):
    mission: MissionResponse
    flight_logs: List[FlightLogResponse]
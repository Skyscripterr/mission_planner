from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime 
from .database import Base

# Association table for the self-referential many-to-many relationship
# This says: "dependent_id" requires "prerequisite_id" to be finished first.
step_dependencies = Table(
    'step_dependencies', Base.metadata,
    Column('dependent_id', Integer, ForeignKey('mission_steps.id'), primary_key=True),
    Column('prerequisite_id', Integer, ForeignKey('mission_steps.id'), primary_key=True)
)


class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="planned")
    created_at = Column(DateTime, default=datetime.utcnow)

    flight_logs = relationship("FlightLog", back_populates="mission")
    steps = relationship("MissionStep", back_populates="mission")


class FlightLog(Base):
    __tablename__ = "flight_logs"

    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    speed = Column(Float, nullable=False)           # e.g. meters per second
    mode = Column(String, nullable=False)            # e.g. "manual", "auto", "hover"
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    mission = relationship("Mission", back_populates="flight_logs")


class MissionStep(Base):
    """A single command in a drone mission (e.g. TAKEOFF, WAYPOINT)"""
    __tablename__ = "mission_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    name = Column(String, nullable=False)
    command = Column(String, nullable=False) # e.g. "TAKEOFF", "WAYPOINT", "LAND"
    
    # Coordinates (using 0.0 if not needed for a specific command)
    latitude = Column(Float, nullable=False, default=0.0)
    longitude = Column(Float, nullable=False, default=0.0)
    altitude = Column(Float, nullable=False, default=0.0)

    mission = relationship("Mission", back_populates="steps")

    # The magic self-referential relationship for Topological Sort!
    # "What steps must happen before this one?"
    prerequisites = relationship(
        "MissionStep",
        secondary=step_dependencies,
        primaryjoin=id==step_dependencies.c.dependent_id,
        secondaryjoin=id==step_dependencies.c.prerequisite_id,
        backref="dependents"
    )


class AirspaceRestriction(Base):
    """A blocked time window for a specific airspace"""
    __tablename__ = "airspace_restrictions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # Using integer Unix timestamps makes it easy for our Interval Tree
    start_time = Column(Integer, nullable=False) 
    end_time = Column(Integer, nullable=False)

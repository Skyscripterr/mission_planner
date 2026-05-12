from fastapi import FastAPI
from app.database import engine, Base
from app.routes import missions, flight_logs, export, steps, airspace

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mission Planner API",
    description="An API for managing UAV missions and flight logs.",
    version="1.0.0"
)


app.include_router(missions.router, tags=["Missions"])
app.include_router(flight_logs.router, tags=["Flight Logs"])
app.include_router(export.router, tags=["Export"])
app.include_router(steps.router)
app.include_router(airspace.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Mission Planner API!"}

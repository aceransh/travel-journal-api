from typing import List
from fastapi import FastAPI

from models import Trip, TripCreate

app = FastAPI()

_trips: List[Trip] = []
_next_id: int = 1

@app.get("/")
def home():
    return "Hello World"

@app.get("/health")
def health_check():
    return {"Status": "Ok"}

@app.get("/trips", response_model=List[Trip])
def list_trips() -> List[Trip]:
    return _trips

@app.post("/trips", response_model=Trip, status_code=201)
def create_trip(payload: TripCreate) -> Trip:
    global _next_id
    trip = Trip(id=_next_id, **payload.model_dump())
    _trips.append(trip)
    _next_id += 1
    return trip


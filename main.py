from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Response
from datetime import date

from models import Trip, TripCreate, TripDB

from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

_trips: List[Trip] = []
_next_id: int = 1

@app.get("/")
def home():
    return "Hello World"

@app.get("/health")
def health_check():
    return {"Status": "Ok"}

@app.post("/trips", response_model=Trip, status_code=201)
def create_trip(payload: TripCreate) -> Trip:
    global _next_id
    trip = Trip(id=_next_id, **payload.model_dump())
    _trips.append(trip)
    _next_id += 1
    return trip

# @app.get("/trips", response_model=List[Trip])
# def list_trips() -> List[Trip]:
#     return _trips

@app.get("/trips/{trip_id}", response_model=Trip)
def get_trip(trip_id: int) -> Trip:
    for t in _trips:
        if t.id == trip_id:
            return t
    raise HTTPException(status_code=404, detail=f"Trip {trip_id} not found")
    
@app.put("/trips/{trip_id}", response_model=Trip)
def update_trip(trip_id: int, payload: TripCreate) -> Trip:
    for idx, t in enumerate(_trips):
        if t.id == trip_id:
            updated = Trip(id=trip_id, **payload.model_dump())
            _trips[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail=f"Trip {trip_id} not found")

@app.delete("/trips/{trip_id}", status_code=204)
def delete_trip(trip_id: int) -> None:
    for idx, t in enumerate(_trips):
        if t.id == trip_id:
            _trips.pop(idx)
            return 
    raise HTTPException(status_code=404, detail=f"Trip {trip_id} not found") 

@app.get("/trips", response_model=List[Trip])
def list_trips(
    locationName: Optional[str] = Query(None, description="case-insensitive substring"),
    city: Optional[str] = Query(None, description="case-insensitive substring"),
    country: Optional[str] = Query(None, description="case-insensitive substring"),
    visitDate: Optional[date] = Query(None, description="exact date"),
    visitDateFrom: Optional[date] = Query(None, description="inclusive start"),
    visitDateTo: Optional[date] = Query(None, description="inclusive end"),
    rating: Optional[int] = Query(None, ge=1, le=5, description="exact rating"),
    minRating: Optional[int] = Query(None, ge=1, le=5),
    maxRating: Optional[int] = Query(None, ge=1, le=5),

    #pagination
    limit: int = Query(20, ge=1, le=100, description="items per page (1-100)"),
    offset: int = Query(0, ge=0, description="items to skip"),
    response: Response = None,
) -> List[Trip]:
    results = _trips
    def contains(field: str, needle: str) -> bool:
        return needle.lower() in field.lower()

    if locationName:
        results = [t for t in results if contains(t.locationName, locationName)]
    if city:
        results = [t for t in results if contains(t.city, city)]
    if country:
        results = [t for t in results if contains(t.country, country)]

    if visitDate:
        results = [t for t in results if t.visitDate == visitDate]
    if visitDateFrom:
        results = [t for t in results if t.visitDate >= visitDateFrom]
    if visitDateTo:
        results = [t for t in results if t.visitDate <= visitDateTo]

    if rating is not None:
        results = [t for t in results if t.rating == rating]
    if minRating is not None:
        results = [t for t in results if t.rating >= minRating]
    if maxRating is not None:
        results = [t for t in results if t.rating <= maxRating]

    total = len(results)
    if response is not None:
        response.headers["X-Total-Count"] = str(total)
    return results[offset : offset + limit]

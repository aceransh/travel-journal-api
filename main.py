from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException, Query, Response, Depends
from datetime import date

from models import Trip, TripCreate, TripDB

from database import Base, engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

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

# @app.post("/trips", response_model=Trip, status_code=201)
# def create_trip(payload: TripCreate) -> Trip:
#     global _next_id
#     trip = Trip(id=_next_id, **payload.model_dump())
#     _trips.append(trip)
#     _next_id += 1
#     return trip

@app.post("/trips", response_model=Trip, status_code=201)
def create_trip(payload: TripCreate, db: Session = Depends(get_db)) -> Trip:
    row = TripDB(
        locationName = payload.locationName,
        city = payload.city,
        country = payload.country,
        visitDate=payload.visitDate,
        rating=payload.rating,
        notes=payload.notes,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

# @app.get("/trips", response_model=List[Trip])
# def list_trips() -> List[Trip]:
#     return _trips

# @app.get("/trips/{trip_id}", response_model=Trip)
# def get_trip(trip_id: int) -> Trip:
#     for t in _trips:
#         if t.id == trip_id:
#             return t
#     raise HTTPException(status_code=404, detail=f"Trip {trip_id} not found")

@app.get("/trips/{trip_id}", response_model=Trip)
def get_trip(trip_id: int, db: Session = Depends(get_db)) -> Trip:
    row = db.query(TripDB).filter(TripDB.id == trip_id).first()
    if not row:
        raise HTTPException(status_code=404, detail=f"Trip {trip_id} not found")
    return row

# @app.put("/trips/{trip_id}", response_model=Trip)
# def update_trip(trip_id: int, payload: TripCreate) -> Trip:
#     for idx, t in enumerate(_trips):
#         if t.id == trip_id:
#             updated = Trip(id=trip_id, **payload.model_dump())
#             _trips[idx] = updated
#             return updated
#     raise HTTPException(status_code=404, detail=f"Trip {trip_id} not found")

@app.put("/trips/{trip_id}", response_model=Trip)
def update_trip(trip_id: int, payload: TripCreate, db: Session = Depends(get_db)) -> Trip:
    row = db.query(TripDB).filter(TripDB.id == trip_id).first()
    if not row:
        raise HTTPException(status_code=404, detail=f"Trip {trip_id} not found")
    
    row.locationName = payload.locationName
    row.city = payload.city
    row.country = payload.country
    row.visitDate = payload.visitDate
    row.rating = payload.rating
    row.notes = payload.notes

    db.commit()
    return row

# @app.delete("/trips/{trip_id}", status_code=204)
# def delete_trip(trip_id: int) -> None:
#     for idx, t in enumerate(_trips):
#         if t.id == trip_id:
#             _trips.pop(idx)
#             return 
#     raise HTTPException(status_code=404, detail=f"Trip {trip_id} not found") 

@app.delete("/trips/{trip_id}", status_code=204)
def delete_trip(trip_id: int, db: Session = Depends(get_db)) -> None:
    row = db.query(TripDB).filter(TripDB.id == trip_id).first()
    if not row:
        raise HTTPException(status_code=404, detail=f"Trip {trip_id} not found")
    
    db.delete(row)
    db.commit()
    return

# @app.get("/trips", response_model=List[Trip])
# def list_trips(
#     locationName: Optional[str] = Query(None, description="case-insensitive substring"),
#     city: Optional[str] = Query(None, description="case-insensitive substring"),
#     country: Optional[str] = Query(None, description="case-insensitive substring"),
#     visitDate: Optional[date] = Query(None, description="exact date"),
#     visitDateFrom: Optional[date] = Query(None, description="inclusive start"),
#     visitDateTo: Optional[date] = Query(None, description="inclusive end"),
#     rating: Optional[int] = Query(None, ge=1, le=5, description="exact rating"),
#     minRating: Optional[int] = Query(None, ge=1, le=5),
#     maxRating: Optional[int] = Query(None, ge=1, le=5),

#     #pagination
#     limit: int = Query(20, ge=1, le=100, description="items per page (1-100)"),
#     offset: int = Query(0, ge=0, description="items to skip"),
#     response: Response = None,
# ) -> List[Trip]:
#     results = _trips
#     def contains(field: str, needle: str) -> bool:
#         return needle.lower() in field.lower()

#     if locationName:
#         results = [t for t in results if contains(t.locationName, locationName)]
#     if city:
#         results = [t for t in results if contains(t.city, city)]
#     if country:
#         results = [t for t in results if contains(t.country, country)]

#     if visitDate:
#         results = [t for t in results if t.visitDate == visitDate]
#     if visitDateFrom:
#         results = [t for t in results if t.visitDate >= visitDateFrom]
#     if visitDateTo:
#         results = [t for t in results if t.visitDate <= visitDateTo]

#     if rating is not None:
#         results = [t for t in results if t.rating == rating]
#     if minRating is not None:
#         results = [t for t in results if t.rating >= minRating]
#     if maxRating is not None:
#         results = [t for t in results if t.rating <= maxRating]

#     total = len(results)
#     if response is not None:
#         response.headers["X-Total-Count"] = str(total)
#     return results[offset : offset + limit]

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

    limit: int = Query(20, ge=1, le=100, description="items per page (1-100)"),
    offset: int = Query(0, ge=0, description="items to skip"),
    response: Response = None,
    db: Session = Depends(get_db),
):
    
    q = db.query(TripDB)

    if locationName:
        q = q.filter(func.lower(TripDB.locationName).like(f"%{locationName.lower()}%"))
    if city:
        q = q.filter(func.lower(TripDB.city).like(f"%{city.lower()}%"))
    if country:
        q = q.filter(func.lower(TripDB.country).like(f"%{country.lower()}%"))

    if visitDate:
        q = q.filter(TripDB.visitDate == visitDate)
    if visitDateFrom:
        q = q.filter(TripDB.visitDate >= visitDateFrom)
    if visitDateTo:
        q = q.filter(TripDB.visitDate <= visitDateTo)

    if rating is not None:
        q = q.filter(TripDB.rating == rating)
    if minRating is not None:
        q = q.filter(TripDB.rating >= minRating)
    if maxRating is not None:
        q = q.filter(TripDB.rating <= maxRating)

    total = q.count()
    if response is not None:
        response.headers["X-Total-Count"] = str(total)

    rows = q.order_by(TripDB.id.asc()).offset(offset).limit(limit).all()
    return rows

@app.get("/trips/stats/avg-rating-by-country")
def avg_rating_by_country(db: Session = Depends(get_db)) -> List[Dict]:
    rows = (
        db.query(
            TripDB.country.label("country"),
            func.count(TripDB.id).label("count"),
            func.avg(TripDB.rating).label("avgRating"),
        )
        .group_by(TripDB.country)
        .order_by(func.avg(TripDB.rating).desc())
        .all()
    )

    results = []
    for row in rows:
        results.append({
            "country": row.country,
            "count": row.count,
            "avgRating": round(row.avgRating, 2)
        })
    return results

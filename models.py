from datetime import date
from typing import Optional
from pydantic import BaseModel


class TripBase(BaseModel):
    locationName: str
    city: str
    country: str
    visitDate: date
    rating: int
    notes: Optional[str] = None

class TripCreate(TripBase):
    pass

class Trip(TripBase):
    id: int
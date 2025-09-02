from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

from sqlalchemy import Column, Integer, String, Date
from database import Base


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
    model_config = ConfigDict(from_attributes=True)

class TripDB(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    locationName = Column(String, index=True)
    city = Column(String, index=True)
    country = Column(String, index=True)
    visitDate = Column(Date)
    rating = Column(Integer)
    notes = Column(String, nullable=True)    
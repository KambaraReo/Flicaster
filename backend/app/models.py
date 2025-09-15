from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Airport(Base):
  __tablename__ = "airports"

  code = Column(String(10), primary_key=True)
  name = Column(String(100), nullable=False)
  region = Column(String(50), nullable=False)
  scale = Column(String(50), nullable=False)
  lat = Column(Float, nullable=False)
  lon = Column(Float, nullable=False)

  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Flight(Base):
  __tablename__ = "flights"

  flight_no = Column(String(20), primary_key=True)
  departure = Column(String(10), nullable=False)
  arrival = Column(String(10), nullable=False)
  airline_code = Column(String(10), nullable=False)
  distance_km = Column(Float, nullable=False)
  distance_cat = Column(String(20), nullable=False)
  seat_capacity = Column(Integer, nullable=False)

  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

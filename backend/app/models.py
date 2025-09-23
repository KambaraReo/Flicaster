from sqlalchemy import Column, String, Float, Integer, Date, DateTime
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

class FlightHistory(Base):
  __tablename__ = "flight_histories"

  id = Column(Integer, primary_key=True, autoincrement=True)
  flight_no = Column(String(20), nullable=False)
  date = Column(Date, nullable=False)
  month = Column(Integer, nullable=False)
  weekday = Column(Integer, nullable=False)
  holiday_flag = Column(Integer, nullable=False)
  weather_flag = Column(Integer, nullable=False)
  reservations = Column(Integer, nullable=False)
  passengers = Column(Integer, nullable=False)
  seat_capacity = Column(Integer, nullable=False)
  load_factor = Column(Float, nullable=False)
  lag_7 = Column(Float, nullable=True)
  lag_14 = Column(Float, nullable=True)
  lag_30 = Column(Float, nullable=True)

  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FlightCondition(Base):
  __tablename__ = "flight_conditions"

  id = Column(Integer, primary_key=True, autoincrement=True)
  flight_no = Column(String(20), nullable=False)
  date = Column(Date, nullable=False)
  weather_flag = Column(Integer, nullable=False)
  reservations = Column(Integer, nullable=False)
  lag_7 = Column(Float, nullable=True)
  lag_14 = Column(Float, nullable=True)
  lag_30 = Column(Float, nullable=True)

  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

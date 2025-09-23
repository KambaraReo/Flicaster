from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Airport as AirportModel, Flight as FlightModel
from schemas import AirportSchema

router = APIRouter(prefix="/airports", tags=["airports"])

# 全空港一覧を取得
@router.get("/", response_model=List[AirportSchema])
def get_airports(db: Session = Depends(get_db)):
  airports = db.query(AirportModel).all()

  return airports

# 出発空港に基づく到着空港一覧を取得
@router.get("/arrivals", response_model=List[AirportSchema])
def get_arrival_airports(departure: str, db: Session = Depends(get_db)):
  flights = db.query(FlightModel).filter(FlightModel.departure == departure).all()
  arrival_codes = {f.arrival for f in flights}
  airports = db.query(AirportModel).filter(AirportModel.code.in_(arrival_codes)).all()

  return airports

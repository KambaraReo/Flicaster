from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import Flight as FlightModel
from schemas import FlightSchema

router = APIRouter(prefix="/flights", tags=["flights"])

# 出発・到着空港で絞ったフライト一覧を取得
@router.get("/by_route", response_model=List[FlightSchema])
def get_flights_by_route(departure: str, arrival: str, db: Session = Depends(get_db)):
  """
  指定された出発空港と到着空港のフライト一覧を返す
  """
  flights = db.query(FlightModel).filter(
    FlightModel.departure == departure,
    FlightModel.arrival == arrival
  ).all()

  return flights

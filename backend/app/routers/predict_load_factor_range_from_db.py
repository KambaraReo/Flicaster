from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from db import get_db
from models import FlightCondition
from .predict_load_factor import predict_load_factor, LoadFactorFeatures
import jpholiday
from typing import List, Dict

router = APIRouter(tags=["prediction"])

# フロント用リクエストモデル
class LoadFactorRangeRequest(BaseModel):
  start_date: str  # "YYYY-MM-DD"
  end_date: str    # "YYYY-MM-DD"
  departure: str
  arrival: str
  flight_no: str

def is_holiday(dt: date, extra_holidays: List[str] = None) -> int:
  # jpholidayで判定
  if jpholiday.is_holiday(dt):
    return 1

  # 追加の祝日リストで判定
  if extra_holidays and date in extra_holidays:
    return 1

  return 0

def fetch_flight_conditions_range(db: Session, flight_no: str, start_date: str, end_date: str) -> List[Dict]:
  """指定期間のflight_conditionsをまとめて取得"""

  start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
  end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

  records = db.query(FlightCondition).filter(
    FlightCondition.flight_no == flight_no,
    FlightCondition.date >= start_date_obj,
    FlightCondition.date <= end_date_obj
  ).order_by(FlightCondition.date).all()

  if not records:
    raise HTTPException(status_code=404, detail="Flight conditions not found")

  return [
    {
      "date": rec.date,
      "weather_flag": rec.weather_flag,
      "reservations": rec.reservations,
      "lag_7": rec.lag_7,
      "lag_14": rec.lag_14,
      "lag_30": rec.lag_30
    }
    for rec in records
  ]

@router.post("/predict/load_factor_range/from_db")
def predict_load_factor_range_from_db(req: LoadFactorRangeRequest, db: Session = Depends(get_db)):
  """
  フロント用：日付範囲・便名・出発/到着だけ送れば予測が返る
  """

  # 祝日設定を追加
  extra_holidays = ['2025-12-29', '2025-12-30', '2025-12-31', '2026-01-02', '2026-01-03']

  # range で flight_conditions を取得
  cond_range = fetch_flight_conditions_range(db, req.flight_no, req.start_date, req.end_date)

  predictions = []
  for cond in cond_range:
    # LoadFactorFeatures に整形
    features = LoadFactorFeatures(
      month=cond["date"].month,
      weekday=cond["date"].weekday(),
      holiday_flag=is_holiday(cond["date"], extra_holidays),
      weather_flag=cond["weather_flag"],
      reservations=cond["reservations"],
      lag_7=cond["lag_7"],
      lag_14=cond["lag_14"],
      lag_30=cond["lag_30"],
      departure=req.departure,
      arrival=req.arrival
    )

    # 既存 predict_load_factor を呼び出す
    result = predict_load_factor(features)

    # predictions に結果を格納
    predictions.append({
      "date": cond["date"].strftime("%Y-%m-%d"),
      "prediction": result["prediction"],
      "shap_values": result["shap_values"]
    })

  return {
    "flight_no": req.flight_no,
    "departure": req.departure,
    "arrival": req.arrival,
    "predictions": predictions
  }

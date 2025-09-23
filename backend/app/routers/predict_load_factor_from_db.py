from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from db import get_db
from models import FlightCondition  # flight_conditions テーブルの ORM モデル
from .predict_load_factor import predict_load_factor, LoadFactorFeatures
import jpholiday
from datetime import datetime
from typing import List

router = APIRouter(tags=["prediction"])

# フロント用リクエストモデル
class LoadFactorRequest(BaseModel):
  date: str        # "YYYY-MM-DD"
  departure: str
  arrival: str
  flight_no: str

def fetch_flight_conditions(db: Session, flight_no: str, date: str):
  """flight_conditions テーブルから特徴量を取得"""
  record = db.query(FlightCondition).filter(
    FlightCondition.flight_no == flight_no,
    FlightCondition.date == date
  ).first()
  if not record:
    raise HTTPException(status_code=404, detail="Flight conditions not found")

  return {
    "weather_flag": record.weather_flag,
    "reservations": record.reservations,
    "lag_7": record.lag_7,
    "lag_14": record.lag_14,
    "lag_30": record.lag_30
  }

def is_holiday(date: str, extra_holidays: List[str] = None) -> int:
  """
  祝日かどうか判定する
  date: "YYYY-MM-DD" 形式の文字列
  extra_holidays: 手動で追加した祝日リスト
  戻り値: 祝日なら1、そうでなければ0
  """
  dt = datetime.strptime(date, "%Y-%m-%d").date()

  # jpholidayで判定
  if jpholiday.is_holiday(dt):
    return 1

  # 追加の祝日リストで判定
  if extra_holidays and date in extra_holidays:
    return 1

  return 0

@router.post("/predict/load_factor/from_db")
def predict_load_factor_from_db(req: LoadFactorRequest, db: Session = Depends(get_db)):
  """
  フロント用：日付・便名・出発/到着だけ送れば予測が返る
  """
  # flight_conditions を取得
  cond = fetch_flight_conditions(db, req.flight_no, req.date)

  # 日付を datetime に変換
  date_obj = datetime.strptime(req.date, "%Y-%m-%d")

  # 祝日設定を追加
  extra_holidays = ['2025-12-29', '2025-12-30', '2025-12-31', '2026-01-02', '2026-01-03']

  # LoadFactorFeatures に整形
  features = LoadFactorFeatures(
    month=date_obj.month,
    weekday=date_obj.weekday(),
    holiday_flag=is_holiday(req.date, extra_holidays),
    weather_flag=cond["weather_flag"],
    reservations=cond["reservations"],
    lag_7=cond["lag_7"],
    lag_14=cond["lag_14"],
    lag_30=cond["lag_30"],
    departure=req.departure,
    arrival=req.arrival
  )

  # 既存 predict_load_factor を呼び出す
  return predict_load_factor(features)

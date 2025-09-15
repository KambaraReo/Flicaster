from fastapi import APIRouter
import pickle
import pandas as pd
from pathlib import Path
from pydantic import BaseModel, conint

router = APIRouter(tags=["prediction"])

# モデルロード（初回のみ）
MODEL_PATH = Path(__file__).resolve().parent.parent / "data" / "demand_model.pkl"
with open(MODEL_PATH, "rb") as f:
  model = pickle.load(f)

class Features(BaseModel):
  month: conint(ge=1, le=12)
  weekday: conint(ge=0, le=6)
  holiday_flag: conint(ge=0, le=1)
  weather_flag: conint(ge=0, le=1)
  reservations: int
  lag_7: float
  lag_14: float
  lag_30: float

@router.post("/predict/passengers")
def predict_passengers(features: Features):
  """
  features: JSON形式で特徴量を受け取る
  """

  # Pydanticモデルから dict に変換して DataFrame に渡す
  df = pd.DataFrame([features.dict()])

  # 予測
  pred = model.predict(df)

  return {
    "features": features.dict(),
    "prediction": float(pred[0])
  }

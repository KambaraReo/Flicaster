from fastapi import APIRouter
import pickle
import pandas as pd
from pathlib import Path
from pydantic import BaseModel, conint
import shap

router = APIRouter(tags=["prediction"])

# 入力用 Pydantic モデル
class LoadFactorFeatures(BaseModel):
  month: conint(ge=1, le=12)
  weekday: conint(ge=0, le=6)
  holiday_flag: conint(ge=0, le=1)
  weather_flag: conint(ge=0, le=1)
  reservations: int
  lag_7: float
  lag_14: float
  lag_30: float
  departure: str
  arrival: str

# モデルロード（初回のみ）
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "load_factor_model.pkl"
with open(MODEL_PATH, "rb") as f:
  saved = pickle.load(f)

  model = saved["model"]
  le_dep = saved["le_dep"]
  le_arr = saved["le_arr"]

# POST エンドポイント
@router.post("/predict/load_factor")
def predict_load_factor(features: LoadFactorFeatures):
  """
  features: JSON形式で特徴量を受け取る
  """

  # Pydanticモデルから dict に変換して DataFrame に渡す
  df = pd.DataFrame([features.dict()])

  # カテゴリ変数をエンコード
  df["dep_encoded"] = le_dep.transform(df["departure"])
  df["arr_encoded"] = le_arr.transform(df["arrival"])

  # 特徴量の順序を学習時と揃える
  feature_cols = [
    "month", "weekday", "holiday_flag", "weather_flag", "reservations",
    "lag_7", "lag_14", "lag_30",
    "dep_encoded", "arr_encoded"
  ]
  X = df[feature_cols]

  # 予測
  pred = model.predict(X)
  pred = pred.clip(0, 1)

  # SHAP　値の計算
  explainer = shap.TreeExplainer(model)
  shap_values = explainer.shap_values(X)

  # 特徴量ごとの寄与度を dict にまとめる
  shap_dict = {col: float(val) for col, val in zip(feature_cols, shap_values[0])}

  return {
    "features": features.dict(),
    "prediction": float(pred[0]),
    "shap_values": shap_dict
  }

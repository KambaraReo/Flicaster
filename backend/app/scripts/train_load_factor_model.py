# train_load_factor.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import xgboost as xgb
import shap
import pickle
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

# データ読み込み
airport_df = pd.read_csv(os.path.join(DATA_DIR, "airport_master.csv"))
flight_df = pd.read_csv(os.path.join(DATA_DIR, "flight_master.csv"))
history_df = pd.read_csv(os.path.join(DATA_DIR, "flight_history.csv"))

# flight_master.csv と結合して、 departure/arrival を追加
history_df = history_df.merge(
  flight_df[['flight_no', 'departure', 'arrival']],
  on='flight_no',
  how='left'
)

# カテゴリ変数のエンコード
le_dep = LabelEncoder()
le_arr = LabelEncoder()

history_df["dep_encoded"] = le_dep.fit_transform(history_df["departure"])
history_df["arr_encoded"] = le_arr.fit_transform(history_df["arrival"])

# 特徴量・目的変数設定
feature_cols = [
  "month", "weekday", "holiday_flag", "weather_flag", "reservations",
  "lag_7", "lag_14", "lag_30",
  "dep_encoded", "arr_encoded"
]
target_col = "load_factor"

X = history_df[feature_cols]
y = history_df[target_col]

# 学習用とテスト用に分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost モデル学習
model = xgb.XGBRegressor(
  n_estimators=200,
  max_depth=5,
  learning_rate=0.1,
  random_state=42
)

# 学習用データを使ってモデルを学習
model.fit(X_train, y_train)

# モデル評価
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
print(f"RMSE: {rmse:.3f}, MAE: {mae:.3f}")

# モデル保存
os.makedirs(MODEL_DIR, exist_ok=True)
model_path = os.path.join(MODEL_DIR, "load_factor_model.pkl")

with open(model_path, "wb") as f:
  pickle.dump({
    "model": model,
    "le_dep": le_dep,
    "le_arr": le_arr
  }, f)

print(f"load_factor モデルを保存しました: {model_path}")

# SHAP 可視化
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

plt.figure()
shap.summary_plot(shap_values, X_test, show=False)
os.makedirs(REPORT_DIR, exist_ok=True)
shap_path = os.path.join(REPORT_DIR, "shap_summary_for_lf.png")
plt.savefig(shap_path)

print(f"SHAP可視化を保存しました: {shap_path}")

import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import shap
import pickle
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

# データ読み込み
df = pd.read_csv(os.path.join(DATA_DIR, "flight_history.csv"))

# 特徴量選択
feature_cols = ["month", "weekday", "holiday_flag", "weather_flag", "reservations", "lag_7", "lag_14", "lag_30"]
X = df[feature_cols]
y = df["passengers"]

# 学習用とテスト用に分割
X_train, X_test, y_train, y_test = train_test_split(
  X, y, test_size=0.2, random_state=42
)

# XGBoost の回帰モデルを定義
model = XGBRegressor(
  n_estimators=200,
  max_depth=5,
  learning_rate=0.1,
  random_state=42
)

# 学習用データを使ってモデルを学習
model.fit(X_train, y_train)

# モデル保存
os.makedirs(MODEL_DIR, exist_ok=True)
model_path = os.path.join(MODEL_DIR, "passenger_model.pkl")
with open(model_path, "wb") as f:
  pickle.dump(model, f)

print(f"モデルを保存しました: {model_path}")

# SHAP 可視化
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

plt.figure()
shap.summary_plot(shap_values, X_test, show=False)
os.makedirs(REPORT_DIR, exist_ok=True)
shap_path = os.path.join(REPORT_DIR, "shap_summary_for_pax.png")
plt.savefig(shap_path)
print(f"SHAP可視化を保存しました: {shap_path}")

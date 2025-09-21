import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# 保存先ディレクトリ
data_dir = "../data"
os.makedirs(data_dir, exist_ok=True)

# 便マスタ読み込み
flight_master = pd.read_csv(f"{data_dir}/flight_master.csv")

# 日付範囲
start_date = datetime(2025, 10, 1)
end_date = datetime(2026, 9, 30)
dates = pd.date_range(start_date, end_date)

np.random.seed(42)

records = []

for _, flight in flight_master.iterrows():
  for date in dates:
    weather_flag = np.random.choice([0,1], p=[0.9,0.1])
    reservations = np.random.randint(50, flight['seat_capacity'] + 1)

    # 基本 load_factor を生成
    lag_30 = np.random.uniform(0.5, 0.7)
    lag_14 = lag_30 + np.random.uniform(0.01, 0.1)
    lag_7  = lag_14 + np.random.uniform(0.01, 0.1)

    # lag_14 にキャンセルシナリオ
    if np.random.rand() < 0.2:
      factor = np.random.uniform(0.7, 1.0)
      lag_14 *= factor

    # lag_7 にキャンセルシナリオ
    if np.random.rand() < 0.2:
      factor = np.random.uniform(0.7, 1.0)
      lag_7 *= factor

    records.append({
      "flight_no": flight['flight_no'],
      "date": date.strftime("%Y-%m-%d"),
      "weather_flag": weather_flag,
      "reservations": reservations,
      "lag_7": round(lag_7, 3),
      "lag_14": round(lag_14, 3),
      "lag_30": round(lag_30, 3)
    })

# DataFrame に変換
df = pd.DataFrame(records)

# CSVに保存
df.to_csv(f"{data_dir}/flight_condition.csv", index=False)

print("data/ に flight_condition.csv を生成しました。")

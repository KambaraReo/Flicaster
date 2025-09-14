import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# 保存先ディレクトリ
data_dir = "../data"
os.makedirs(data_dir, exist_ok=True)

# 便マスタ読み込み
flight_master = pd.read_csv(f"{data_dir}/flight_master.csv")
airport_master = pd.read_csv(f"{data_dir}/airport_master.csv")

# 日付範囲
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
dates = pd.date_range(start_date, end_date)

# 祝日フラグ（元旦・GW・お盆・年末年始など適当に設定）
holidays = [
  "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-08", "2024-02-11",
  "2024-02-12", "2024-02-23", "2024-03-20", "2024-04-29", "2024-04-30",
  "2024-05-01", "2024-05-02", "2024-05-03", "2024-05-04", "2024-05-05",
  "2024-05-06", "2024-07-15", "2024-08-11", "2024-08-12", "2024-08-13",
  "2024-08-14", "2024-08-15", "2024-09-16", "2024-09-22", "2024-09-23",
  "2024-10-14", "2024-11-03", "2024-11-04", "2024-11-23", "2024-12-29",
  "2024-12-30", "2024-12-31"
]

# 天候フラグ（0:通常, 1:悪天候）をランダムで設定
np.random.seed(42)

records = []

for _, flight in flight_master.iterrows():
  dep_airport = airport_master[airport_master['code'] == flight['departure']].iloc[0]
  arr_airport = airport_master[airport_master['code'] == flight['arrival']].iloc[0]

  # hub判定（出発空港または到着空港が hub かどうか）
  is_hub = (dep_airport['scale'] == 'hub') or (arr_airport['scale'] == 'hub')

  for date in dates:
    month = date.month
    weekday = date.weekday()
    holiday_flag = int(date.strftime("%Y-%m-%d") in holidays)
    weekend_flag = int(weekday >= 5)
    weather_flag = np.random.choice([0,1], p=[0.9,0.1])  # 10%の悪天候

    # base_demand は内部計算用
    base_demand = 50  # 基本値
    if is_hub:
      base_demand += 50  # hub便は需要高め
    if flight['distance_cat'] == "medium":
      base_demand += 10
    elif flight['distance_cat'] == "long":
      base_demand += 20
    if weekend_flag:
      base_demand += 5
    if holiday_flag:
      base_demand += 10
    if weather_flag == 1:
      base_demand -= 10  # 悪天候で減少

    # 予約者数
    reservations = int(base_demand * np.random.uniform(0.7, 0.95))
    # 搭乗者数
    passengers = int(reservations * np.random.uniform(0.9,1.0))
    # 搭乗率
    load_factor = round(passengers / flight['seat_capacity'], 3)

    records.append({
      "flight_no": flight['flight_no'],
      "date": date.strftime("%Y-%m-%d"),
      "month": month,
      "weekday": weekday,
      "holiday_flag": holiday_flag,
      "weather_flag": weather_flag,
      "reservations": reservations,
      "passengers": passengers,
      "seat_capacity": flight['seat_capacity'],
      "load_factor": load_factor
    })

# DataFrame化
df = pd.DataFrame(records)

# n日前の搭乗者数ラグ作成
df = df.sort_values(['flight_no','date'])
for lag in [7,14,30]:
  lag_col = f'lag_{lag}'
  df[lag_col] = df.groupby('flight_no')['passengers'].shift(lag)

  # ラグが存在しない最初の数日だけ便ごとの平均で補完
  df[lag_col] = df.groupby('flight_no')[lag_col].transform(lambda x: x.fillna(x.mean()))

# CSV出力
df.to_csv(f"{data_dir}/flight_history.csv", index=False)

print("data/ に flight_history.csv を生成しました。")

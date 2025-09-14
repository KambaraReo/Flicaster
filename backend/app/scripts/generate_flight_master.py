import pandas as pd
import numpy as np
import os
from itertools import count

# 距離計算用の関数を用意
def haversine(lat1, lon1, lat2, lon2):
  """2地点の距離（km）を計算"""
  R = 6371  # 地球半径 (km)
  phi1, phi2 = np.radians(lat1), np.radians(lat2)
  dphi = phi2 - phi1
  dlambda = np.radians(lon2 - lon1)
  a = np.sin(dphi/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2)**2
  return 2 * R * np.arcsin(np.sqrt(a))

def get_distance_category(distance_km):
  """距離カテゴリを自動判定"""
  if distance_km <= 500:
    return "short"
  elif distance_km <= 1500:
    return "medium"
  else:
    return "long"

def get_seat_capacity(distance_cat):
  """距離カテゴリに応じた座席数を設定"""
  if distance_cat == "short":
    return np.random.choice([60, 70, 80, 90])
  elif distance_cat == "medium":
    return np.random.choice([100, 120, 140, 150])
  else:
    return np.random.choice([180, 200, 220, 240])

# 保存先ディレクトリ
data_dir = "../data"
os.makedirs(data_dir, exist_ok=True)

# 空港マスタ読み込み
airport_master = pd.read_csv(f"{data_dir}/airport_master.csv")

# 全空港ペア作成（同じ空港・同じ地域は除外）
routes = airport_master.merge(
  airport_master, how='cross', suffixes=('_dep', '_arr')
)
routes = routes[
  (routes['code_dep'] != routes['code_arr']) &
  (routes['region_dep'] != routes['region_arr'])
]
possible_routes = list(routes[['code_dep', 'code_arr']].itertuples(index=False, name=None))

# ランダムに50路線選択
np.random.seed(42)
selected_indices = np.random.choice(len(possible_routes), size=50, replace=False)
selected_routes = [possible_routes[i] for i in selected_indices]

# 便番号生成＆距離カテゴリ判定
flight_master_records = []
flight_counter = count(101)
airline_codes = ["NH", "JL", "BC", "7G", "6J"]

for dep, arr in selected_routes:
  airline_code = np.random.choice(airline_codes)
  flight_no = f"{airline_code}{next(flight_counter)}"

  # 出発・到着空港の緯度経度取得
  dep_row = airport_master[airport_master['code'] == dep].iloc[0]
  arr_row = airport_master[airport_master['code'] == arr].iloc[0]
  distance_km = haversine(dep_row['lat'], dep_row['lon'], arr_row['lat'], arr_row['lon'])
  distance_cat = get_distance_category(distance_km)
  seat_capacity = get_seat_capacity(distance_cat)

  flight_master_records.append({
    "flight_no": flight_no,
    "departure": dep,
    "arrival": arr,
    "airline_code": airline_code,
    "distance_km": round(distance_km, 1),
    "distance_cat": distance_cat,
    "seat_capacity": seat_capacity
  })

# DataFrame に変換
flight_master = pd.DataFrame(flight_master_records)

# CSVに保存
flight_master.to_csv(f"{data_dir}/flight_master.csv", index=False)

print("data/ に flight_master.csv を生成しました。")

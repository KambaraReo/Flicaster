import pandas as pd
import os

# 保存先ディレクトリ
data_dir = "../data"
os.makedirs(data_dir, exist_ok=True)

# 空港マスタ用リスト（20件）
airport_list = [
  {"code": "HND", "name": "Tokyo Haneda", "region": "Kanto", "scale": "hub", "lat": 35.553333, "lon": 139.781113},
  {"code": "NRT", "name": "Narita", "region": "Kanto", "scale": "hub", "lat": 35.769272, "lon": 140.389898},
  {"code": "ITM", "name": "Osaka Itami", "region": "Kansai", "scale": "regional", "lat": 34.7840, "lon": 135.4368},
  {"code": "KIX", "name": "Kansai Intl", "region": "Kansai", "scale": "hub", "lat": 34.427299, "lon": 135.244003},
  {"code": "CTS", "name": "New Chitose", "region": "Hokkaido", "scale": "hub", "lat": 42.7718, "lon": 141.6888},
  {"code": "OKA", "name": "Naha", "region": "Okinawa", "scale": "hub", "lat": 26.1966997, "lon": 127.648952},
  {"code": "FUK", "name": "Fukuoka", "region": "Kyushu", "scale": "hub", "lat": 33.5840, "lon": 130.4510},
  {"code": "NGO", "name": "Chubu Centrair", "region": "Chubu", "scale": "hub", "lat": 34.858334, "lon": 136.805283},
  {"code": "SDJ", "name": "Sendai", "region": "Tohoku", "scale": "regional", "lat": 38.1375, "lon": 140.9186},
  {"code": "AOJ", "name": "Aomori", "region": "Tohoku", "scale": "regional", "lat": 40.7375, "lon": 140.7392},
  {"code": "AKJ", "name": "Asahikawa", "region": "Hokkaido", "scale": "regional", "lat": 43.7700, "lon": 142.3656},
  {"code": "HIJ", "name": "Hiroshima", "region": "Chugoku", "scale": "regional", "lat": 34.4340, "lon": 132.9195},
  {"code": "OKJ", "name": "Okayama", "region": "Chugoku", "scale": "regional", "lat": 34.8019, "lon": 133.9347},
  {"code": "MYJ", "name": "Matsuyama", "region": "Shikoku", "scale": "regional", "lat": 33.8392, "lon": 132.7653},
  {"code": "TAK", "name": "Takamatsu", "region": "Shikoku", "scale": "regional", "lat": 34.1850, "lon": 134.0433},
  {"code": "KOJ", "name": "Kagoshima", "region": "Kyushu", "scale": "regional", "lat": 31.8036, "lon": 130.7181},
  {"code": "KMI", "name": "Miyazaki", "region": "Kyushu", "scale": "regional", "lat": 31.9111, "lon": 131.4450},
  {"code": "ISG", "name": "Ishigaki", "region": "Okinawa", "scale": "regional", "lat": 24.3442, "lon": 124.1897},
  {"code": "SHM", "name": "Shimojishima", "region": "Okinawa", "scale": "regional", "lat": 24.8050, "lon": 124.1850},
  {"code": "OIT", "name": "Oita", "region": "Kyushu", "scale": "regional", "lat": 33.0800, "lon": 131.7194}
]

# DataFrame に変換
airport_master = pd.DataFrame(airport_list)

# CSVに保存
airport_master.to_csv(f"{data_dir}/airport_master.csv", index=False)

print("data/ に airport_master.csv を生成しました。")

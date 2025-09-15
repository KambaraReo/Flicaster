# load_data.py
import pandas as pd
from db import SessionLocal, engine
from models import Base, Airport, Flight

# CSV ファイルパス
AIRPORT_CSV = "data/airport_master.csv"
FLIGHT_CSV = "data/flight_master.csv"

def load_airports(session):
  airports_df = pd.read_csv(AIRPORT_CSV)
  for _, row in airports_df.iterrows():
    airport = Airport(
      code=row["code"],
      name=row["name"],
      region=row["region"],
      scale=row["scale"],
      lat=row["lat"],
      lon=row["lon"]
    )
    session.add(airport)
  print(f"{len(airports_df)} 件の空港データを追加しました。")

def load_flights(session):
  flights_df = pd.read_csv(FLIGHT_CSV)
  for _, row in flights_df.iterrows():
    flight = Flight(
      flight_no=row["flight_no"],
      departure=row["departure"],
      arrival=row["arrival"],
      airline_code=row["airline_code"],
      distance_km=row["distance_km"],
      distance_cat=row["distance_cat"],
      seat_capacity=row["seat_capacity"]
    )
    session.add(flight)
  print(f"{len(flights_df)} 件の便データを追加しました。")

def main():
  # テーブルがまだ作成されていない場合は作成
  Base.metadata.create_all(bind=engine)

  session = SessionLocal()
  try:
    load_airports(session)
    load_flights(session)
    session.commit()
    print("データベースへの投入が完了しました。")
  except Exception as e:
    session.rollback()
    print("データ投入中にエラーが発生しました:", e)
  finally:
    session.close()

if __name__ == "__main__":
  main()

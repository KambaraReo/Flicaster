# load_data.py
import pandas as pd
from db import SessionLocal, engine
from models import Base, Airport, Flight, FlightHistory, FlightCondition

# CSV ファイルパス
AIRPORT_CSV = "data/airport_master.csv"
FLIGHT_CSV = "data/flight_master.csv"
FLIGHT_HISTORY_CSV = "data/flight_history.csv"
FLIGHT_CONDITION_CSV = "data/flight_condition.csv"

def load_airports(session):
  airports_df = pd.read_csv(AIRPORT_CSV)
  added_count = 0
  for _, row in airports_df.iterrows():
    exists = session.query(Airport).filter_by(code=row["code"]).first()
    if exists:
      continue
    airport = Airport(
      code=row["code"],
      name=row["name"],
      region=row["region"],
      scale=row["scale"],
      lat=row["lat"],
      lon=row["lon"]
    )
    session.add(airport)
    added_count += 1
  print(f"{added_count} 件の空港データを追加しました。")

def load_flights(session):
  flights_df = pd.read_csv(FLIGHT_CSV)
  added_count = 0
  for _, row in flights_df.iterrows():
    exists = session.query(Flight).filter_by(flight_no=row["flight_no"]).first()
    if exists:
      continue
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
    added_count += 1
  print(f"{added_count} 件の便データを追加しました。")

def load_flight_histories(session):
  flight_histories_df = pd.read_csv(FLIGHT_HISTORY_CSV)
  added_count = 0
  for _, row in flight_histories_df.iterrows():
    exists = session.query(FlightHistory).filter_by(
      flight_no=row["flight_no"],
      date=row["date"]
    ).first()
    if exists:
      continue
    fh = FlightHistory(
      flight_no=row["flight_no"],
      date=row["date"],
      month=row["month"],
      weekday=row["weekday"],
      holiday_flag=row["holiday_flag"],
      weather_flag=row["weather_flag"],
      reservations=row["reservations"],
      passengers=row["passengers"],
      seat_capacity=row["seat_capacity"],
      load_factor=row["load_factor"],
      lag_7=row["lag_7"],
      lag_14=row["lag_14"],
      lag_30=row["lag_30"],
    )
    session.add(fh)
    added_count += 1
  print(f"{added_count} 件のフライト履歴データを追加しました。")

def load_flight_conditions(session):
  df = pd.read_csv(FLIGHT_CONDITION_CSV)
  added_count = 0
  for _, row in df.iterrows():
    exists = session.query(FlightCondition).filter_by(
      flight_no=row["flight_no"],
      date=row["date"]
    ).first()
    if exists:
      continue
    fc = FlightCondition(
      flight_no=row["flight_no"],
      date=row["date"],
      weather_flag=row["weather_flag"],
      reservations=row["reservations"],
      lag_7=row["lag_7"],
      lag_14=row["lag_14"],
      lag_30=row["lag_30"]
    )
    session.add(fc)
    added_count += 1
  print(f"{added_count} 件のフライト条件データを追加しました。")

def main():
  # テーブルがまだ作成されていない場合は作成
  Base.metadata.create_all(bind=engine)

  session = SessionLocal()
  try:
    load_airports(session)
    load_flights(session)
    load_flight_histories(session)
    load_flight_conditions(session)
    session.commit()
    print("データベースへの投入が完了しました。")
  except Exception as e:
    session.rollback()
    print("データ投入中にエラーが発生しました:", e)
  finally:
    session.close()

if __name__ == "__main__":
  main()

from pydantic import BaseModel

class AirportSchema(BaseModel):
  code: str
  name: str
  region: str
  scale: str
  lat: float
  lon: float

  class Config:
    orm_mode = True


class FlightSchema(BaseModel):
  flight_no: str
  departure: str
  arrival: str
  airline_code: str
  distance_km: float
  distance_cat: str
  seat_capacity: int

  class Config:
    orm_mode = True

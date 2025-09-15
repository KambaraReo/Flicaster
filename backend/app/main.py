from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from init_db import init_db

from routers.health import router as health_router
from routers.predict_passenger import router as predict_passenger_router
from routers.predict_load_factor import router as predict_load_factor_router
from routers.airports import router as airports_router
from routers.flights import router as flights_router

app = FastAPI()

# CORS 設定
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3100"],  # Next.js 開発サーバ
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# DBテーブル作成
init_db()

# router の登録
app.include_router(health_router)
app.include_router(predict_passenger_router)
app.include_router(predict_load_factor_router)
app.include_router(airports_router)
app.include_router(flights_router)

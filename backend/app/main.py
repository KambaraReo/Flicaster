from fastapi import FastAPI
from routers.health import router as health_router
from routers.predict_passenger import router as predict_passenger_router

app = FastAPI()

# router の登録
app.include_router(health_router)
app.include_router(predict_passenger_router)

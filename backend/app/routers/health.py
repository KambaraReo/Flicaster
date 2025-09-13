from fastapi import APIRouter
from db_test import test_connection

router = APIRouter()

@router.get("/health")
def health():
  try:
    val = test_connection()
    return {"status": "ok", "db_test": val}
  except Exception as e:
    return {"status": "error", "detail": str(e)}

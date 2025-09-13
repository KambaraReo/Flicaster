from db import engine
from sqlalchemy import text

def test_connection():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    return result.scalar()

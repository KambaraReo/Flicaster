from sqlalchemy.orm import sessionmaker
from models import Base
from db import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
  try:
    # テーブル作成
    Base.metadata.create_all(bind=engine)
    print("DB テーブル作成完了")
  except Exception as e:
    print(f"DB 作成時にエラー: {e}")

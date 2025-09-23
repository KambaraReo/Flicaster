from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# 環境変数から DB 情報を取得
DB_USER = os.environ.get("MYSQL_USER", "user")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD", "password")
DB_NAME = os.environ.get("MYSQL_DATABASE", "flicaster_db")

# Docker 内のコンテナ名でホスト指定
DB_HOST = "db"
DB_PORT = 3306

# SQLAlchemy の接続文字列
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# エンジン作成
engine = create_engine(DB_URL, echo=True, future=True)

# Session の雛形作成
SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

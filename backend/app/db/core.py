from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Engine 생성
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# 세션 팩토리 정의
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base 클래스
Base = declarative_base()

# Dependency 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
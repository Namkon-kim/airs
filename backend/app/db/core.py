import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from dotenv import load_dotenv

load_dotenv(verbose=True)

dbms = os.getenv('DBMS')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')
options = os.getenv('DB_OPTIONS')

database_url = f'{dbms}://{user}:{password}@{host}:{port}/{database}'
if options:
    database_url += f'?{options}'

engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

# Dependency 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

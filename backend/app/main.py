import uvicorn

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1 import router as v1_router

from app.db.core import Base, engine, get_db
from app.db.model import User
from app.schemas.user import UserCreate, UserRead
from app.db.user import get_user, create_user

# 모든 테이블 삭제
# Base.metadata.drop_all(bind=engine)

# 데이터베이스 초기화
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(v1_router)


@app.post("/users/", response_model=UserRead)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


if __name__ == '__main__':
    uvicorn.run('main:app')

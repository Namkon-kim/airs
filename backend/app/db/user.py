from sqlalchemy.orm import Session
from model import User
from app.schemas.user import UserCreate
from app.db.core import SessionLocal


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(user_id=user.user_id,
                   username=user.username,
                   email=user.email,
                   dept_id=user.dept_id,
                   password=user.password,
                   gender=user.gender)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


if __name__ == '__main__':
    # TODO : get_user 테스트 해보기
    user = UserCreate
    user.user_id = 'so22816'
    user.username = '김남곤'
    user.email = 'namkon.kim@sk.com'
    user.dept_id = 'MI'
    user.password = 'qwer12#$'
    user.gender = 'M'
    create_user(SessionLocal, user)

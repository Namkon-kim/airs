from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, and_, or_
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from app.db.model import User
from app.schemas.user import UserCreate
from app.db.core import SessionLocal


class UserService:
    def __init__(self, session: Session):
        """
        UserService 클래스 초기화
        :param session: SQLAlchemy Session 객체
        """
        self.session = session

    def get_user_by_user_id(self, user_id: str):
        """
        User ID 기반 사용자 조회
        :param user_id: 사용자 ID
        :return: 사용자 정보
        """
        stmt = select(User).where(User.user_id == user_id)
        return self.session.execute(stmt).scalar()

    def create_user(self, user: User):
        try:
            self.session.add(user)
            self.session.commit()

        except IntegrityError:
            self.session.rollback()
            return False

        return True

    def get_all_users(self):
        """
        모든 사용자 조회
        :return: User 객체 리스트
        """
        stmt = select(User)
        return self.session.execute(stmt).scalars().all()

    def get_active_users(self):
        """
        활성화된 사용자 조회
        :return: 활성화된 User 객체 리스트
        """
        stmt = select(User).where(User.is_active == True)
        return self.session.execute(stmt).scalars().all()

    def get_users_ordered_by_username(self):
        """
        username 기준으로 정렬된 사용자 조회
        :return: 정렬된 User 객체 리스트
        """
        stmt = select(User).order_by(User.username)
        return self.session.execute(stmt).scalars().all()

    def get_usernames_and_emails(self):
        """
        사용자 이름과 이메일만 조회
        :return: (username, email) 튜플 리스트
        """
        stmt = select(User.username, User.email)
        return self.session.execute(stmt).all()

    def get_paginated_users(self, limit: int, offset: int):
        """
        페이징 처리된 사용자 조회
        :param limit: 가져올 사용자 수
        :param offset: 시작 위치
        :return: 페이징 처리된 User 객체 리스트
        """
        stmt = select(User).limit(limit).offset(offset)
        return self.session.execute(stmt).scalars().all()

    def get_complex_query_results(self):
        """
        복잡한 조건으로 사용자 조회
        - 활성화된 사용자 중 부서가 'IT'이거나 성별이 'F'인 사용자
        :return: 조건에 맞는 User 객체 리스트
        """
        stmt = select(User).where(
            and_(
                User.is_active == True,
                or_(
                    User.dept_id == 'IT',
                    User.gender == 'F'
                )
            )
        ).order_by(User.created_at.desc())
        return self.session.execute(stmt).scalars().all()

user_service = UserService(SessionLocal)


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
    # user = UserCreate
    # user.user_id = 'so22816'
    # user.username = '김남곤'
    # user.email = 'namkon.kim@sk.com'
    # user.dept_id = 'MI'
    # user.password = 'qwer12#$'
    # user.gender = 'M'
    # create_user(SessionLocal, user)
    ret = user_service.get_user_by_user_id('so228162')
    print(ret)
    print('t' if ret else 'f')
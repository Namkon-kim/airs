from sqlalchemy import Column, Integer, VARCHAR, Enum, TIMESTAMP, BOOLEAN, text
from app.db.core import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(VARCHAR(7), primary_key=True)
    password = Column(VARCHAR(60), nullable=False)
    username = Column(VARCHAR(5), nullable=False, index=True)
    email = Column(VARCHAR(50), unique=True, nullable=False)
    dept_id = Column(VARCHAR(50), nullable=False)
    gender = Column(Enum('M', 'F', 'O'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    last_login = Column(TIMESTAMP)
    is_active = Column(BOOLEAN, default=True)


if __name__ == '__main__':
    from core import Base, engine, get_db

    Base.metadata.create_all(bind=engine)

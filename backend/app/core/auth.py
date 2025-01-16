import os
import bcrypt

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import JSONResponse
from typing import Union, Dict
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
from app.db import user_service

load_dotenv(verbose=True)

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')


def get_password_hash(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def match_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def authenticate_user(emp_id: str, password: str):
    user = user_service.get_user_by_user_id(emp_id)
    if not user:
        return False
    if not match_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str) -> Dict[str, str]:
    decoded_jwt = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
    return decoded_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error:bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                return JSONResponse(
                    status_code=403,
                    content=dict(msg='Invalid authentication scheme')
                )
            if not self.verify_token(credentials.credentials):
                return JSONResponse(
                    status_code=403,
                    content=dict(msg='Invalid token or expired token')
                )
            return credentials.credentials
        else:
            JSONResponse(
                status_code=403,
                content=dict(msg='Invalid authorization code')
            )

    def verify_token(self, token: str, check_expire: bool = True) -> bool:
        is_valid: bool

        try:
            payload = decode_jwt(token)
        except:
            payload = None

        if payload:
            if check_expire:
                # To-do : expired datetime 구성
                is_valid = True
            else:
                is_valid = True
        else:
            is_valid = False

        return is_valid

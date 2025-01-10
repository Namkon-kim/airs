import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Union
from pydantic import SecretStr

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse

from models import Token, UserRegister, CustomOAuth2PasswordRequestForm, OAuth2PasswordRequestForm
from database.portal import Users
from lib.auth import get_password_hash, match_password, create_access_token


ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix='/auth')


@router.post('/v1/register/email')
def register_new_user(reg_info: UserRegister = Depends()):
    """회원가입 API
    Parameters:


    Returns:
        aa
    """
    user_info = Users.get(reg_info.email)
    is_exist = True if user_info else False
    pw = reg_info.password.get_secret_value()
    pw_val = reg_info.password_valid.get_secret_value()
    if not reg_info.email or not pw:
        return JSONResponse(status_code=400, content=dict(msg='Email and Password must be provided'))
    if is_exist:
        return JSONResponse(status_code=400, content=dict(msg='Email is already exists'))
    hashed_password = get_password_hash(pw)
    Users.create(email=reg_info.email,
                 password=hashed_password,
                 name=reg_info.name,
                 phone_number=reg_info.phone_number)
    return JSONResponse(status_code=200, content=dict(msg='success'))


@router.post("/v1/auth", response_model=Token)
async def login_for_access_token(login_info: CustomOAuth2PasswordRequestForm = Depends()):
    user = Users.get(login_info.username)
    if not user:
        return JSONResponse(
            status_code=401,
            content=dict(msg='Unknown or invalid email address'),
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not match_password(login_info.password, user.get('password')):
        return JSONResponse(
            status_code=401,
            content=dict(msg='Incorrect password'),
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user['email']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

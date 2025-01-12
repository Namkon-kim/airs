import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Union
from pydantic import SecretStr

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse

from app.schemas.auth import Token, CustomOAuth2PasswordRequestForm, OAuth2PasswordRequestForm
from app.schemas.user import UserRegister
from app.db import user_service
from app.db.model import User
from app.core.auth import get_password_hash, match_password, create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix='/auth')


@router.post('/register')
def register_new_user(reg_info: UserRegister):
    """회원가입 API
    Parameters:


    Returns:
        aa
    """
    user_info = user_service.get_user_by_user_id(reg_info.emp_id)
    is_exist = True if user_info else False
    pw = reg_info.password.get_secret_value()
    pw_val = reg_info.password_valid.get_secret_value()
    if not reg_info.emp_id or not pw or not reg_info.email:
        return JSONResponse(status_code=400, content=dict(msg='Employee ID, Email and Password must be provided'))
    if is_exist:
        return JSONResponse(status_code=400, content=dict(msg='User is already exists'))
    hashed_password = get_password_hash(pw)
    user = User(user_id=reg_info.emp_id,
                username=reg_info.name,
                email=reg_info.email,
                dept_id=reg_info.dept_id,
                password=hashed_password,
                gender=reg_info.gender)

    ret = user_service.create_user(user)
    if not ret:
        return JSONResponse(status_code=400, content=dict(msg='Email is duplicated'))

    return JSONResponse(status_code=200, content=dict(msg='success'))


@router.post("/login", response_model=Token)
async def login(login_info: CustomOAuth2PasswordRequestForm = Depends()):
    user = User.get(login_info.username)
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

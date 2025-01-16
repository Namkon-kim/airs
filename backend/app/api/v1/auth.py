import bcrypt
import time
from jose import JWTError, jwt
from datetime import datetime, timedelta

from typing import Union, Annotated
from pydantic import SecretStr

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse

from app.schemas.auth import CustomOAuth2PasswordRequestForm
from app.schemas.user import UserRegister
from app.db import user_service
from app.db.model import User
from app.core.auth import get_password_hash, match_password, create_access_token, authenticate_user

ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(prefix='/auth')


@router.post('/register')
def register_new_user(reg_info: UserRegister):
    """회원가입 API
    Parameters:


    Returns:
        aa
    """
    is_exist = (user_service.value_counts(User.emp_id, reg_info.emp_id) or
                user_service.value_counts(User.email, reg_info.email))
    pw = reg_info.password.get_secret_value()
    if not reg_info.emp_id or not pw or not reg_info.email:
        return JSONResponse(status_code=400, content=dict(msg='Employee ID, Email and Password must be provided'))
    if is_exist:
        return JSONResponse(status_code=400, content=dict(msg='User is already exists'))
    hashed_password = get_password_hash(pw)
    user = User(emp_id=reg_info.emp_id,
                username=reg_info.name,
                email=reg_info.email,
                dept_id=reg_info.dept_id,
                password=hashed_password,
                gender=reg_info.gender)

    ret = user_service.create_user(user)

    return JSONResponse(status_code=200, content=dict(msg='success'))


@router.post("/login")
async def login_for_access_token(form_data: Annotated[CustomOAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        return JSONResponse(status_code=401, content=dict(msg="Incorrect username or password"),
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.emp_id,
              'iss': 'airs',
              'iat': int(time.time()),
              'username': user.username},
        expires_delta=access_token_expires
    )
    return JSONResponse(status_code=200, content=dict(msg='success', access_token=access_token, token_type="bearer"),
                        headers={"WWW-Authenticate": "Bearer"})

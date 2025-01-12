from enum import Enum

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Form
from typing import Union, Optional
from pydantic import validator, SecretStr, Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(self,
                 email: str = Form(...),
                 password: SecretStr = Form(...)):
        super().__init__(username=email,
                         password=password.get_secret_value(),
                         scope='',
                         client_id=None,
                         client_secret=None)


class UserToken(BaseModel):
    id: int
    password: str = None
    email: str = None
    name: str = None
    phone_number: str = None

    class Config:
        from_attributes = True

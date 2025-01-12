from enum import Enum

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Form
from typing import Union, Optional
from pydantic import validator, SecretStr
from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserRegister:
    def __init__(self,
                 email: EmailStr = Form(...),
                 password: SecretStr = Form(...),
                 password_valid: SecretStr = Form(...),
                 name: str = Form(...),
                 phone_number: Optional[str] = Form(default='')):
        self.email = email
        self.password = password
        self.password_valid = password_valid
        self.name = name
        self.phone_number = phone_number

        # TODO: password validation 제대로 동작하는지 확인
        @validator('password_valid')
        def passwords_match(cls, v, values, **kwargs):
            if 'password_valid' in values and v != values['password']:
                raise ValueError('passwords do not match')
            return v


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
        orm_mode = True

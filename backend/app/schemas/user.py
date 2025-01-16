from pydantic import BaseModel, Field, EmailStr, SecretStr, model_validator, root_validator
from typing_extensions import Self
from enum import Enum


class GenderEnum(str, Enum):
    man = 'M'
    female = 'F'
    other = 'O'


class UserRegister(BaseModel):
    emp_id: str = Field(..., example='so22816')
    name: str = Field(..., example='김남곤')
    email: EmailStr = Field(..., example="example@example.com")
    password: SecretStr = Field(...)
    password_valid: SecretStr = Field(...)
    dept_id: str = Field(...)
    gender: GenderEnum = Field(...)

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_valid:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return self


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    user_id: str
    username: str
    email: str
    dept_id: str
    password: str
    gender: GenderEnum


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

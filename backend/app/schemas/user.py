from pydantic import BaseModel, Field, EmailStr, SecretStr, validator
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

    # TODO: password validation 제대로 동작하는지 확인
    @validator('password_valid')
    def passwords_match(cls, v, values, **kwargs):
        if 'password_valid' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


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

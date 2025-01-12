from pydantic import BaseModel
from enum import Enum


class GenderEnum(str, Enum):
    man = 'M'
    female = 'F'
    other = 'O'


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

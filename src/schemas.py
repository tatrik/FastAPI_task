import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator


class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    hashed_password: str
    created: datetime.datetime
    logged_in: datetime.datetime
    last_activity: datetime.datetime


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    password2: str

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("password don't match")
        return v


class Token(BaseModel):
    access_token: str
    token_type: str


class Login(BaseModel):
    email: EmailStr
    password: str

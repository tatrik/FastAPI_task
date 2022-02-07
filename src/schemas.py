import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserOut(UserBase):
    id: Optional[int] = None


class UserAct(UserOut):
    created: datetime.datetime
    logged_in: datetime.datetime
    last_activity: datetime.datetime


class User(UserAct):
    hashed_password: str


class UserIn(UserBase):
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


class BasePost(BaseModel):
    title: str
    description: str


class Post(BasePost):
    id: int
    user_id: int
    created: datetime.datetime


class PostIn(BasePost):
    pass


class BaseLike(BaseModel):
    id: int
    post_id: int
    user_id: int
    date: datetime.datetime


class Like(BaseLike):
    like: bool = True


class LikeIn(BaseModel):
    post_id: int
    like: bool = True


class UnLike(BaseLike):
    like: bool = False


class UnLikeIn(BaseModel):
    post_id: int
    like: bool = False


class Analytics(BaseModel):
    likes: int
    unlikes: int
    date: datetime.date

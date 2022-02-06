from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas import User, UserIn, Token, Login
from src.repositories import UserRepository
from src.depends import get_user_repository, get_current_user
from src.security import verify_password, create_access_token

user_router = APIRouter()


@user_router.get("/", response_model=List[User])
async def read_users(
    users: UserRepository = Depends(get_user_repository),
    limit: int = 100,
    skip: int = 0
):
    return await users.get_all(limit=limit, skip=skip)


@user_router.post("/", response_model=User)
async def create_user(
    user: UserIn,
    users: UserRepository = Depends(get_user_repository)
):
    return await users.create_user(u=user)


@user_router.put("/", response_model=User)
async def update_user(
    id: int,
    user: UserIn,
    users: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user)
):
    old_user = await users.get_by_id(user_id=id)
    if old_user is None or old_user.email != current_user.email:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
    return await users.update_user(user_id=id, u=user)


auth_router = APIRouter()


@auth_router.post("/", response_model=Token)
async def login(
    login: Login,
    users: UserRepository = Depends(get_user_repository)
):
    user = await users.get_by_email(login.email)
    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return Token(
        access_token=create_access_token({"sub": user.email}),
        token_type="Bearer"
    )

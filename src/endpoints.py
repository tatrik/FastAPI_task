import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas import User, UserOut, UserAct, UserIn, Token, Login, Post, PostIn, Like, LikeIn, UnLike, UnLikeIn, Analytics
from src.repositories import UserRepository, PostRepository, LikeRepository
from src.depends import get_user_repository, get_current_user, get_post_repository, get_like_repository
from src.security import verify_password, create_access_token


user_router = APIRouter()


@user_router.get("/", response_model=List[UserOut])
async def read_users(
    users: UserRepository = Depends(get_user_repository),
    limit: int = 100,
    skip: int = 0
):
    return await users.get_all(limit=limit, skip=skip)


@user_router.get("/activity", response_model=List[UserAct])
async def read_users(
    users: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user),
    limit: int = 100,
    skip: int = 0
):
    await users.update_activity(id=current_user.id)
    return await users.get_all(limit=limit, skip=skip)


@user_router.post("/", response_model=UserOut)
async def create_user(
    user: UserIn,
    users: UserRepository = Depends(get_user_repository)
):
    return await users.create_user(u=user)


@user_router.put("/", response_model=UserOut)
async def update_user(
    id: int,
    user: UserIn,
    users: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user)
):
    old_user = await users.get_by_id(user_id=id)
    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
    await users.update_activity(id=current_user.id)
    return await users.update_user(user_id=id, u=user)


@user_router.delete("/")
async def delete_user(
    id: int,
    users: UserRepository = Depends(get_user_repository),
    current_user: User = Depends(get_current_user)
):
    user = await users.get_by_id(user_id=id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    elif user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not correct user")
    await users.delete_user(user_id=id)
    return {"status": True}


auth_router = APIRouter()


@auth_router.post("/", response_model=Token)
async def login(
    login: Login,
    users: UserRepository = Depends(get_user_repository)
):
    user = await users.get_by_email(login.email)
    if user is None or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    await users.update_login_time(login.email)
    return Token(
        access_token=create_access_token({"sub": user.email}),
        token_type="Bearer"
    )


post_router = APIRouter()


@post_router.get("/", response_model=List[Post])
async def read_posts(
    posts: PostRepository = Depends(get_post_repository),
    limit: int = 100,
    skip: int = 0
):
    return await posts.get_posts(limit=limit, skip=skip)


@post_router.post("/", response_model=Post)
async def create_post(
    post: PostIn,
    posts: PostRepository = Depends(get_post_repository),
    current_user: User = Depends(get_current_user),
    users: UserRepository = Depends(get_user_repository)
):
    await users.update_activity(id=current_user.id)
    return await posts.create_post(user_id=current_user.id, p=post)


@post_router.put("/", response_model=Post)
async def update_post(
    id: int,
    post: PostIn,
    posts: PostRepository = Depends(get_post_repository),
    current_user: User = Depends(get_current_user),
    users: UserRepository = Depends(get_user_repository)
):
    old_post = await posts.get_by_id(id=id)
    if old_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    elif old_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    await users.update_activity(id=current_user.id)
    return await posts.update_post(id=id, user_id=current_user.id, p=post)


@post_router.delete("/")
async def delete_post(
    id: int,
    posts: PostRepository = Depends(get_post_repository),
    current_user: User = Depends(get_current_user),
    users: UserRepository = Depends(get_user_repository)
):
    post = await posts.get_by_id(id=id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    elif post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    await posts.delete_post(post_id=id)
    await users.update_activity(id=current_user.id)
    return {"status": True}


like_router = APIRouter()


@like_router.post("/create_like", response_model=Like)
async def create_like(
    like: LikeIn,
    likes: LikeRepository = Depends(get_like_repository),
    current_user: User = Depends(get_current_user),
    users: UserRepository = Depends(get_user_repository)
):
    await users.update_activity(id=current_user.id)
    return await likes.create_like(user_id=current_user.id, l=like)


@like_router.post("/create_unlike", response_model=UnLike)
async def create_unlike(
    id: int,
    unlike: UnLikeIn,
    likes: LikeRepository = Depends(get_like_repository),
    current_user: User = Depends(get_current_user),
    users: UserRepository = Depends(get_user_repository)
):
    like = await likes.get_by_id(id=id)
    if like is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    elif like.user_id != current_user.id or like.post_id != unlike.post_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    await users.update_activity(id=current_user.id)
    return await likes.create_unlike(id=id, user_id=current_user.id, l=unlike)


@like_router.get("/analytics", response_model=List[Analytics])
async def read_likes(
    likes: LikeRepository = Depends(get_like_repository),
    date_from: str = datetime.date.today(),
    date_to: str = datetime.date.today()
):
    return await likes.get_analytics(date_from=date_from, date_to=date_to)

import datetime

from src.queries import query_sql
from src.models import users, posts, likes
from databases import Database
from typing import Optional, List, Mapping
from src.schemas import User, UserIn, Post, PostIn, Like, LikeIn, UnLikeIn, UnLike, UserOut
from src.security import hash_password


class BaseRepository:
    def __init__(self, database: Database):
        self.database = database


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Mapping]:
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        query = users.select().where(users.c.id == user_id)
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create_user(self, u: UserIn) -> UserOut:
        user = User(
            id=0,
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            created=datetime.datetime.utcnow(),
            logged_in=datetime.datetime.utcnow(),
            last_activity=datetime.datetime.utcnow(),
        )

        values = {**user.dict()}
        values.pop("id", None)
        query = users.insert().values(**values)
        user.id = await self.database.execute(query)
        return user

    async def update_user(self, user_id: int, u: UserIn) -> UserOut:
        user = User(
            id=user_id,
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            created=datetime.datetime.utcnow(),
            logged_in=datetime.datetime.utcnow(),
            last_activity=datetime.datetime.utcnow(),
        )

        values = {**user.dict()}
        print(values)
        values.pop("created", None)
        values.pop("logged_in", None)
        values.pop("id", None)
        query = users.update().where(users.c.id == user_id).values(**values)
        await self.database.execute(query)
        return user

    async def update_login_time(self, email: str):
        new_time = datetime.datetime.utcnow()
        query = users.update().where(users.c.email == email).values(logged_in=new_time, last_activity=new_time )
        return await self.database.execute(query)

    async def update_activity(self, id: int):
        query = users.update().where(users.c.id == id).values(last_activity=datetime.datetime.utcnow())
        return await self.database.execute(query)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def delete_user(self, user_id: int):
        query = users.delete().where(users.c.id == user_id)
        return await self.database.execute(query)


class PostRepository(BaseRepository):

    async def create_post(self, user_id: Optional[str], p: PostIn) -> Post:
        post = Post(
            id=0,
            user_id=user_id,
            title=p.title,
            description=p.description,
            created=datetime.datetime.utcnow()
        )
        values = {**post.dict()}
        values.pop("id", None)
        query = posts.insert().values(**values)
        post.id = await self.database.execute(query)
        return post

    async def update_post(self, id: int, user_id: Optional[str], p: PostIn) -> Post:
        post = Post(
            id=id,
            user_id=user_id,
            title=p.title,
            description=p.description,
            created=datetime.datetime.utcnow(),
        )

        values = {**post.dict()}
        values.pop("created", None)
        values.pop("id", None)
        query = posts.update().where(posts.c.id == id).values(**values)
        await self.database.execute(query)
        return post

    async def get_posts(self, limit: int = 100, skip: int = 0) -> List[Mapping]:
        query = posts.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def delete_post(self, post_id: int) -> dict:
        query = posts.delete().where(posts.c.id == post_id)
        return await self.database.execute(query)

    async def get_by_id(self, id: int) -> Optional[Post]:
        query = posts.select().where(posts.c.id == id)
        post = await self.database.fetch_one(query=query)
        if post is None:
            return None
        return Post.parse_obj(post)


class LikeRepository(BaseRepository):

    async def create_like(self, user_id: int, l: LikeIn) -> Like:
        like = Like(
            id=0,
            post_id=l.post_id,
            user_id=user_id,
            like=l.like,
            date=datetime.datetime.utcnow(),
        )
        values = {**like.dict()}
        values.pop("id", None)
        query = likes.insert().values(**values)
        like.id = await self.database.execute(query)
        return like

    async def create_unlike(self, id: int, user_id: int, l: UnLikeIn) -> UnLike:
        unlike = UnLike(
            id=0,
            post_id=l.post_id,
            user_id=user_id,
            like=l.like,
            date=datetime.datetime.utcnow(),
        )
        values = {**unlike.dict()}
        values.pop("id", None)
        query = likes.insert().values(**values)
        unlike.id = await self.database.execute(query)
        return unlike

    async def get_by_id(self, id: int) -> Optional[Like]:
        query = likes.select().where(likes.c.id == id)
        like = await self.database.fetch_one(query=query)
        if like is None:
            return None
        return Like.parse_obj(like)

    async def get_analytics(self, date_from: str, date_to: str) -> List[Mapping]:
        query = query_sql(date_from=date_from, date_to=date_to)
        return await self.database.fetch_all(query=query)

    async def get_likes(self, limit: int = 100, skip: int = 0) -> List[Mapping]:
        query = likes.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

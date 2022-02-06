import datetime

from src.models import users, posts, likes
from databases import Database
from typing import Optional, List, Mapping
from src.schemas import User, UserIn
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

    async def create_user(self, u: UserIn) -> User:
        user = User(
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

    async def update_user(self, user_id: int, u: UserIn) -> User:
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
        values.pop("created", None)
        values.pop("id", None)
        query = users.update().where(users.c.id == user_id).values(**values)
        await self.database.execute(query)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def delete_user(self, user_id: int) -> dict:
        query = users.delete().where(users.c.id == user_id)
        await self.database.execute(query)
        return {"success": True}

from sqlalchemy import Integer, Table, Column, String, DateTime, ForeignKey, Boolean
from src.db import metadata
import datetime

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False, unique=True),
    Column("hashed_password", String, nullable=False),
    Column("created", DateTime, default=datetime.datetime.utcnow),
    Column("logged_in", DateTime, default=datetime.datetime.utcnow),
    Column("last_activity", DateTime, default=datetime.datetime.utcnow),
)

posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("title", String, nullable=False),
    Column("description", String, nullable=False),
    Column("created", DateTime, default=datetime.datetime.utcnow),
)

likes = Table(
    "likes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("post_id", Integer, ForeignKey("posts.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("like", Boolean, nullable=False),
    Column("date", DateTime, default=datetime.datetime.utcnow),
)

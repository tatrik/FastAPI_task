from sqlalchemy import Table, Column, String, INTEGER, DateTime, ForeignKey, Boolean
from src.db import metadata
import datetime

users = Table(
    "users",
    metadata,
    Column("id", INTEGER, primary_key=True, autoincrement=True, unique=True),
    Column("name", String(32), nullable=False),
    Column("email", String(64), nullable=False, unique=True),
    Column("hashed_password", String(64), nullable=False),
    Column("created", DateTime, default=datetime.datetime.utcnow),
    Column("logged_in", DateTime, default=datetime.datetime.utcnow),
    Column("last_activity", DateTime, default=datetime.datetime.utcnow),
)

posts = Table(
    "posts",
    metadata,
    Column("id", INTEGER, primary_key=True, autoincrement=True, unique=True),
    Column("user_id", INTEGER, ForeignKey("users.id"), nullable=False),
    Column("title", String(64), nullable=False),
    Column("description", String(350), nullable=False),
    Column("created", DateTime, default=datetime.datetime.utcnow),
)

likes = Table(
    "likes",
    metadata,
    Column("id", INTEGER, primary_key=True, autoincrement=True, unique=True),
    Column("post_id", INTEGER, ForeignKey("posts.id"), nullable=False),
    Column("user_id", INTEGER, ForeignKey("users.id"), nullable=False),
    Column("like", Boolean, nullable=False),
    Column("date", DateTime, default=datetime.datetime.utcnow),
)

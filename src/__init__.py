from src.models import users, posts
from src.db import metadata, engine

metadata.create_all(bind=engine)

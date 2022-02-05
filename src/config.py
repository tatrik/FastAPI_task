from starlette.config import Config

config = Config(".venv")

DATABASE_URL = config("MY_DATABASE_URL", cast=str, default="")

from starlette.config import Config

config = Config(".venv")

DATABASE_URL = config("SN_DATABASE_URL", cast=str, default="")
SECRET_KEY = config("SN_SECRET_KEY", cast=str, default="c46f8c49d52b2c09bdffed1145e8c1db8a394f1eba0608a382dd5c780bcf1a48")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

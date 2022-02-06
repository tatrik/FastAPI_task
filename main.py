import uvicorn
from fastapi import FastAPI
from src.db import database
from src import endpoints
# import sys
# import os
#
#
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))

app = FastAPI(title="Social Network Task")
app.include_router(endpoints.user_router, prefix="/users", tags=["users"])
app.include_router(endpoints.auth_router, prefix="/auth", tags=["auth"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)

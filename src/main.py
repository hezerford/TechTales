from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

import uvicorn
import sys
import os
from auth.database import create_db_and_tables

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.auth.schemas import UserCreate, UserRead
from src.auth.manager import get_user_manager
from src.auth.models import User
from src.auth.utils import auth_backend

# Подключаем роутеры
from src.articles.router import router as article_router
from src.mailing.router import router as mailing_router
from src.api.articles.router import router as api_articles_router
from src.api.comments.router import router as api_comments_router

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(
    title="TechTales",
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(article_router, prefix="")
app.include_router(mailing_router, prefix="")
app.include_router(api_articles_router, prefix="/api")
app.include_router(api_comments_router, prefix="/api")

@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
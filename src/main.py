from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Подключаем роутеры
from src.articles.router import router as article_router
from src.mailing.router import router as mailing_router
from src.api.articles.router import router as api_articles_router
from src.api.comments.router import router as api_comments_router

app = FastAPI(
    title="TechTales",
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(article_router, prefix="")
app.include_router(mailing_router, prefix="")
app.include_router(api_articles_router, prefix="/api")
app.include_router(api_comments_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
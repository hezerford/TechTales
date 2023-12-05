from fastapi import FastAPI
from src.blog.router import router as article_router
import uvicorn

app = FastAPI(
    title="TechTales"
)

# Подключаем роутеры
app.include_router(article_router, prefix="/articles")

# Другие роутеры и настройки могут быть добавлены здесь

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
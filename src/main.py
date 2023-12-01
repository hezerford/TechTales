from fastapi import FastAPI
from blog.router import router as article_router
from database import init_mongo, close_mongo_connection

app = FastAPI(
    title="TechTales"
)

@app.on_event("startup")
async def startup_db_client():
    await init_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Подключаем роутеры
app.include_router(article_router, prefix="/api/v1")

# Другие роутеры и настройки могут быть добавлены здесь

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
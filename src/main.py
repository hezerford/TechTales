from contextlib import asynccontextmanager
from fastapi import FastAPI
from blog.router import router as article_router
from database import init_mongo, close_mongo_connection, create_test_data
import asyncio

app = FastAPI(
    title="TechTales"
)

'''
Устарело ;

@app.on_event("startup")
async def startup_db_client():
    await init_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
'''


@asynccontextmanager
async def lifespan():
    try:
        await init_mongo()
    finally:
        await close_mongo_connection()


# Подключаем роутеры
app.include_router(article_router, prefix="/api/v1")

# Другие роутеры и настройки могут быть добавлены здесь

async def main():
    await init_mongo()
    await create_test_data()

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
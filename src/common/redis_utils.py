import redis
from .settings import REDIS_URL

async def get_redis() -> redis.Redis:
    redis_instance = redis.Redis.from_url("redis://localhost", encoding="utf-8")
    try:
        yield redis_instance
    finally:
        redis_instance.close()
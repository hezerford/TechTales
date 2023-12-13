from decouple import config

REDIS_URL = config("REDIS_URL", default="redis://localhost")
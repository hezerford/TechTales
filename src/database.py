from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

MONGODB_URL = f"mongodb+srv://{config('MONGODB_USER')}:{config('MONGODB_PASS')}@cluster0.qdjlej8.mongodb.net/your_database_name?retryWrites=true&w=majority"

class Database:
    def __init__(self):
        self.client = None
        self.db = None

database = Database()

async def connect_to_mongo():
    database.client = AsyncIOMotorClient(MONGODB_URL)
    database.db = database.client.get_database()

async def close_mongo_connection():
    database.client.close()

async def init_mongo():
    await connect_to_mongo()
    await close_mongo_connection()
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

MONGODB_URL=f"mongodb+srv://{config('MONGODB_USER')}:{config('MONGODB_PASS')}@{config('MONGODB_URL')}/?retryWrites=true&w=majority"

client = AsyncIOMotorClient(MONGODB_URL)
db = client.get_database("TechTales")
blog_collection = db.get_collection("Blog")
subscribers_collection = db.get_collection("Subscribers")
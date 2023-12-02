import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from blog.schemas import ArticleSchema, CommentSchema
from pymongo import MongoClient

MONGODB_URI = f"mongodb+srv://{config('MONGODB_USER')}:{config('MONGODB_PASS')}@cluster0.qdjlej8.mongodb.net/your_database_name?retryWrites=true&w=majority"

class Database:
    def __init__(self):
        self.client = None
        self.db = None

database = Database()

async def connect_to_mongo():
    database.client = AsyncIOMotorClient(MONGODB_URI)
    database.db = database.client.get_database('Cluster0')

async def close_mongo_connection():
    database.client.close()

async def init_mongo():
    await connect_to_mongo()
    await close_mongo_connection()

client = MongoClient(MONGODB_URI)

db = client.sample_guides
coll = db.Articles

coll.drop()

test_data = [
    {"title": "Test 1", "content": "Some test content 1", "views": 0, "likes": 0, "comments": [], "publication_date": datetime.now().date(), "description": "Some test description 1"},
    {"title": "Test 2", "content": "Some test content 2", "views": 1, "likes": 1, "comments": [], "publication_date": datetime.now().date(), "description": "Some test description 2"}
]

result = coll.insert_many(test_data)

print(result.inserted_ids)

client.close()

async def create_article(article: ArticleSchema):
    # Преобразуем Pydantic-модель в словарь, исключив поле "id"
    article_dict = article.dict(exclude={"id"})
    
    # Добавляем текущее время публикации
    article_dict["publication_date"] = datetime.utcnow()

    # Вставляем запись в коллекцию "articles" и получаем идентификатор вставки
    result = await database.db.articles.insert_one(article_dict)

    # Возвращаем идентификатор
    return str(result.inserted_id)

async def get_articles():
    # Находим все статьи в коллекции "articles"
    articles = await database.db.articles.find().to_list(100)

    # Возвращаем список статей
    return articles

async def get_article(article_id: str):
    # Находим статью по идентификатору в коллекции "articles"
    article = await database.db.articles.find_one({"_id": ObjectId(article_id)})
    # Возвращаем найденную статью
    return article

async def create_comment(article_id: str, comment: CommentSchema):
    # Преобразуем Pydantic-модель в словарь, исключив поле "id"
    comment_dict = comment.dict(exclude={"id"})

    # Добавить текущее время публикации комментария
    comment_dict["timestamp"] = datetime.utcnow()
    
    # Ассинхронно обновляем статью в коллекции "articles", добавив комментарий
    result = await database.db.articles.update_one(
        # Указываем какой документ обновить по идентификатору
        {"_id": ObjectId(article_id)},
        # Оператором push добавляем элеммент в массив
        {"$push": {"comments": comment_dict}}
    )

    # Вернуть строковое представление идентификатора комментария
    return str(comment_dict["id"])

async def get_comments(article_id: str):
    article = await database.db.articles.find_one({"_id": ObjectId(article_id)})
    if article:
        return article.get("comments", [])
    return []
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from database import database, connect_to_mongo, close_mongo_connection
from blog.schemas import CommentSchema, ArticleSchema
from bson import ObjectId
from typing import List

router = APIRouter()

@router.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@router.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@router.get("/articles", response_model=List[ArticleSchema])
async def get_articles():
    articles = await database.db.articles.find().to_list(100)
    return articles

@router.post("/articles", response_model=ArticleSchema)
async def create_article(article: ArticleSchema):
    article_dict = article.dict()
    article_id = await database.db.articles.insert_one(article_dict)
    return {**article_dict, "id": str(article_id.inserted_id)}

@router.get("/articles/{article_id}", response_model=ArticleSchema)
async def get_article(article_id: str):
    article = await database.db.articles.find_one({"_id": ObjectId(article_id)})
    if article:
        return article
    raise HTTPException(status_code=404, detail="Article not found")

@router.post("/articles/{article_id}/comments", response_model=CommentSchema)
async def create_comment(article_id: str, comment: CommentSchema):
    comment_dict = comment.dict()
    await database.db.articles.update_one(
        {"_id": ObjectId(article_id)},
        {"$push": {"comments": comment_dict}}
    )
    return {**comment_dict, "id": str(comment_dict["id"])}
from contextlib import asynccontextmanager
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from database import database, connect_to_mongo, close_mongo_connection
from blog.schemas import CommentSchema, ArticleSchema
from bson import ObjectId
from typing import List

router = APIRouter()

@asynccontextmanager
async def lifespan():
    await connect_to_mongo()

'''
Устарело
@router.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@router.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
'''

from fastapi import APIRouter, Depends
from fastapi.openapi.models import Response
from fastapi.responses import JSONResponse
from blog.schemas import ArticleSchema, CommentSchema
from database import create_article, get_articles, get_article, create_comment, get_comments

router = APIRouter()

@router.post("/articles/", response_model=ArticleSchema)
async def create_article_route(article: ArticleSchema):
    article_id = await create_article(article)
    return JSONResponse(content={"article_id": article_id}, status_code=201)

@router.get("/articles/", response_model=ArticleSchema)
async def get_articles_route():
    articles = await get_articles()
    return JSONResponse(content={"data": articles}, status_code=200)

@router.get("/articles/{article_id}/", response_model=ArticleSchema)
async def get_article_route(article_id: str):
    article = await get_article(article_id)
    if article:
        return JSONResponse(content={"data": article}, status_code=200)
    return JSONResponse(content={"message": "Article not found"}, status_code=404)

@router.post("/articles/{article_id}/comments/", response_model=CommentSchema)
async def create_comment_route(article_id: str, comment: CommentSchema):
    comment_id = await create_comment(article_id, comment)
    return JSONResponse(content={"comment_id": comment_id}, status_code=201)

@router.get("/articles/{article_id}/comments/", response_model=CommentSchema)
async def get_comments_route(article_id: str):
    comments = await get_comments(article_id)
    return JSONResponse(content={"data": comments}, status_code=200)
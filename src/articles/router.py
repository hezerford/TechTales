from bson import ObjectId
from pymongo import ReturnDocument
from src.articles.models import ArticleCollection, ArticleModel, UpdateArticleModel

from fastapi import APIRouter, Body, HTTPException, Request, Response, Depends
from fastapi.templating import Jinja2Templates
from src.database import blog_collection

router = APIRouter(tags=["Articles"])

templates = Jinja2Templates(directory="src/templates")

@router.get("/", response_description="List all articles", response_model=ArticleCollection)
async def list_articles(request: Request):
    articles = await blog_collection.find().to_list(10)
    return templates.TemplateResponse(name="index.html", context={"request": request, "articles": articles})


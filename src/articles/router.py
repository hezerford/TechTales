from cachetools import TTLCache
import redis
from bson import ObjectId
from fastapi.responses import HTMLResponse
import httpx
from comments.models import CommentModel
from src.articles.models import ArticleCollection, ArticleModel
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from src.database import blog_collection
from src.common.redis_utils import get_redis
from decouple import config

templates = Jinja2Templates(directory="src/templates")

router = APIRouter(tags=["Articles"])

@router.get("/", response_description="List all articles", response_model=ArticleCollection)
async def list_articles(request: Request):
    articles = await blog_collection.find().to_list(10)
    return templates.TemplateResponse(name="index.html", context={"request": request, "articles": articles})

article_cache = TTLCache(maxsize=256, ttl=30)

@router.get("/{article_id}", response_model=ArticleModel, response_description="Show an article by ID")
async def show_article(article_id: str, request: Request, redis: redis.Redis = Depends(get_redis)):
    cached_article = article_cache.get(article_id)

    if cached_article:
        return templates.TemplateResponse(name="article.html", context={"request": request, "article": cached_article})

    article = await blog_collection.find_one({"_id": ObjectId(article_id)})

    if article:
        article_cache[article_id] = article
        return templates.TemplateResponse(name="article.html", context={"request": request, "article": article})

    raise HTTPException(status_code=404, detail="Article not found")

async def verify_recaptcha(g_recaptcha_response: str):
    recaptcha_secret_key = config("CAPTCHA_SECRET_KEY")
    verify_url = f"https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': recaptcha_secret_key,
        'response': g_recaptcha_response,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(verify_url, data=params)

    data = response.json()

    if data["success"] == True:
        raise HTTPException(status_code=400, detail="reCAPTCHA verification failed")

@router.post("/{article_id}", response_class=HTMLResponse)
async def add_comment(
    article_id: str,
    request: Request,
    g_recaptcha_response: str = Form(None),
    username: str = Form(...),
    comment: str = Form(...),
):
    await verify_recaptcha(g_recaptcha_response)

    comment_model = CommentModel(username=username, content=comment)
    comment_dict = comment_model.model_dump(by_alias=True)

    await blog_collection.update_one(
        {"_id": ObjectId(article_id)},
        {"$push": {"comments": comment_dict}}
    )

    article = await blog_collection.find_one({"_id": ObjectId(article_id)})
    if article:
        return templates.TemplateResponse(name="article.html", context={"request": request, "article": article})
    raise HTTPException(status_code=404, detail="Article not found")
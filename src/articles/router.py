import redis
from bson import ObjectId
from fastapi.responses import HTMLResponse

from src.articles.utils import update_article_cache, verify_recaptcha, get_template_context
from src.comments.models import CommentModel
from src.articles.models import ArticleCollection, ArticleModel
from src.database import blog_collection
from src.common.redis_utils import get_redis

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Form
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="src/templates")

router = APIRouter(tags=["Articles"])

@router.get("/", response_description="List all articles", response_model=ArticleCollection)
async def list_articles(request: Request, template_context: dict = Depends(get_template_context)):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, **template_context},
    )

from src.articles.utils import article_cache

@router.get("/articles/{article_id}", response_model=ArticleModel, response_description="Show an article by ID")
async def show_article(article_id: str, request: Request, page: int = Query(1, alias="page"), redis: redis.Redis = Depends(get_redis)):
    article_key = f"{article_id}_page_{page}"
    # Пытаемся получить кэшированную страницу
    cached_article = article_cache.get(article_key)

    article = cached_article or await blog_collection.find_one({"_id": ObjectId(article_id)})

    if article:
        # Добавляем пагинацию к комментариям
        comments = article["comments"]
        comments_per_page = 10
        total_comments = len(comments)
        total_pages = (total_comments + comments_per_page - 1) // comments_per_page

        # Разделение комментариев на страницы
        start_idx = (page - 1) * comments_per_page
        end_idx = start_idx + comments_per_page
        paginated_comments = comments[start_idx:end_idx]

        # Если страница не в кэше, добавляем ее
        if not cached_article:
            article_cache[article_key] = article

        return templates.TemplateResponse(
            name="article.html", 
            context={
                "request": request, 
                "article": article,
                "paginated_comments": paginated_comments,
                "total_pages": total_pages,
                "current_page": page,
            },
        )

    raise HTTPException(status_code=404, detail="Article not found")

@router.post("/articles/{article_id}", response_class=HTMLResponse)
async def add_comment(
    article_id: str,
    request: Request,
    g_recaptcha_response: str = Form(None),
    username: str = Form(...),
    comment: str = Form(...),
    page: int = Query(1, alias="page"),
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
        # Получаем обновленные данные
        comments = article.get("comments", [])
        comments_per_page = 10
        total_comments = len(comments)
        total_pages = (total_comments + comments_per_page - 1) // comments_per_page

        # Обновляем кэш для всех страниц
        for page_num in range(1, total_pages + 1):
            start_idx = (page_num - 1) * comments_per_page
            end_idx = start_idx + comments_per_page
            paginated_comments = comments[start_idx:end_idx]
            
            await update_article_cache(article_id, paginated_comments, total_comments, total_pages)

        # Передаем total_pages в контекст
        return templates.TemplateResponse(
            name="article.html", 
            context={
                "request": request, 
                "article": article,
                "total_pages": total_pages,
                "paginated_comments": paginated_comments,  # Используем переменную из последней итерации
                "current_page": total_pages,
            },
        )

    raise HTTPException(status_code=404, detail="Article not found")

@router.get("/search/", response_description="Search articles by title")
async def search_articles(request: Request, query: str = Query(...), page: int = Query(1, alias="page")):
    # Размер страницы со статьями (сколько статей на одну страницу)
    page_size = 10

    offset = (page - 1) * page_size
    
    regex_query = {"$regex": query, "$options": "i"}
    articles = await blog_collection.find({"title": regex_query}).skip(offset).limit(page_size).to_list(page_size)

    return templates.TemplateResponse(
        name="searched_articles.html",
        context={
            "request": request,
            "articles": articles,
            "query": query,
            "page": page,
        }
    )
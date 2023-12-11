from bson import ObjectId
from fastapi.responses import HTMLResponse
from comments.models import CommentModel
from src.articles.models import ArticleCollection, ArticleModel

from fastapi import APIRouter,  HTTPException, Request,  Form
from fastapi.templating import Jinja2Templates
from src.database import blog_collection

router = APIRouter(tags=["Articles"])

templates = Jinja2Templates(directory="src/templates")

@router.get("/", response_description="List all articles", response_model=ArticleCollection)
async def list_articles(request: Request):
    articles = await blog_collection.find().to_list(10)
    return templates.TemplateResponse(name="index.html", context={"request": request, "articles": articles})

@router.get("/{article_id}", response_model=ArticleModel, response_description="Show an article by ID")
async def show_article(article_id: str, request: Request):
    article = await blog_collection.find_one({"_id": ObjectId(article_id)})
    if article:
        return templates.TemplateResponse(name="article.html", context={"request": request, "article": article})
    raise HTTPException(status_code=404, detail="Article not found")

@router.post("/{article_id}", response_class=HTMLResponse)
async def add_comment(
    article_id: str,
    request: Request,
    username: str = Form(...),
    comment: str = Form(...),
):  
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
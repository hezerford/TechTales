from decouple import config
from fastapi import HTTPException, Query
import httpx
from src.database import blog_collection

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
    
async def calculate_total_pages():
    total_articles = await blog_collection.count_documents({})
    articles_per_page = 10
    return (total_articles + articles_per_page - 1) // articles_per_page

async def get_template_context(page: int = Query(1, alias="page")):
    articles_per_page = 10
    skip_articles = (page - 1) * articles_per_page
    articles = await blog_collection.find().skip(skip_articles).to_list(articles_per_page)
    total_pages = await calculate_total_pages()

    return {"articles": articles, "total_pages": total_pages, "current_page": page}

from cachetools import TTLCache

COMMENTS_PER_PAGE = 10
article_cache = TTLCache(maxsize=256, ttl=30)

async def update_article_cache(article_id: str, comments: list, total_comments: int, total_pages: int) -> None:
    for page_num in range(1, total_pages + 1):
        start_idx = (page_num - 1) * COMMENTS_PER_PAGE
        end_idx = start_idx + COMMENTS_PER_PAGE
        paginated_comments = comments[start_idx:end_idx]

        cached_article = article_cache.get(f"{article_id}_page_{page_num}")
        if cached_article:
            cached_article["comments"] = paginated_comments
            cached_article["total_comments"] = total_comments
            cached_article["total_pages"] = total_pages
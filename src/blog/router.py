from bson import ObjectId
from pymongo import ReturnDocument
from blog.models import ArticleCollection, ArticleModel, UpdateArticleModel

from fastapi import APIRouter, Body, HTTPException, Response
from database import blog_collection

router = APIRouter()

@router.get("/", response_description="List all articles", response_model=ArticleCollection)
async def list_articles():
    return ArticleCollection(articles=await blog_collection.find().to_list(10))

@router.post("/", response_model=ArticleModel, response_description="Add new article")
async def create_article(article: ArticleModel = Body(...)):
    new_article = await blog_collection.insert_one(
        article.model_dump(by_alias=True, exclude=["id"])
    )
    created_article = await blog_collection.find_one(
        {"_id": new_article.inserted_id}
    )

    return created_article

@router.get("/{id}", response_description="Get a single article", response_model=ArticleModel, response_model_by_alias=False)
async def show_article(id: str):
    if (
        article := await blog_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return article
    
    raise HTTPException(status_code=404, detail=f"Article {id} not found")

@router.patch("/{id}", response_description="Update a article", response_model=ArticleModel, response_model_by_alias=False)
async def update_article(id: str, article: UpdateArticleModel = Body(...)):
    article = {
        k: v for k, v in article.model_dump(by_alias=True).items() if v is not None
    }

    if len(article) >= 1:
        update_result = await blog_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": article},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Article {id} not found")
        
    if (existing_article := await blog_collection.find_one({"_id": id})) is not None:
        return existing_article

    return HTTPException(status_code=404, detail=f"Article {id} not found")

@router.delete("/{id}", response_description="Delete a article")
async def delete_article(id: str):
    delete_result = await blog_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=204)
    
    raise HTTPException(status_code=404, detail=f"Student {id} not found")
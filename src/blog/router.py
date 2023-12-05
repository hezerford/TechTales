from bson import ObjectId
from pymongo import ReturnDocument
from src.blog.models import ArticleCollection, ArticleModel, CommentModel, UpdateArticleModel, UpdateCommentModel

from fastapi import APIRouter, Body, HTTPException, Response
from src.database import blog_collection

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

@router.post("/{id}/comments/", response_model=ArticleModel, response_model_by_alias=False)
async def add_comment(id: str, comment: CommentModel = Body(...)):
    if (article := await blog_collection.find_one({"_id": ObjectId(id)})) is not None:
        comment_dict = comment.model_dump(by_alias=True, exclude=["id"])
        comment_dict["_id"] = ObjectId()
        await blog_collection.update_one(
            {"_id": ObjectId(id)},
            {"$push": {"comments": comment_dict}}
        )
        updated_article = await blog_collection.find_one({"_id": ObjectId(id)})
        return updated_article
    
    raise HTTPException(status_code=404, detail=f"Article {id} not found")

@router.patch("/{id}/comments/{comment_id}", response_model=ArticleModel, response_model_by_alias=False)
async def update_comment(id: str, comment_id: str, update_comment: UpdateCommentModel = Body(...)):
    if (
        article := await blog_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        await blog_collection.update_one(
            {"_id": ObjectId(id), "comments._id": ObjectId(comment_id)},
            {"$set": {"comments.$.content": update_comment.content}}
        )
        updated_article = await blog_collection.find_one({"_id": ObjectId(id)})
        return updated_article

    raise HTTPException(status_code=404, detail=f"Article {id} not found")

@router.delete("/{id}/comments/{comment_id}", response_model=ArticleModel, response_model_by_alias=False)
async def delete_comment(id: str, comment_id: str):
    if (
        article := await blog_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        await blog_collection.update_one(
            {"_id": ObjectId(id)},
            {"$pull": {"comments": {"_id": ObjectId(comment_id)}}}
        )
        updated_article = await blog_collection.find_one({"_id": ObjectId(id)})
        return updated_article
    
    raise HTTPException(status_code=404, detail=f"Article {id} is not found")
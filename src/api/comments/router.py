from bson import ObjectId
from src.articles.models import ArticleModel, CommentModel, UpdateCommentModel

from fastapi import APIRouter, Body, HTTPException
from src.database import blog_collection

router = APIRouter(tags=["API Comments"]) 

@router.post("/comments/{id}", response_model=ArticleModel, response_model_by_alias=False)
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

@router.patch("/comments/{id}/{comment_id}", response_model=ArticleModel, response_model_by_alias=False)
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

@router.delete("/comments/{id}/{comment_id}", response_model=ArticleModel, response_model_by_alias=False)
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
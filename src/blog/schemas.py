from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
class CommentSchema(BaseModel):
    id: int
    username: str
    content: str
    timestamp: datetime

class ArticleSchema(BaseModel):
    id: int
    title: str
    content: str
    views: int
    likes: int
    comments: List[CommentSchema]
    publication_date: datetime
    description: str
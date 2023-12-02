from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class CommentSchema(BaseModel):
    id: int
    username: str
    content: str
    timestamp: datetime = datetime.now()

class ArticleSchema(BaseModel):
    id: int
    title: str
    content: str
    views: int = 0
    likes: int = 0
    comments: List[CommentSchema] = []
    publication_date: datetime = datetime.now().date()
    description: str = ""
from pydantic import BaseModel
from datetime import datetime
from typing import List

class Comment(BaseModel):
    username: str
    content: str
    timestamp: datetime = datetime.now()

class Article(BaseModel):
    title: str
    content: str
    views: int = 0
    likes: int = 0
    comments: List[Comment] = []
    publication_date: datetime = datetime.now()
    description: str = ""
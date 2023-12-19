from pydantic import BaseModel, BeforeValidator, Field
from datetime import datetime
from typing import Annotated, List, Optional

from src.comments.models import CommentModel

PyObjectId = Annotated[str, BeforeValidator(str)]

class ArticleModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field('...', max_length=100)
    description: str = Field('...', max_length=500)
    content: str = Field('...')
    views: int = 0
    likes: int = 0
    comments: List[CommentModel] = []
    publication_date: datetime

class UpdateArticleModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    
class ArticleCollection(BaseModel):
    articles: List[ArticleModel]
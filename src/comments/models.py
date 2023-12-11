from pydantic import BaseModel, BeforeValidator, Field
from datetime import datetime
from typing import Annotated, Optional

PyObjectId = Annotated[str, BeforeValidator(str)]

class CommentModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field('...', max_length=50)
    content: str = Field('...')
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, alias="timestamp")

class UpdateCommentModel(BaseModel):
    content: Optional[str] = None
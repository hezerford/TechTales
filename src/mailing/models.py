from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]

class SubscriberModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: str
    subscribed_at: datetime
from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]

class Subscriber(BaseModel):
    email: str

class SubscriberInDB(Subscriber):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    subscribed_at: datetime
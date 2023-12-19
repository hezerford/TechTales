from pydantic import BaseModel, EmailStr

class SubscriberForm(BaseModel):
    email: EmailStr
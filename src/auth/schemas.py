import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    password: str


class UserCreate(schemas.BaseUserCreate):
    username: str
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    username: str

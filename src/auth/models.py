from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Boolean, TIMESTAMP

from fastapi_users.db import SQLAlchemyBaseUserTableUUID

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
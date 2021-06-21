import uuid

from pizza_store.db.db import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(30), unique=True)
    email = Column(String(50), unique=True)
    password_hash = Column(String)
    role = Column(String(30))

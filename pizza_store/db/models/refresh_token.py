import uuid

from pizza_store.db.db import Base
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    token = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)

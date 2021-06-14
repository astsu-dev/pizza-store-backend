from pizza_store.db.db import Base
from sqlalchemy import Column, Integer, String


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

from pizza_store.db.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import CheckConstraint, ForeignKey


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(30), unique=True, nullable=False)
    weight = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    image = Column(String(80), nullable=False)

    __table_args__ = (
        CheckConstraint(weight > 0, name="check_weight_positive"),
        CheckConstraint(price >= 0, name="check_price_non_negative"),
    )

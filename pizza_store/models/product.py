from fastapi import UploadFile
from pydantic import BaseModel


class ProductBase(BaseModel):
    category_id: int
    name: str
    weight: int
    price: int


class ProductCreate(ProductBase):
    image: UploadFile


class Product(ProductBase):
    id: int
    image: str

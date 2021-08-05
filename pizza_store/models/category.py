from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str 
    

class Category(CategoryBase):
    """Product category model"""

    id: int


class CategoryCreate(CategoryBase):
    pass

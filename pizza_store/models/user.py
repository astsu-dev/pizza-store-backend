import datetime
import uuid

from pizza_store.enums.role import Role
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: uuid.UUID
    role: Role

    class Config:
        orm_mode = True


class UserInDB(User):
    password_hash: str


class UserInToken(User):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class Token(BaseModel):
    exp: datetime.datetime
    iat: datetime.datetime
    user: UserInToken

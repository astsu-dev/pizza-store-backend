from fastapi import Depends
from pizza_store.db.crud import CategoryCRUD, ProductCRUD, RefreshTokenCRUD, UserCRUD
from pizza_store.dependencies.db import get_session
from pizza_store.services import (
    AuthService,
    CategoryService,
    IAuthService,
    ICategoryService,
    IProductService,
    ProductService,
)
from sqlalchemy.ext.asyncio import AsyncSession


def get_auth_service(session: AsyncSession = Depends(get_session)) -> IAuthService:
    """Returns instance of auth service.

    Args:
        session (AsyncSession, optional): sqlalchemy session

    Returns:
        IAuthService
    """

    user_crud = UserCRUD()
    refresh_token_crud = RefreshTokenCRUD()
    return AuthService(session, user_crud, refresh_token_crud)


def get_category_service(
    session: AsyncSession = Depends(get_session),
) -> ICategoryService:
    """Returns instance of category service.

    Args:
        session (AsyncSession, optional): sqlalchemy session

    Returns:
        ICategoryService
    """

    category_crud = CategoryCRUD()
    return CategoryService(session, category_crud)


def get_product_service(
    session: AsyncSession = Depends(get_session),
) -> IProductService:
    """Returns instance of product service.

    Args:
        session (AsyncSession, optional): sqlalchemy session

    Returns:
        IProductService
    """

    product_crud = ProductCRUD()
    return ProductService(session, product_crud)

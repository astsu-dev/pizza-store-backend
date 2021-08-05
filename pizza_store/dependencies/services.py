from fastapi import Depends
from pizza_store.db.crud import RefreshTokenCRUD, UserCRUD
from pizza_store.dependencies.db import get_session
from pizza_store.services import AuthService, IAuthService
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

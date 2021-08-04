import datetime
import uuid
from typing import Optional, Protocol

from pizza_store.db.models import RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession


class IRefreshTokenCRUD(Protocol):
    """Has methods for getting, adding, deleting refresh tokens from db."""

    @classmethod
    async def get_refresh_token(
        cls, session: AsyncSession, token: uuid.UUID
    ) -> Optional[RefreshToken]:
        """Fetches refresh token by token.

        Args:
            session (AsyncSession): sqlalchemy session
            token (uuid.UUID)

        Returns:
            Optional[RefreshToken]: if None refresh token does not exist
        """

    @classmethod
    def add_refresh_token(
        cls,
        session: AsyncSession,
        user_id: uuid.UUID,
        token: uuid.UUID,
        expires_at: datetime.datetime,
    ) -> RefreshToken:
        """Creates refresh token model and adds to session.

        NOTE: Does not commit.

        Args:
            session (AsyncSession): sqlalchemy session
            user_id (uuid.UUID)
            token (uuid.UUID)
            expires_at (datetime.datetime): expiration datetime

        Returns:
            RefreshToken: token model
        """

    @classmethod
    async def delete_refresh_token(
        cls, session: AsyncSession, user_id: uuid.UUID
    ) -> None:
        """Deletes refresh token by user id.

        NOTE: Does not commit.

        Args:
            session (AsyncSession): sqlalchemy session
            user_id (uuid.UUID)
        """

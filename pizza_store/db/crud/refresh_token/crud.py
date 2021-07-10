import datetime
import uuid
from typing import Optional

from pizza_store.db.models import RefreshToken
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class RefreshTokenCRUD:
    """Has methods for getting, adding, deleting refresh tokens from db."""

    @classmethod
    async def get_refresh_token(
        cls, session: AsyncSession, user_id: uuid.UUID
    ) -> Optional[RefreshToken]:
        """Fetchs refresh token by user id.

        Example:
            >>> token = await RefreshTokenCRUD.get_refresh_token(session, user_id=uuid.UUID("x-x-x-x-x"))
            >>> token
            RefreshToken(user_id=uuid.UUID("x-x-x-x-x"), token=uuid.UUID("x-x-x-x-x"), expires_at=datetime.datetime(2021, 12, 12, 15))

        Args:
            session (AsyncSession): sqlalchemy session
            user_id (uuid.UUID)

        Returns:
            Optional[RefreshToken]: if None refresh token does not exist
        """

        stmt = select(RefreshToken).where(RefreshToken.user_id == user_id)
        res = await session.execute(stmt)

        return res.scalars().first()

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

        Example:
            >>> token = RefreshTokenCRUD.add_refresh_token(
                session,
                user_id=uuid.UUID("x-x-x-x-x"),
                token=uuid.UUID("x-x-x-x-x"),
                expires_at=datetime.datetime(2021, 12, 12, 15)
                )
            >>> await session.commit()
            >>> token
            RefreshToken(user_id=uuid.UUID("x-x-x-x-x"), token=uuid.UUID("x-x-x-x-x"), expires_at=datetime.datetime(2021, 12, 12, 15))

        Args:
            session (AsyncSession): sqlalchemy session
            user_id (uuid.UUID)
            token (uuid.UUID)
            expires_at (datetime.datetime): expiration datetime

        Returns:
            RefreshToken: token model
        """

        refresh_token = RefreshToken(
            user_id=user_id, token=token, expires_at=expires_at
        )
        session.add(refresh_token)

        return refresh_token

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

        stmt = delete(RefreshToken).where(RefreshToken.user_id == user_id)
        await session.execute(stmt)

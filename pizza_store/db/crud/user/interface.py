import uuid
from typing import Optional, Protocol

from pizza_store.db.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


class IUserCRUD(Protocol):
    """Has methods for getting, adding, deleting users from db."""

    @classmethod
    def add_user(
        cls,
        session: AsyncSession,
        username: str,
        email: str,
        password_hash: str,
        role: str,
    ) -> User:
        """Creates user model and adds to session.

        NOTE: Does not commit.

        Args:
            session (AsyncSession)
            username (str)
            email (str)
            password_hash (str)
            role (str)

        Returns:
            User: created user
        """

    @classmethod
    async def get_user(cls, session: AsyncSession, id: uuid.UUID) -> Optional[User]:
        """Fetch user by `id`.

        Args:
            session (AsyncSession)
            id (uuid.UUID): user id

        Returns:
            User
        """

    @classmethod
    async def get_user_by_name(
        cls, session: AsyncSession, username: str
    ) -> Optional[User]:
        """Fetches user by `username`.

        Args:
            session (AsyncSession)
            username (str)

        Returns:
            User
        """

    @classmethod
    async def get_user_by_email(
        cls, session: AsyncSession, email: str
    ) -> Optional[User]:
        """Fetches user by `email`.

        Args:
            session (AsyncSession)
            email (str)

        Returns:
            User
        """

    @classmethod
    async def delete_user(cls, session: AsyncSession, id: uuid.UUID) -> None:
        """Deletes user by `id`.

        Args:
            session (AsyncSession)
            id (uuid.UUID): user id
        """

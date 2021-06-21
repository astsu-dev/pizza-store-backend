import uuid
from typing import Optional

from pizza_store.db.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import delete


class UserCRUD:
    """Has methods for getting, adding, deleting users from db.

    Example:
        >>> crud = UserCRUD()
        >>> user = crud.add_user(session, username="john", email="test@example.com", password_hash="hash", role="user")
        >>> await session.commit()
        >>> user
        User(id=uuid.UUID("x-x-x-x-x"), username="john", email="test@example.com", password_hash="hash", role="user")
    """

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

        Example:
            >>> crud = UserCRUD()
            >>> user = crud.add_user(session, username="john",
            ...     email="test@example.com", password_hash="hash", role="user")
            >>> await session.commit()
            >>> user
            User(id=uuid.UUID("x-x-x-x-x"), username="john", email="test@example.com", password_hash="hash", role="user")

        Args:
            session (AsyncSession)
            username (str)
            email (str)
            password_hash (str)
            role (str)

        Returns:
            User: created user
        """

        user = User(
            username=username, email=email, password_hash=password_hash, role=role
        )
        session.add(user)
        return user

    @classmethod
    async def get_user(cls, session: AsyncSession, id: uuid.UUID) -> Optional[User]:
        """Fetch user by `id`.

        Example:
            >>> crud = UserCRUD()
            >>> user = await crud.get_user(session, id=uuid.UUID("x-x-x-x-x"))
            >>> user
            User(id=uuid.UUID("x-x-x-x-x"), username="john", email="test@example.com", password_hash="hash", role="user")

        Args:
            session (AsyncSession)
            id (uuid.UUID): user id

        Returns:
            User
        """

        res = await session.execute(select(User).where(User.id == id))
        return res.scalars().first()

    @classmethod
    async def get_user_by_name(
        cls, session: AsyncSession, username: str
    ) -> Optional[User]:
        """Fetches user by `username`.

        Example:
            >>> crud = UserCRUD()
            >>> user = await crud.get_user_by_name(session, username="john")
            >>> user
            User(id=uuid.UUID("x-x-x-x-x"), username="john", email="test@example.com", password_hash="hash", role="user")

        Args:
            session (AsyncSession)
            username (str)

        Returns:
            User
        """

        res = await session.execute(select(User).where(User.username == username))
        return res.scalars().first()

    @classmethod
    async def get_user_by_email(
        cls, session: AsyncSession, email: str
    ) -> Optional[User]:
        """Fetches user by `email`.

        Example:
            >>> crud = UserCRUD()
            >>> user = await crud.get_user(session, email="test@example.com")
            >>> user
            User(id=uuid.UUID("x-x-x-x-x"), username="john", email="test@example.com", password_hash="hash", role="user")

        Args:
            session (AsyncSession)
            email (str)

        Returns:
            User
        """

        res = await session.execute(select(User).where(User.email == email))
        return res.scalars().first()

    @classmethod
    async def delete_user(cls, session: AsyncSession, id: uuid.UUID) -> None:
        """Deletes user by `id`.

        Example:
            >>> crud = UserCRUD()
            >>> await crud.delete_user(session, id=1)

        Args:
            session (AsyncSession)
            id (uuid.UUID): user id
        """

        await session.execute(delete(User).where(User.id == id))

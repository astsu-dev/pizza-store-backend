from typing import Optional, Protocol

from pizza_store.db.models.category import Category
from sqlalchemy.ext.asyncio import AsyncSession


class ICategoryCRUD(Protocol):
    """Has methods for getting, adding, deleting categories from db.

    Example:
        >>> crud = CategoryCRUD()
        >>> categories = await crud.get_categories(session)
        >>> print(categories)
        [Category(id=1, name="Drinks), Category(id=2, name="Pizzas")]
    """

    @classmethod
    async def get_category(cls, session: AsyncSession, id: int) -> Optional[Category]:
        """Fetchs category by id.

        Example:
            >>> crud = CategoryCRUD()
            >>> category = await crud.get_category(session, id=5)
            >>> if category is not None:
            ...     print(category)
            ... else:
            ...     print("category does not exist")

        Args:
            session (AsyncSession): sqlalchemy session
            id (int): category id

        Returns:
            Optional[Category]: if None category does not exist
        """

    @classmethod
    async def get_categories(cls, session: AsyncSession) -> list[Category]:
        """Fetchs categories.

        Example:
            >>> crud = CategoryCRUD()
            >>> categories = await crud.get_categories(session)
            >>> print(categories)
            [Category(id=1, name="Drinks), Category(id=2, name="Pizzas")]

        Args:
            session (AsyncSession): sqlalchemy session

        Returns:
            list[Category]: list of categories.
        """

    @classmethod
    def add_category(cls, session: AsyncSession, name: str) -> Category:
        """Creates category model and adds to session.

        NOTE: Does not commit.

        Example:
            >>> crud = CategoryCRUD()
            >>> category = crud.add_category(session, name="Drinks")
            >>> await session.commit()
            >>> print(category)
            Category(id=1, name="Drinks")

        Args:
            session (AsyncSession): sqlalchemy session
            name (str): category name

        Returns:
            Category: created category
        """

    @classmethod
    async def delete_category(cls, session: AsyncSession, id: int) -> None:
        """Deletes category by id.

        NOTE: Does not commit.

        Example:
            >>> crud = CategoryCRUD()
            >>> await crud.delete_category(session, id=1)
            >>> await session.commit()

        Args:
            session (AsyncSession): sqlalchemy session
            id (int): category id
        """

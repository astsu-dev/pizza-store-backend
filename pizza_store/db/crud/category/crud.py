from typing import Optional

from pizza_store.db.models.category import Category
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryCRUD:
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

        stmt = select(Category).where(Category.id == id)
        result = await session.execute(stmt)
        return result.scalars().first()

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

        stmt = select(Category)
        result = await session.execute(stmt)
        return result.scalars().all()

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

        category = Category(name=name)
        session.add(category)
        return category

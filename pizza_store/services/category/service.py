from typing import List

import sqlalchemy as sa
from fastapi import HTTPException, status
from pizza_store import models
from pizza_store.db.crud import ICategoryCRUD
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryService:
    """Category service interface

    Example:
        >>> service = CategoryService(session, category_crud)
        >>> await service.get_categories()
        [Category(id=1, name="Pizzas"), Category(id=2, name="Sushi")]
    """

    def __init__(self, session: AsyncSession, category_crud: ICategoryCRUD) -> None:
        self._session = session
        self._category_crud = category_crud

    async def get_categories(self) -> List[models.Category]:
        """Returns list of categories from db.

        Example:
            >>> service = CategoryService(session, category_crud)
            >>> await service.get_categories()
            [Category(id=1, name="Pizza"), Category(id=2, name="Sushi")]

        Returns:
            List[models.Category]
        """

        db_categories = await self._category_crud.get_categories(self._session)
        categories = [
            models.Category(id=category.id, name=category.name)
            for category in db_categories
        ]

        return categories

    async def add_category(
        self, category_create: models.CategoryCreate
    ) -> models.Category:
        """Creates category, add to db.

        Example:
            >>> service = CategoryService(session, category_crud)
            >>> await service.add_category(category_create=CategoryCreate(name="Pizza"))
            Category(id=1, name="Pizza")

        Args:
            name (str): category name

        Returns:
            models.Category: created category
        """

        session = self._session

        db_category = self._category_crud.add_category(
            session, name=category_create.name
        )
        try:
            await session.commit()
        except sa.exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Category already exists"
            )

        category = models.Category(id=db_category.id, name=db_category.name)

        return category

    async def delete_category(self, id: int) -> None:
        """Deletes category from db.

        Example:
            >>> service = CategoryService(session, category_crud)
            >>> await service.delete_category(id=1)

        Args:
            id (int): category id
        """

        session = self._session

        await self._category_crud.delete_category(session, id=id)
        await session.commit()

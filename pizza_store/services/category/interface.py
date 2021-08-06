from typing import List, Protocol

from pizza_store import models


class ICategoryService(Protocol):
    """Category service interface"""

    async def get_categories(self) -> List[models.Category]:
        """Returns list of categories from db.

        Returns:
            List[models.Category]
        """

    async def add_category(
        self, category_create: models.CategoryCreate
    ) -> models.Category:
        """Creates category, add to db.

        Args:
            category_create (models.CategoryCreate): data for create category

        Returns:
            models.Category: created category
        """

    async def delete_category(self, id: int) -> None:
        """Deletes category from db.

        Args:
            id (int): category id
        """

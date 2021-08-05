from typing import List, Protocol

from pizza_store import models


class ICategoryService(Protocol):
    """Category service interface"""

    async def get_categories(self) -> List[models.Category]:
        """Returns list of categories from db.

        Returns:
            List[models.Category]
        """

        ...

    async def add_category(self, name: str) -> models.Category:
        """Creates category, add to db.

        Args:
            name (str): category name

        Returns:
            models.Category: created category
        """

    async def delete_category(self, id: int) -> models.Category:
        """Deletes category from db.

        Args:
            id (int): category id

        Returns:
            models.Category: deleted category
        """

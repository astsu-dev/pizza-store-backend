from typing import Protocol

from pizza_store import models


class IProductService(Protocol):
    """Product service interface"""

    async def get_products(self) -> list[models.Product]:
        """Returns list of products from db.

        Returns:
            list[models.Product]
        """

    async def add_product(self, product_create: models.ProductCreate) -> models.Product:
        """Add product to db.

        Args:
            product_create (models.ProductCreate): data for product adding

        Returns:
            models.Product: created product
        """

    async def delete_product(self, product_id: int) -> None:
        """Deletes product from db.

        Args:
            product_id (int)
        """

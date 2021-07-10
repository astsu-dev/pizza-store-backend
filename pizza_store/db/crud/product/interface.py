from typing import Optional, Protocol

from pizza_store.db.models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession


class IProductCRUD(Protocol):
    """Has methods for getting, adding, deleting products from db."""

    @classmethod
    async def get_product(cls, session: AsyncSession, id: int) -> Optional[Product]:
        """Fetchs product by id.

        Args:
            session (AsyncSession): sqlalchemy session
            id (int): product id

        Returns:
            Optional[Product]: if None product does not exist
        """

    @classmethod
    async def get_products(
        cls,
        session: AsyncSession,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[Product]:
        """Fetchs products.

        Args:
            session (AsyncSession): sqlalchemy session
            limit (Optional[int]): max amount of products. If None unlimitted.
            offset (Optional[int]): products offset. If None offset is 0.

        Returns:
            list[Product]: list of products.
        """

    @classmethod
    def add_product(
        cls,
        session: AsyncSession,
        category_id: int,
        name: str,
        weight: int,
        price: int,
        image: str,
    ) -> Product:
        """Creates product model and adds to session.

        NOTE: Does not commit.

        Args:
            session (AsyncSession): sqlalchemy session
            category_id (int): category id
            name (str): product name
            weight (int): weight in grams
            price (int): price in cents
            image (str): image name

        Returns:
            Product: created product
        """

    @classmethod
    async def delete_product(cls, session: AsyncSession, id: int) -> None:
        """Deletes product by id.

        NOTE: Does not commit.

        Args:
            session (AsyncSession): sqlalchemy session
            id (int): product id
        """

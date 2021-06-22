from typing import Optional, Protocol

from pizza_store.db.models.product import Product
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class ProductCRUD:
    """Has methods for getting, adding, deleting products from db.

    Example:
        >>> crud = ProductCRUD()
        >>> products = await crud.get_products(session, limit=2)
        >>> print(products)
        [Product(id=1, category_id=1, name="Tea", weight: 100, price=5_000),
         Product(id=2, category_id=1, name="Coffee", weight: 100, price=5_000)]
    """

    @classmethod
    def add_product(
        cls, session: AsyncSession, category_id: int, name: str, weight: int, price: int
    ) -> Product:
        """Creates product model and adds to session.

        NOTE: Does not commit.

        Example:
            >>> crud = ProductCRUD()
            >>> product = crud.add_product(session, category_id=1, name="Tea", weight: 100, price=5_000)
            >>> await session.commit()
            >>> print(product)
            Product(id=1, category_id=1, name="Tea", weight: 100, price=5_000)

        Args:
            session (AsyncSession): sqlalchemy session
            category_id (int): category id
            name (str): product name
            weight (int): weight in grams
            price (int): price in cents

        Returns:
            Product: created product
        """

        product = Product(
            category_id=category_id, name=name, weight=weight, price=price
        )
        session.add(product)

        return product

    @classmethod
    async def get_product(cls, session: AsyncSession, id: int) -> Optional[Product]:
        """Fetchs product by id.

        Example:
            >>> crud = ProductCRUD()
            >>> product = await crud.get_product(session, id=1)
            >>> if product is not None:
            ...     print(product)
            ... else:
            ...     print("product does not exist")

        Args:
            session (AsyncSession): sqlalchemy session
            id (int): product id

        Returns:
            Optional[Product]: if None product does not exist
        """

        res = await session.execute(select(Product).where(Product.id == id))
        return res.scalars().first()

    @classmethod
    async def get_products(
        cls,
        session: AsyncSession,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> list[Product]:
        """Fetches products.

        Example:
        >>> crud = ProductCRUD()
        >>> products = await crud.get_products(session, limit=2)
        >>> print(products)
        [Product(id=1, category_id=1, name="Tea", weight: 100, price=5_000), Product(id=2, category_id=1, name="Coffee", weight: 100, price=5_000)]

        Args:
            session (AsyncSession): sqlalchemy session
            limit (Optional[int]): max amount of products. If None unlimitted.
            offset (Optional[int]): products offset. If None offset is 0.

        Returns:
            list[Product]: list of products.
        """

        stmt = select(Product)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        res = await session.execute(stmt)

        return res.scalars().all()

    @classmethod
    async def delete_product(cls, session: AsyncSession, id: int) -> None:
        """Deletes product by id.

        NOTE: Does not commit.

        Example:
            >>> crud = ProductCRUD()
            >>> await crud.delete_product(session, id=1)
            >>> await session.commit()

        Args:
            session (AsyncSession): sqlalchemy session
            id (int): product id
        """

        await session.execute(delete(Product).where(Product.id == id))

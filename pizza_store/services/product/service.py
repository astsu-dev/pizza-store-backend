from pathlib import Path

import sqlalchemy
from fastapi import HTTPException, status
from pizza_store import models
from pizza_store.constants.files import IMAGE_READ_BUFFER
from pizza_store.constants.paths import IMAGE_FOLDER_PATH
from pizza_store.db.crud import IProductCRUD
from pizza_store.utils.files import get_binary_file_hash, write_binary_file
from sqlalchemy.ext.asyncio import AsyncSession


class ProductService:
    """Product service interface

    Example:
        >>> service = ProductService(session, product_crud)
        >>> await service.get_products()
        [models.Product(id=1, category_id=1, name="Pizza", weight=500, price=1000, image="/static/img/pizza.jpg"),
         models.Product(id=2, category_id=2, name="Sushi", weight=500, price=1000, image="/static/img/sushi.jpg")]
    """

    def __init__(self, session: AsyncSession, product_crud: IProductCRUD) -> None:
        self._session = session
        self._product_crud = product_crud

    async def get_products(self) -> list[models.Product]:
        """Returns list of products from db.

        Example:
            >>> service = ProductService(session, product_crud)
            >>> await service.get_products()
            [models.Product(id=1, category_id=1, name="Pizza", weight=500, price=1000, image="/static/img/pizza.jpg"),
             models.Product(id=2, category_id=2, name="Sushi", weight=500, price=1000, image="/static/img/sushi.jpg")]

        Returns:
            list[models.Product]
        """

        db_products = await self._product_crud.get_products(self._session)
        products = [
            models.Product(
                id=p.id,
                category_id=p.category_id,
                name=p.name,
                weight=p.weight,
                price=p.price,
                image=p.image,
            )
            for p in db_products
        ]

        return products

    async def add_product(self, product_create: models.ProductCreate) -> models.Product:
        """Add product to db.

        Args:
            product_create (models.ProductCreate): data for product adding

        Returns:
            models.Product: created product
        """

        session = self._session
        image_file = product_create.image

        image_hash = await get_binary_file_hash(image_file, IMAGE_READ_BUFFER)
        image_path = IMAGE_FOLDER_PATH / image_hash
        image_extension = Path(image_file.filename).suffix
        image_path = image_path.with_suffix(image_extension)

        db_product = self._product_crud.add_product(
            session,
            category_id=product_create.category_id,
            name=product_create.name,
            weight=product_create.weight,
            price=product_create.price,
            image=str(image_path),
        )
        try:
            await session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exists or category does not exists.",
            )

        if not image_path.exists():
            await image_file.seek(0)
            await write_binary_file(
                path=image_path, file=image_file, read_buffer=IMAGE_READ_BUFFER
            )

        product = models.Product(
            id=db_product.id,
            category_id=db_product.category_id,
            name=db_product.name,
            weight=db_product.weight,
            price=db_product.price,
            image=db_product.image,
        )

        return product

    async def delete_product(self, product_id: int) -> None:
        """Deletes product from db.

        Example:
            >>> service = ProductService(session, product_crud)
            >>> await service.delete_product(product_id=1)

        Args:
            product_id (int)
        """

        session = self._session

        await self._product_crud.delete_product(session, id=product_id)
        await session.commit()

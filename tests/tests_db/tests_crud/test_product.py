from unittest import mock

import pytest
from pizza_store.db.crud.product import ProductCRUD
from pizza_store.db.models.product import Product
from sqlalchemy import delete, select


def test_add_product() -> None:
    session = mock.Mock()

    ProductCRUD.add_product(
        session, category_id=1, name="Test", weight=100, price=10_000
    )
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_get_products() -> None:
    scalars = mock.Mock()
    scalars.all.return_value = [1, 2]
    result = mock.Mock()
    result.scalars.return_value = scalars
    session = mock.AsyncMock()
    session.execute.return_value = result

    res = await ProductCRUD.get_products(session, limit=2, offset=0)
    assert res == [1, 2]
    assert str(session.execute.await_args.args[0]) == str(
        select(Product).limit(2).offset(0)
    )


@pytest.mark.asyncio
async def test_get_product() -> None:
    scalars = mock.Mock()
    scalars.first.return_value = 1
    result = mock.Mock()
    result.scalars.return_value = scalars
    session = mock.AsyncMock()
    session.execute.return_value = result

    res = await ProductCRUD.get_product(session, id=1)
    assert res == 1
    assert str(session.execute.await_args.args[0]) == str(
        select(Product).where(Product.id == 1)
    )


@pytest.mark.asyncio
async def test_delete_product() -> None:
    session = mock.AsyncMock()

    await ProductCRUD.delete_product(session, id=1)
    assert str(session.execute.await_args.args[0]) == str(
        delete(Product).where(Product.id == 1)
    )

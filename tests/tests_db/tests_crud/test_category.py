from typing import Final
from unittest import mock

import pytest
from pizza_store.db.crud.category import CategoryCRUD
from pizza_store.db.models import Category, Product
from sqlalchemy import delete, select

CATEGORY_CRUD_MODULE_PATH: Final[str] = "pizza_store.db.crud.category.crud"


@pytest.mark.asyncio
async def test_get_categories() -> None:
    scalars = mock.Mock()
    scalars.all.return_value = [1, 2]
    result = mock.Mock()
    result.scalars.return_value = scalars
    session = mock.AsyncMock()
    session.execute.return_value = result

    res = await CategoryCRUD.get_categories(session)
    assert res == [1, 2]
    assert str(session.execute.await_args.args[0]) == str(select(Category))


@pytest.mark.asyncio
async def test_get_category() -> None:
    scalars = mock.Mock()
    scalars.first.return_value = 1
    result = mock.Mock()
    result.scalars.return_value = scalars
    session = mock.AsyncMock()
    session.execute.return_value = result

    res = await CategoryCRUD.get_category(session, id=5)
    assert res == 1
    assert str(session.execute.await_args.args[0]) == str(
        select(Category).where(Category.id == 5)
    )


def test_add_category() -> None:
    session = mock.Mock()

    CategoryCRUD.add_category(session, name="Test")
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_delete_category() -> None:
    session = mock.AsyncMock()

    await CategoryCRUD.delete_category(session, id=5)
    assert str(session.execute.await_args.args[0]) == str(
        delete(Category).where(Category.id == 5)
    )

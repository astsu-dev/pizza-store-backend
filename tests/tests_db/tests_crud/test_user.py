import uuid
from unittest import mock

import pytest
from pizza_store.db.crud.user import UserCRUD


def test_add_user() -> None:
    session = mock.Mock()

    UserCRUD.add_user(
        session,
        username="John",
        email="example@example.com",
        password_hash="hash",
        role="user",
    )
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_get_user() -> None:
    scalars = mock.Mock()
    scalars.first.return_value = 1
    result = mock.Mock()
    result.scalars.return_value = scalars
    session = mock.AsyncMock()
    session.execute.return_value = result

    res = await UserCRUD.get_user(
        session, id=uuid.UUID("7076a9b6-3a67-46cf-889d-f1ddc2cb2e68")
    )
    assert res == 1


@pytest.mark.asyncio
async def test_get_user_by_name() -> None:
    scalars = mock.Mock()
    scalars.first.return_value = 1
    result = mock.Mock()
    result.scalars.return_value = scalars
    session = mock.AsyncMock()
    session.execute.return_value = result

    res = await UserCRUD.get_user_by_name(session, username="John")
    assert res == 1


@pytest.mark.asyncio
async def test_get_user_by_email() -> None:
    scalars = mock.Mock()
    scalars.first.return_value = 1
    result = mock.Mock()
    result.scalars.return_value = scalars
    session = mock.AsyncMock()
    session.execute.return_value = result

    res = await UserCRUD.get_user_by_email(session, email="example@example.com")
    assert res == 1


@pytest.mark.asyncio
async def test_delete_user() -> None:
    session = mock.AsyncMock()

    await UserCRUD.delete_user(
        session, id=uuid.UUID("7076a9b6-3a67-46cf-889d-f1ddc2cb2e68")
    )
    session.execute.assert_called_once()

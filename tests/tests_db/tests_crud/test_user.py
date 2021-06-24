import uuid
from unittest import mock

import pytest
from pizza_store.db.crud.user import UserCRUD
from pizza_store.db.models import User
from sqlalchemy import delete, select


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
    assert str(session.execute.await_args.args[0]) == str(
        select(User).where(User.id == uuid.UUID("7076a9b6-3a67-46cf-889d-f1ddc2cb2e68"))
    )


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
    assert str(session.execute.await_args.args[0]) == str(
        select(User).where(User.username == "John")
    )


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
    assert str(session.execute.await_args.args[0]) == str(
        select(User).where(User.email == "example@example.com")
    )


@pytest.mark.asyncio
async def test_delete_user() -> None:
    session = mock.AsyncMock()

    await UserCRUD.delete_user(
        session, id=uuid.UUID("7076a9b6-3a67-46cf-889d-f1ddc2cb2e68")
    )
    assert str(session.execute.await_args.args[0]) == str(
        delete(User).where(User.id == uuid.UUID("7076a9b6-3a67-46cf-889d-f1ddc2cb2e68"))
    )

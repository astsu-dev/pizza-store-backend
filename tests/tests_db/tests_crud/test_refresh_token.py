import datetime
import uuid
from typing import Final
from unittest import mock

import pytest
from pizza_store.db.crud.refresh_token.crud import RefreshTokenCRUD
from pizza_store.db.models import RefreshToken
from sqlalchemy import delete, select

CATEGORY_CRUD_MODULE_PATH: Final[str] = "pizza_store.db.crud.refresh_token.crud"


@pytest.mark.asyncio
async def test_get_refresh_token() -> None:
    scalars = mock.Mock()
    scalars.first.return_value = 1
    result = mock.Mock()
    result.scalars.return_value = scalars
    session = mock.AsyncMock()
    session.execute.return_value = result

    res = await RefreshTokenCRUD.get_refresh_token(
        session, user_id=uuid.UUID("ee2a39ce-3812-4872-b17a-35b9c43667d3")
    )
    assert res == 1
    assert str(session.execute.await_args.args[0]) == str(
        select(RefreshToken).where(
            RefreshToken.user_id == uuid.UUID("ee2a39ce-3812-4872-b17a-35b9c43667d3")
        )
    )


def test_add_refresh_token() -> None:
    session = mock.Mock()

    RefreshTokenCRUD.add_refresh_token(
        session,
        user_id=uuid.UUID("ee2a39ce-3812-4872-b17a-35b9c43667d3"),
        token=uuid.UUID("ee2a39ce-3812-4872-b17a-35b9c43667d3"),
        expires_at=datetime.datetime(2020, 12, 12, 15),
    )
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_delete_refresh_token() -> None:
    session = mock.AsyncMock()

    await RefreshTokenCRUD.delete_refresh_token(
        session, user_id=uuid.UUID("ee2a39ce-3812-4872-b17a-35b9c43667d3")
    )
    assert str(session.execute.await_args.args[0]) == str(
        delete(RefreshToken).where(
            RefreshToken.user_id == uuid.UUID("ee2a39ce-3812-4872-b17a-35b9c43667d3")
        )
    )

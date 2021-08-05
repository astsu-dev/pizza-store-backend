import datetime
import uuid

import jwt
import pytest
from fastapi import HTTPException, status
from pizza_store import models
from pizza_store.enums import ProductPermission, Role
from pizza_store.services import AuthService
from pizza_store.settings import settings


def test_get_current_user_with_valid_token() -> None:
    current_datetime = datetime.datetime.utcnow()
    jwt_payload = {
        "exp": current_datetime + datetime.timedelta(seconds=settings.JWT_EXPIRES_IN),
        "iat": current_datetime,
        "user": {
            "id": "ec3365b2-b014-4b2e-ba00-a7fe119d5e09",
            "username": "test",
            "email": "test@example.com",
            "role": Role.USER,
        },
    }
    token = jwt.encode(
        jwt_payload, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    result = AuthService.get_current_user()(token)
    assert result == models.UserInToken(
        username="test",
        email="test@example.com",
        id=uuid.UUID("ec3365b2-b014-4b2e-ba00-a7fe119d5e09"),
        role=Role.USER,
    )


def test_get_current_user_with_invalid_secret_key() -> None:
    current_datetime = datetime.datetime.utcnow()
    jwt_payload = {
        "exp": current_datetime + datetime.timedelta(seconds=settings.JWT_EXPIRES_IN),
        "iat": current_datetime,
        "user": {
            "id": "ec3365b2-b014-4b2e-ba00-a7fe119d5e09",
            "username": "test",
            "email": "test@example.com",
            "role": Role.USER,
        },
    }
    token = jwt.encode(jwt_payload, key="invalid key", algorithm=settings.JWT_ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        AuthService.get_current_user()(token)
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_with_expired_token() -> None:
    current_datetime = datetime.datetime.utcnow()
    jwt_payload = {
        "exp": current_datetime - datetime.timedelta(seconds=settings.JWT_EXPIRES_IN),
        "iat": current_datetime,
        "user": {
            "id": "ec3365b2-b014-4b2e-ba00-a7fe119d5e09",
            "username": "test",
            "email": "test@example.com",
            "role": Role.USER,
        },
    }
    token = jwt.encode(
        jwt_payload, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    with pytest.raises(HTTPException) as excinfo:
        AuthService.get_current_user()(token)
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_with_valid_required_permissions() -> None:
    current_datetime = datetime.datetime.utcnow()
    jwt_payload = {
        "exp": current_datetime + datetime.timedelta(seconds=settings.JWT_EXPIRES_IN),
        "iat": current_datetime,
        "user": {
            "id": "ec3365b2-b014-4b2e-ba00-a7fe119d5e09",
            "username": "test",
            "email": "test@example.com",
            "role": Role.USER,
        },
    }
    token = jwt.encode(
        jwt_payload, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    result = AuthService.get_current_user(
        required_permissions=(ProductPermission.READ,)
    )(token)
    assert result == models.UserInToken(
        username="test",
        email="test@example.com",
        id=uuid.UUID("ec3365b2-b014-4b2e-ba00-a7fe119d5e09"),
        role=Role.USER,
    )


def test_get_current_user_with_invalid_required_permissions() -> None:
    current_datetime = datetime.datetime.utcnow()
    jwt_payload = {
        "exp": current_datetime + datetime.timedelta(seconds=settings.JWT_EXPIRES_IN),
        "iat": current_datetime,
        "user": {
            "id": "ec3365b2-b014-4b2e-ba00-a7fe119d5e09",
            "username": "test",
            "email": "test@example.com",
            "role": Role.USER,
        },
    }
    token = jwt.encode(
        jwt_payload, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    with pytest.raises(HTTPException) as excinfo:
        AuthService.get_current_user(required_permissions=(ProductPermission.CREATE,))(
            token
        )

    assert excinfo.value.status_code == status.HTTP_403_FORBIDDEN

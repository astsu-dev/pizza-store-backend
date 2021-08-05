from typing import Optional

import pizza_store.models as models
from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pizza_store.dependencies.services import get_auth_service
from pizza_store.models import UserIn
from pizza_store.services import IAuthService

auth_router = APIRouter(prefix="/auth")
router = auth_router


@router.post("/sign-up", status_code=201, response_model=models.User)
async def sign_up(
    user_create: models.UserCreate,
    service: IAuthService = Depends(get_auth_service),
):
    return await service.sign_up(user_create=user_create)


@router.post("/sign-in", response_model=models.TokenResponse)
async def sign_in(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: IAuthService = Depends(get_auth_service),
):
    return await service.sign_in(
        user_in=UserIn(username=form_data.username, password=form_data.password),
        response=response,
    )


@router.get("/refresh", response_model=models.TokenResponse)
async def refresh(
    response: Response,
    refresh_token: Optional[str] = Cookie(None),
    service: IAuthService = Depends(get_auth_service),
):
    return await service.refresh_tokens(
        response=response, refresh_token_cookie=refresh_token
    )

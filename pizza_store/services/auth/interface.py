import datetime
import uuid
from typing import Any, Callable, Dict, FrozenSet, Iterable, Optional, Protocol

import pizza_store.models as models
from fastapi import Response


class IAuthService(Protocol):
    @classmethod
    def create_access_token(
        cls,
        payload: Dict[str, Any],
        key: str,
        algorithm: str,
        expires_in: datetime.timedelta,
    ) -> str:
        """Creates access token from payload.

        Adds iat, exp claims.

        Args:
            payload (Dict[str, Any])
            key (str): secret key
            algorithm (str)
            expires_in (datetime.timedelta)

        Returns:
            str: access token
        """

    @classmethod
    def create_access_token_for_user(
        cls, user: models.UserInToken, key: str, algorithm: str, expires_in: int
    ) -> str:
        """Creates access token for user.

        Args:
            user (models.UserInToken): user data
            key (str): jwt secret
            algorithm (str): jwt algorithm
            expires_in (int)

        Returns:
            str: access token
        """

    @classmethod
    def create_token_response(cls, user: models.UserInToken) -> models.TokenResponse:
        """Creates token response for user.

        Token response is oauth2 response.

        Args:
            user (models.UserInToken): user data

        Returns:
            models.TokenResponse
        """

    @classmethod
    def create_refresh_token(cls) -> uuid.UUID:
        """Creates refresh token.

        Refresh token represents uuid4.

        Returns:
            str
        """

    @classmethod
    def verify_password(cls, password: str, password_hash: str) -> bool:
        """Returns True if `password` hash match `password_hash`.

        Args:
            password (str)
            password_hash (str)

        Returns:
            bool
        """

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Returns `password` hash.

        Args:
            password (str)

        Returns:
            str
        """

    @classmethod
    def decode_token(cls, token: str, key: str, algorithm: str) -> models.Token:
        """Decodes token.

        Args:
            token (str)
            key (str): jwt secret key
            algorithm (str)
            decode_exception (Exception)

        Raises:
            HTTPException: raises 401 http exception if token is not valid

        Returns:
            Token
        """

    @classmethod
    def check_permissions(
        cls, permissions: FrozenSet[str], required_permissions: FrozenSet[str]
    ) -> None:
        """Raises 403 http exception if `required_permissions` has not `permissions`.

        Args:
            permissions (FrozenSet[str])
            required_permissions (FrozenSet[str])

        Raises:
            HTTPException
        """

    @classmethod
    def get_current_user(
        cls, required_permissions: Optional[Iterable[str]] = None
    ) -> Callable[[str], models.UserInToken]:
        """Returns fastapi dependency.

        Dependency verifies access token, check user permissions and returns user from token.

        Args:
            required_permissions (Optional[Iterable[str]]): if None will be empty

        Returns:
            Callable[[str], models.UserInToken]: fastapi dependency
        """

    async def sign_up(self, user_create: models.UserCreate) -> models.User:
        """Signs up user.

        Args:
            user_create (models.UserCreate): model with user credentials

        Raises:
            HTTPException: will be raised 409 http error if user already exists.

        Returns:
            models.User: pydantic created user model.
        """

    async def sign_in(
        self, user_in: models.UserIn, response: Response
    ) -> models.TokenResponse:
        """Creates access and refresh tokens for user.

        Access token will be in response. Refresh token will be setted to cookies.

        Args:
            user_in (models.UserIn): model with username and password
            response (Response): need for set refresh token to cookies

        Raises:
            HTTPException: will be raised if invalid username or password

        Returns:
            models.TokenResponse
        """

    async def refresh_tokens(
        self, response: Response, refresh_token_cookie: Optional[str] = None
    ) -> models.TokenResponse:
        """Returns new pair of refresh and access tokens.

        Access token will be in response. Refresh token will be in cookies.

        Args:
            response (Response): needs for set new refresh token to cookie.
            refresh_token_cookie (Optional[str]): refresh_token cookie value.

        Raises:
            HTTPException: will be raised 403 http error code if refresh token is not passed.

        Returns:
            models.TokenResponse
        """

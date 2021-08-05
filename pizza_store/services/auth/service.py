import datetime
import uuid
from typing import Any, Callable, Dict, FrozenSet, Iterable, Optional

import jwt
import pizza_store.db.models as tables
import pizza_store.models as models
import sqlalchemy as sa
from fastapi import Depends, Response, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
from pizza_store.constants.roles import ROLES
from pizza_store.db.crud import IRefreshTokenCRUD, IUserCRUD
from pizza_store.enums.role import Role
from pizza_store.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_password_bearer_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/sign-in")


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        user_crud: IUserCRUD,
        refresh_token_crud: IRefreshTokenCRUD,
    ) -> None:
        self._session = session
        self._user_crud = user_crud
        self._refresh_token_crud = refresh_token_crud

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

        created_at = datetime.datetime.utcnow()
        expires_at = created_at + expires_in
        payload = {**payload, "iat": created_at, "exp": expires_at}
        token = jwt.encode(payload, key, algorithm=algorithm)
        return token

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

        user_id = str(user.id)
        user_dict = {**user.dict(), "id": user_id}  # Replace id on string
        payload = {"user": user_dict, "sub": user_id}

        expires_in_delta = datetime.timedelta(seconds=expires_in)

        access_token = cls.create_access_token(
            payload,
            key=key,
            algorithm=algorithm,
            expires_in=expires_in_delta,
        )

        return access_token

    @classmethod
    def create_token_response(cls, user: models.UserInToken) -> models.TokenResponse:
        """Creates token response for user.

        Token response is oauth2 response.

        Args:
            user (models.UserInToken): user data

        Returns:
            models.TokenResponse
        """

        expires_in = settings.JWT_EXPIRES_IN

        access_token = cls.create_access_token_for_user(
            user,
            key=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
            expires_in=expires_in,
        )
        token_response = models.TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in,
        )

        return token_response

    @classmethod
    def create_refresh_token(cls) -> uuid.UUID:
        """Creates refresh token.

        Refresh token represents uuid4.

        Returns:
            str
        """

        refresh_token = uuid.uuid4()

        return refresh_token

    @classmethod
    def verify_password(cls, password: str, password_hash: str) -> bool:
        """Returns True if `password` hash match `password_hash`.

        Args:
            password (str)
            password_hash (str)

        Returns:
            bool
        """

        return bcrypt.verify(password, password_hash)

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Returns `password` hash.

        Args:
            password (str)

        Returns:
            str
        """

        return bcrypt.hash(password)

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

        try:
            token_data = jwt.decode(token, key=key, algorithms=[algorithm])
        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        return models.Token(**token_data)

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

        if not required_permissions.issubset(permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )

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

        required_permissions = (
            frozenset(required_permissions)
            if required_permissions is not None
            else frozenset()
        )

        def dependency(
            token: str = Depends(oauth2_password_bearer_scheme),
        ) -> models.UserInToken:
            token_data = cls.decode_token(
                token, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
            )
            user = token_data.user

            cls.check_permissions(ROLES[user.role], required_permissions)

            return user

        return dependency

    async def sign_up(self, user_create: models.UserCreate) -> models.User:
        """Signs up user.

        Args:
            user_create (models.UserCreate)

        Raises:
            HTTPException: will be raised 409 http error if user already exists.

        Returns:
            models.User: pydantic created user model.
        """

        password_hash = self.hash_password(user_create.password)
        user_db = await self._add_user_to_db(user_create, password_hash)
        user = models.User.from_orm(user_db)

        return user

    async def sign_in(
        self, user_in: models.UserIn, response: Response
    ) -> models.TokenResponse:
        """Creates access and refresh tokens for user.

        Access token will be in response. Refresh token will be setted to cookies.

        Args:
            form_data (OAuth2PasswordRequestForm): has user username and password
            response (Response): need for set refresh token to cookies

        Raises:
            HTTPException: will be raised if invalid username or password

        Returns:
            models.TokenResponse
        """

        session = self._session

        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

        user_db = await self._user_crud.get_user_by_email(
            session, email=user_in.username
        )
        if user_db is None or not self.verify_password(
            password=user_in.password, password_hash=user_db.password_hash
        ):
            raise exception

        user_id = user_db.id

        await self._make_refresh_token(user_id=user_id, response=response)

        user = models.UserInToken.from_orm(user_db)
        token_response = self.create_token_response(user)

        return token_response

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

        if refresh_token_cookie is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token"
            )

        session = self._session

        try:
            refresh_token = uuid.UUID(refresh_token_cookie)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        refresh_token_db = await self._refresh_token_crud.get_refresh_token(
            session, token=refresh_token
        )
        if (
            refresh_token_db is None
            or datetime.datetime.utcnow() > refresh_token_db.expires_at
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is expired or does not exist",
            )

        user_id = refresh_token_db.user_id

        user_db = await self._user_crud.get_user(session, id=user_id)
        assert user_db is not None

        user = models.UserInToken.from_orm(user_db)
        token_response = self.create_token_response(user)

        await self._make_refresh_token(user_id=user_id, response=response)

        return token_response

    async def _make_refresh_token(self, user_id: uuid.UUID, response: Response) -> None:
        """Deletes old user refresh token from db, then creates new, then writes it to db, then set to cookies.

        Args:
            user_id (uuid.UUID)
            response (Response)
        """

        await self._delete_refresh_token(user_id=user_id)
        refresh_token = self.create_refresh_token()
        await self._add_refresh_token(user_id=user_id, token=refresh_token)
        response.set_cookie("refresh_token", str(refresh_token), httponly=True)

    async def _delete_refresh_token(self, user_id: uuid.UUID) -> None:
        """Deletes refresh token for user with `user_id` from db.

        Args:
            user_id (uuid.UUID)
        """

        session = self._session

        await self._refresh_token_crud.delete_refresh_token(
            self._session, user_id=user_id
        )
        await session.commit()

    async def _add_refresh_token(
        self, user_id: uuid.UUID, token: uuid.UUID
    ) -> tables.RefreshToken:
        """Adds refresh token for user with user_id to db.

        Sets expires at.

        Args:
            user_id (uuid.UUID)
        """

        session = self._session

        expires_at = datetime.datetime.utcnow() + datetime.timedelta(
            seconds=settings.JWT_REFRESH_EXPIRES_IN
        )

        refresh_token = self._refresh_token_crud.add_refresh_token(
            session, user_id=user_id, token=token, expires_at=expires_at
        )
        await session.commit()

        return refresh_token

    async def _add_user_to_db(
        self, user_create: models.UserCreate, password_hash: str
    ) -> tables.User:
        """Writes user to db.

        Args:
            user_create (models.UserCreate)
            password_hash (str)

        Raises:
            HTTPException: will be raised 409 http error if user already exists.

        Returns:
            tables.User: user orm model
        """

        session = self._session

        user_db = self._user_crud.add_user(
            session,
            username=user_create.username,
            email=user_create.email,
            password_hash=password_hash,
            role=Role.USER,
        )
        try:
            await session.commit()
        except sa.exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )

        return user_db

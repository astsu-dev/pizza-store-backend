from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

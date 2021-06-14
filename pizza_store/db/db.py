from pizza_store.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_url = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)
engine = create_async_engine(db_url, echo=True)
async_session = sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession
)
Base = declarative_base()

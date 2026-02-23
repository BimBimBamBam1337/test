from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

__all__ = ["SessionFactory", "engine"]


engine = create_async_engine(
    settings.postgres_dsn,
    echo=False,
    future=True,
    pool_timeout=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)


SessionFactory = async_sessionmaker(engine, expire_on_commit=False, autocommit=False)

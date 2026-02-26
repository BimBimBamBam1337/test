from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from conf import POSTGRES_DSN

__all__ = ["SessionFactory", "engine"]


engine = create_async_engine(
    POSTGRES_DSN,
)


SessionFactory = async_sessionmaker(engine, expire_on_commit=False, autocommit=False)

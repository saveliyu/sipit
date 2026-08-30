from typing import AsyncGenerator, Annotated, TypeAlias

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings


class DbHelper:
    def __init__(
        self,
        url: str,
        pool_size: int = 5,
        max_overflow: int = 10,
        echo: bool = False,
        echo_pool: bool = False,
    ) -> None:
        self.engine = create_async_engine(
            url=url,
            pool_size=pool_size,
            max_overflow=max_overflow,
            echo=echo,
            echo_pool=echo_pool,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine, autocommit=False, expire_on_commit=False, autoflush=False
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper = DbHelper(
    url=str(settings.db.url),
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
)


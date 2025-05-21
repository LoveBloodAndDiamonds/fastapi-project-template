"""Database class with all-in-one features."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core import config

from .models import Base


class Database:
    """Database class.

    Is the highest abstraction level of database and
    can be used in the handlers or any other bot-side functions.
    """

    engine: AsyncEngine = create_async_engine(url=config.db.build_connection_str())
    """ Pre-inited database engine """

    sessionmaker = async_sessionmaker(bind=engine)
    """ Sessionmaker """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize Database class.

        :param session: AsyncSession to use
        """
        self.session: AsyncSession = session
        """ Current database session """

    @classmethod
    @asynccontextmanager
    async def session_context(cls) -> AsyncGenerator["Database", None]:
        """Async session generator"""
        async with cls.sessionmaker() as session:
            yield cls(session)  # Возвращаем объект сессии

    async def commit(self) -> None:
        """Make commit using AsyncSession."""
        await self.session.commit()

    async def refresh(self, instance: type[Base]) -> None:
        """Expire and refresh the attributes on the given instance"""
        await self.session.refresh(instance)

    async def flush(self) -> None:
        """Make flush using AsyncSession."""
        await self.session.flush()

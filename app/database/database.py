"""Класс, инкапсулирующий работу с базой данных."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import config

from .models import Base


class Database:
    """Высокоуровневая обертка над взаимодействием с базой данных."""

    engine: AsyncEngine = create_async_engine(url=config.db.build_connection_str())
    """Предварительно инициализированный движок базы данных."""

    sessionmaker = async_sessionmaker(bind=engine)
    """Фабрика асинхронных сессий."""

    def __init__(self, session: AsyncSession) -> None:
        """Создает экземпляр класса Database.

        :param session: Асинхронная сессия, используемая для операций.
        """
        self.session: AsyncSession = session
        """Текущая сессия базы данных."""

    @classmethod
    @asynccontextmanager
    async def session_context(cls) -> AsyncGenerator["Database"]:
        """Генератор асинхронных сессий."""
        async with cls.sessionmaker() as session:
            yield cls(session)  # Возвращаем объект сессии

    async def commit(self) -> None:
        """Фиксирует изменения в базе данных."""
        await self.session.commit()

    async def refresh(self, instance: type[Base]) -> None:
        """Принудительно обновляет атрибуты переданного экземпляра модели."""
        await self.session.refresh(instance)

    async def flush(self) -> None:
        """Сбрасывает изменения в базу без коммита."""
        await self.session.flush()

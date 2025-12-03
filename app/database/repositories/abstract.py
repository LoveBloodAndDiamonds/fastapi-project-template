"""Абстрактный репозиторий для работы с моделями БД."""

from collections.abc import Sequence
from typing import Any, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base

AbstractModel = TypeVar("AbstractModel", bound=Base)


class Repository[AbstractModel]:
    """Базовый абстрактный репозиторий."""

    def __init__(self, type_model: type[AbstractModel], session: AsyncSession):
        """Инициализирует абстрактный репозиторий.

        :param type_model: Модель, с которой выполняются операции.
        :param session: Сессия, в рамках которой работает репозиторий.
        """
        self.type_model = type_model
        self.session = session

    async def get(self, ident: int | str) -> AbstractModel | None:
        """Получает одну запись по первичному ключу.

        :param ident: Значение ключа, по которому ищем запись.
        :return: Найденная модель или None.
        """
        return await self.session.get(entity=self.type_model, ident=ident)

    async def get_by_where(self, whereclause) -> AbstractModel | None:
        """Возвращает одну запись по условию.

        :param whereclause: Условие, по которому выполняется поиск.
        :return: Модель при единственном совпадении, иначе None.
        """
        statement = select(self.type_model).where(whereclause)
        result = await self.session.execute(statement)
        row = result.one_or_none()
        return row[0] if row else None

    async def get_many(
        self, whereclause=None, limit: int = 999, order_by=None
    ) -> Sequence[AbstractModel]:
        """Получает несколько записей, удовлетворяющих условию.

        :param whereclause: (опционально) условие фильтрации записей.
        :param limit: (опционально) максимальное количество результатов.
        :param order_by: (опционально) выражение для сортировки.

        Пример:
        >> Repository.get_many(Model.id == 1, limit=10, order_by=Model.id)

        :return: Список найденных моделей.
        """
        statement = select(self.type_model)
        if whereclause is not None:
            statement = statement.where(whereclause)
        if limit:
            statement = statement.limit(limit)
        if order_by is not None:
            statement = statement.order_by(order_by)

        return (await self.session.scalars(statement)).all()

    async def get_all(
        self, whereclause: Any | None = None, order_by: Any | None = None
    ) -> Sequence[AbstractModel]:
        """Возвращает все записи с дополнительными условиями.

        :param whereclause: (опционально) условие фильтрации.
        :param order_by: (опционально) выражение для сортировки.

        Пример:
        >> Repository.get_all(Model.is_active == True, order_by=Model.id)

        :return: Список всех найденных моделей.
        """
        statement = select(self.type_model)
        if whereclause is not None:
            statement = statement.where(whereclause)
        if order_by:
            statement = statement.order_by(order_by)

        return (await self.session.scalars(statement)).all()

    async def delete(self, whereclause) -> None:
        """Удаляет записи по заданному условию.

        :param whereclause: Условие удаления.
        :return: None.
        """
        statement = delete(self.type_model).where(whereclause)
        await self.session.execute(statement)

    async def delete_all(self) -> None:
        """Удаляет все записи модели из базы данных.

        :return: None.
        """
        statement = delete(self.type_model)
        await self.session.execute(statement)

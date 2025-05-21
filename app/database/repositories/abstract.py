"""Repository file."""

from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base

AbstractModel = TypeVar("AbstractModel", bound=Base)


class Repository(Generic[AbstractModel]):
    """Repository abstract class."""

    def __init__(self, type_model: type[AbstractModel], session: AsyncSession):
        """Initialize abstract repository class.

        :param type_model: Which model will be used for operations
        :param session: Session in which repository will work.
        """
        self.type_model = type_model
        self.session = session

    async def get(self, ident: int | str) -> AbstractModel | None:
        """Get an ONE model from the database with PK.

        :param ident: Key which need to find entry in database
        :return:
        """
        return await self.session.get(entity=self.type_model, ident=ident)

    async def get_by_where(self, whereclause) -> AbstractModel | None:
        """Get an ONE model from the database with whereclause.

        :param whereclause: Clause by which entry will be found
        :return: Model if only one model was found, else None.
        """
        statement = select(self.type_model).where(whereclause)
        result = await self.session.execute(statement)
        row = result.one_or_none()
        return row[0] if row else None

    async def get_many(
        self, whereclause=None, limit: int = 999, order_by=None
    ) -> Sequence[AbstractModel]:
        """Get many models from the database with whereclause.

        :param whereclause: (Optional) Where clause for finding models
        :param limit: (Optional) Limit count of results
        :param order_by: (Optional) Order by clause.

        Example:
        >> Repository.get_many(Model.id == 1, limit=10, order_by=Model.id)

        :return: List of founded models
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
        """Get all models from the database with optional whereclause.

        :param whereclause: (Optional) Where clause for finding models
        :param order_by: (Optional) Order by clause.

        Example:
        >> Repository.get_all(Model.is_active == True, order_by=Model.id)

        :return: List of all found models
        """
        statement = select(self.type_model)
        if whereclause is not None:
            statement = statement.where(whereclause)
        if order_by:
            statement = statement.order_by(order_by)

        return (await self.session.scalars(statement)).all()

    async def delete(self, whereclause) -> None:
        """Delete model from the database.

        :param whereclause: (Optional) Which statement
        :return: Nothing
        """
        statement = delete(self.type_model).where(whereclause)
        await self.session.execute(statement)

    async def delete_all(self) -> None:
        """Delete all records from the model in the database.

        :return: Nothing
        """
        statement = delete(self.type_model)
        await self.session.execute(statement)

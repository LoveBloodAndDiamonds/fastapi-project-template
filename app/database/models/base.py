"""Базовые модели SQLAlchemy."""

import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Аннотация для поля created_at
created_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]


class Base(DeclarativeBase):
    """Базовая модель SQLAlchemy."""

    created_at: Mapped[created_at]
    """Когда запись была создана."""

    # Starlette-admin representations
    # Docs: https://jowilf.github.io/starlette-admin/user-guide/configurations/modelview/

    async def __admin_repr__(self, *_, **__) -> str:
        return f"[{self.__class__.__name__}]"

    async def __admin_select2_repr__(self, *_, **__) -> str:
        return f"<span>{self.__class__.__name__}</span>"

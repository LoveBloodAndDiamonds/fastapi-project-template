__all__ = [
    "EnvironmentType",
]

from enum import StrEnum


class EnvironmentType(StrEnum):
    """Перечисление типов окружения."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"

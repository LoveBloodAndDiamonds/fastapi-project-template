"""
Конфигурационные данные и настройка логирования.
"""

__all__ = [
    "config",
]

import os
import uuid
from dataclasses import dataclass
from os import getenv

from sqlalchemy import URL

from app.schemas import EnvironmentType


@dataclass(frozen=True)
class _DatabaseConfig:
    """Параметры подключения к базе данных."""

    name: str | None = getenv("POSTGRES_DB")
    user: str | None = getenv("POSTGRES_USER")
    passwd: str | None = getenv("POSTGRES_PASSWORD", None)
    port: int = int(getenv("POSTGRES_PORT", "5432"))
    host: str = getenv("POSTGRES_HOST", "db")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def build_connection_str(self) -> str:
        """Формирует строку подключения к базе данных."""
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass(frozen=True)
class _AdminConfig:
    """Настройки админ-панели."""

    title: str = "Admin Panel"
    """Название приложения."""

    logo_url: str = "https://images.icon-icons.com/3256/PNG/512/admin_lock_padlock_icon_205893.png"
    """Ссылка на логотип."""

    login: str = getenv("ADMIN_LOGIN", "admin")
    """Логин администратора."""

    password: str = getenv("ADMIN_PASSWORD", "admin")
    """Пароль администратора."""


@dataclass(frozen=True)
class Configuration:
    """Единая точка доступа к настройкам приложения."""

    db: _DatabaseConfig = _DatabaseConfig()
    """Конфигурация базы данных."""

    admin: _AdminConfig = _AdminConfig()
    """Конфигурация админ-панели."""

    try:
        environment: EnvironmentType = EnvironmentType(os.getenv("ENVIRONMENT", "production"))
        """Текущее окружение проекта."""
    except KeyError as err:
        raise ValueError(f"Invalid environment: {os.getenv('ENVIRONMENT')}") from err

    cypher_key: str = getenv("CYPHER_KEY", uuid.UUID(int=uuid.getnode()).hex[-12:])
    """Ключ для шифрования."""


config: Configuration = Configuration()

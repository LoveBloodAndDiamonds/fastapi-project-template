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
    """Database connection variables."""

    name: str | None = getenv("POSTGRES_DB")
    user: str | None = getenv("POSTGRES_USER")
    passwd: str | None = getenv("POSTGRES_PASSWORD", None)
    port: int = int(getenv("POSTGRES_PORT", 5432))
    host: str = getenv("POSTGRES_HOST", "db")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def build_connection_str(self) -> str:
        """This function build a connection string."""
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
    """Admin panel configuration."""

    title: str = "Admin Panel"
    """App title"""

    logo_url: str = "https://images.icon-icons.com/3256/PNG/512/admin_lock_padlock_icon_205893.png"
    """Logo url"""

    login: str = getenv("ADMIN_LOGIN", "admin")
    """Admin login"""

    password: str = getenv("ADMIN_PASSWORD", "admin")
    """Admin password"""


@dataclass(frozen=True)
class Configuration:
    """All in one configuration's class."""

    db: _DatabaseConfig = _DatabaseConfig()
    """Database config"""

    admin: _AdminConfig = _AdminConfig()
    """Admin panel config"""

    try:
        environment: EnvironmentType = EnvironmentType(os.getenv("ENVIRONMENT", "production"))
        """Current project environment"""
    except KeyError as err:
        raise ValueError(f"Invalid environment: {os.getenv('ENVIRONMENT')}") from err

    cypher_key: str = getenv("CYPHER_KEY", uuid.UUID(int=uuid.getnode()).hex[-12:])
    """Cypher key"""


config: Configuration = Configuration()

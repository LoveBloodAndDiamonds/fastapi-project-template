"""Точка входа Alembic для выполнения миграций."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app import core
from app.database.models import *

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set sqlalchemy.url
config.set_main_option(
    "sqlalchemy.url", core.config.db.build_connection_str() + "?async_fallback=true"
)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata  # noqa: F405

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Запускает миграции в офлайн-режиме.

    Контекст настраивается только через строку подключения без создания движка,
    хотя использование движка здесь также допустимо. Пропуская создание движка,
    мы избавляемся от необходимости в доступном DBAPI.

    Вызовы context.execute() в этом режиме просто выводят сформированные SQL-строки.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запускает миграции в онлайн-режиме.

    В этом сценарии создается движок и связывается подключение с контекстом.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

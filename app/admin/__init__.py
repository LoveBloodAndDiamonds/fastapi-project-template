"""Настройка админ-панели и регистрация представлений."""

__all__ = [
    "register_admin_routes",
]

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import CustomView
from starlette_admin.contrib.sqla import Admin

from app.config import config
from app.database import Database

from .auth import AdminAuthProvider
from .view import LogsCustomView, MetrCustomView


def register_admin_routes(app: FastAPI) -> None:
    """Регистрирует представления админ-панели в FastAPI-приложении."""

    # Init starlette-admin instance
    admin = Admin(
        engine=Database.engine,
        login_logo_url=config.admin.logo_url,
        auth_provider=AdminAuthProvider(),
        base_url="/admin",
        templates_dir="app/admin/templates",
        middlewares=[Middleware(SessionMiddleware, secret_key=config.cypher_key)],
    )

    # Add views
    admin.add_view(CustomView(label="Инструкция", icon="fa fa-info"))
    admin.add_view(LogsCustomView(label="Логи", path="/logs", icon="fa fa-book"))
    admin.add_view(MetrCustomView(label="Система", path="/monitoring", icon="fa fa-heartbeat"))

    # Mount starlette-admin instance to fastApi applaction
    admin.mount_to(app)

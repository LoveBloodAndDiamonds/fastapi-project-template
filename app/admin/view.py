"""Пользовательские представления для админ-панели."""

__all__ = [
    "MetrCustomView",
    "LogsCustomView",
]

import os
from datetime import datetime
from typing import Any

import aiofiles
import psutil
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates
from starlette_admin import (
    CustomView,
)
from starlette_admin.contrib.sqla import ModelView

from app.core import logger


class _CustomModelView(ModelView):
    def handle_exception(self, exc: Exception) -> None:
        try:
            super().handle_exception(exc)
        except Exception as e:
            logger.exception(e)
            raise e


class MetrCustomView(CustomView):
    async def render(self, request: Request, templates: Jinja2Templates) -> Response:  # noqa
        try:
            # Получение данных о системе
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            cpu_percent = psutil.cpu_percent(interval=1)
            boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

            # Подготовка контекста
            context: dict[str, Any] = {
                "request": request,
                "memory_total": f"{memory.total / (1024**3):.2f} GB",
                "memory_used": f"{memory.used / (1024**3):.2f} GB",
                "memory_percent": f"{memory.percent}%",
                "disk_total": f"{disk.total / (1024**3):.2f} GB",
                "disk_used": f"{disk.used / (1024**3):.2f} GB",
                "disk_percent": f"{disk.percent}%",
                "cpu_percent": f"{cpu_percent}%",
                "boot_time": boot_time,
            }

            # Рендеринг шаблона с контекстом
            return templates.TemplateResponse("metr.html", context)
        except Exception as e:
            logger.error(f"Error in MetrCustomView: {e}")
            raise


class LogsCustomView(CustomView):
    async def render(self, request: Request, templates: Jinja2Templates) -> Response:  # noqa
        try:
            # Чтение логов и подготовка контекста
            context: dict[str, Any] = {"request": request}

            for key in ["error", "info", "debug", "trace"]:
                filepath: str = f"logs/{key}.log"
                if os.path.exists(filepath):
                    async with aiofiles.open(filepath) as file:
                        logs = [line.strip() for line in (await file.read()).splitlines()]
                        context[key] = list(reversed(logs[-500:]))
                else:
                    context[key] = [f"Файл {filepath} не существует"]

            # Рендеринг шаблона с контекстом логов
            return templates.TemplateResponse("logs.html", context)
        except Exception as e:
            logger.error(f"Error in LogsCustomView: {e}")
            raise

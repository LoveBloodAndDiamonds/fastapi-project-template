"""Интерфейс доступа к конфигурации и логированию."""

__all__ = [
    "get_logger",
    "logger",
    "config",
]

from .config import config
from .logger import get_logger, logger

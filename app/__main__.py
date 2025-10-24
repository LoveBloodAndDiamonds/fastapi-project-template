"""Точка входа FastAPI-приложения."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .admin import register_admin_routes
from .core import config, logger
from .schemas import EnvironmentType


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения."""
    # Launch logs
    logger.info(f"Admin panel startup! Environment: {config.environment}")
    if config.environment == EnvironmentType.DEVELOPMENT:
        logger.debug("Admin panel url: http://127.0.0.1:8000/admin")
    else:
        logger.info("App started!")

    # Register admin routes
    register_admin_routes(app)

    # Give control to FastAPI
    yield

    # Shutdown logs
    logger.info("Admin panel shutdown!")


# Main FastAPI object
app = FastAPI(
    lifespan=lifespan,
    **{
        "docs_url": None,
        "redoc_url": None,
        "openapi_url": None,
    }
    if config.environment == EnvironmentType.PRODUCTION
    else {},  # type: ignore
)

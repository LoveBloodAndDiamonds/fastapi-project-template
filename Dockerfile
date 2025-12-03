FROM python:3.13-slim

# Определяем рабочую директорию
WORKDIR /app

# Устанавливаем uv
RUN pip install --no-cache-dir uv

# Настраиваем режим работы uv
ENV UV_LINK_MODE=copy

# Копируем зависимости
COPY uv.lock pyproject.toml /app/

# Устанавилваем зависимости
RUN uv sync

# Копируем файл миграций
COPY alembic.ini /app/alembic.ini

# Копируем приложение
COPY app /app/app

create-migrations:
	docker compose run --rm app uv run alembic revision --autogenerate

migrate:
	docker compose run --rm app uv run alembic upgrade head

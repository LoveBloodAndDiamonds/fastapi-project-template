create-migrations:
	@echo "Enter migration message: "; \
	read MESSAGE; \
	docker compose run --rm app uv run alembic revision --autogenerate -m "$$MESSAGE"

migrate:
	docker compose run --rm app uv run alembic upgrade head

clean-macos-trash-stuff:
	find . -name ".DS_Store" -type f -delete

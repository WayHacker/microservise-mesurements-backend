.PHONY: help db-up db-down db-reset migrate-create migrate-up server redis-cli

help:
	@echo "db-up          - Запустить PostgreSQL и Redis"
	@echo "db-down        - Остановить контейнеры"
	@echo "db-reset       - Удалить данные и пересоздать"
	@echo "migrate-create - Создать миграцию (msg=описание)"
	@echo "migrate-up     - Применить миграции"
	@echo "server         - Запустить сервер разработки"
	@echo "redis-cli      - Консоль Redis"

db-up:
	docker compose up -d

db-down:
	docker compose down

db-reset:
	docker compose down -v
	docker compose up -d

migrate-create:
	alembic revision --autogenerate -m "$(msg)"

migrate-up:
	alembic upgrade head

server:
	uvicorn app.main:app --reload

redis-cli:
	docker compose exec redis redis-cli
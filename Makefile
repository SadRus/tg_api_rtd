
build: ## Собирает докер-образ
	docker compose build


up: ## Запускает докер-контейнер
	docker compose up

clean: ## Очищает все volume в соответствии с docker-compose
	docker compose down -v



linter: ## Запускает python линтеры
	docker compose run --rm py-linters flake8 /tg_api/ /tests/



test: ## Запускает python-тесты
	docker compose run --rm tg-api pytest


build-docs: ## Запускает сборку документации Sphinx
	docker compose run --rm tg-api bash -c "cd sphinx_docs; make html"


help: ## Отображает список доступных целей и их описания
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

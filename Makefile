.PHONY: test-unit

test-unit:
	pytest -q tests/unit -c setup.cfg


.PHONY: install
install: ## Install dev requirements
	pip install -r requirements.dev.txt

fmt: ## Run code formatters
	ruff format src tests


lint: ## Run code linters inside Docker (with apache_beam available)
	docker run --rm --entrypoint sh -v "$(PWD)/src:/app/src" -v "$(PWD)/tests:/app/tests" ml-pipeline -c "ruff format src tests --check && ruff check src tests --fix && mypy src tests"

test: ## Run unit tests with coverage
	docker run --rm --entrypoint sh -v "$(PWD):/app" ml-pipeline -c "python -m pytest tests/unit --lf --durations=5 -c setup.cfg"

build:
	docker build -t ml-pipeline .

run-pipeline:
	docker run --rm -v "$(PWD):/app" ml-pipeline
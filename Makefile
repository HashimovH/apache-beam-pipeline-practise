.PHONY: test-unit

test-unit:
	pytest -q tests/unit -c setup.cfg


.PHONY: install install-prod lock-compile upgrade
install: ## Install dev requirements
	pip install -r requirements.dev.txt

install-prod: ## Install production requirements
	pip install -r requirements.txt

lock: ## Compile all requirements files
	pip-compile --no-emit-index-url --no-header --verbose requirements.in
	pip-compile --no-emit-index-url --no-header --verbose requirements.dev.in

upgrade: ## Upgrade requirements files
	pip-compile --no-emit-index-url --no-header --verbose --upgrade requirements.in
	pip-compile --no-emit-index-url --no-header --verbose --upgrade requirements.dev.in 


fmt: ## Run code formatters
	ruff format app tests

lint: ## Run code linters
	ruff format app tests --check
	ruff check app tests --fix
	mypy app tests

test: ## Run unit tests with coverage
	python -m pytest tests/unit --lf --durations=5 -c setup.cfg
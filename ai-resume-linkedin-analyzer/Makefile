.PHONY: help install setup test lint format run clean docker-build docker-up docker-down

# Variables
PYTHON := python3
PIP := pip3
PYTEST := pytest
BLACK := black
ISORT := isort
FLAKE8 := flake8
STREAMLIT := streamlit
UVICORN := uvicorn

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	$(PIP) install -r requirements.txt
	@echo "✓ Dependencies installed"

setup: install ## Setup complete environment
	$(PYTHON) -m spacy download en_core_web_lg
	$(PYTHON) scripts/init_db.py
	@echo "✓ Environment setup complete"

setup-dev: install ## Setup development environment
	$(PIP) install -r requirements.txt
	pre-commit install
	@echo "✓ Development environment ready"

test: ## Run all tests
	$(PYTEST) tests/ -v --cov=src --cov=app --cov-report=html --cov-report=term

test-unit: ## Run unit tests only
	$(PYTEST) tests/unit/ -v

test-integration: ## Run integration tests only
	$(PYTEST) tests/integration/ -v

test-watch: ## Run tests in watch mode
	$(PYTEST) tests/ -v --cov=src -f

coverage: ## Generate coverage report
	$(PYTEST) tests/ --cov=src --cov=app --cov-report=html
	@echo "✓ Coverage report generated in htmlcov/"

lint: ## Run all linters
	$(FLAKE8) src/ app/ api/ --max-line-length=100
	pylint src/ app/ api/ --max-line-length=100
	@echo "✓ Linting complete"

lint-fix: ## Fix linting issues automatically
	$(BLACK) src/ app/ api/ tests/
	$(ISORT) src/ app/ api/ tests/
	@echo "✓ Auto-fix complete"

format: ## Format code with black and isort
	$(BLACK) src/ app/ api/ tests/
	$(ISORT) src/ app/ api/ tests/
	@echo "✓ Code formatted"

type-check: ## Run type checking with mypy
	mypy src/ app/ --ignore-missing-imports
	@echo "✓ Type checking complete"

security: ## Run security checks
	bandit -r src/ app/ api/
	safety check
	@echo "✓ Security check complete"

run: ## Run Streamlit application
	$(STREAMLIT) run app/main.py

run-api: ## Run FastAPI application
	$(UVICORN) api.main:app --reload --host 0.0.0.0 --port 8000

run-prod: ## Run in production mode
	$(STREAMLIT) run app/main.py --server.port 8501 --server.address 0.0.0.0

docker-build: ## Build Docker images
	docker-compose build
	@echo "✓ Docker images built"

docker-up: ## Start Docker containers
	docker-compose up -d
	@echo "✓ Docker containers started"
	@echo "Streamlit: http://localhost:8501"
	@echo "FastAPI: http://localhost:8000"
	@echo "Grafana: http://localhost:3000"

docker-down: ## Stop Docker containers
	docker-compose down
	@echo "✓ Docker containers stopped"

docker-logs: ## Show Docker logs
	docker-compose logs -f

docker-restart: ## Restart Docker containers
	docker-compose restart

docker-clean: ## Remove Docker containers and volumes
	docker-compose down -v
	docker system prune -f
	@echo "✓ Docker cleaned"

init-db: ## Initialize database
	$(PYTHON) scripts/init_db.py
	@echo "✓ Database initialized"

seed-data: ## Seed database with sample data
	$(PYTHON) scripts/seed_data.py
	@echo "✓ Database seeded"

backup-db: ## Backup database
	$(PYTHON) scripts/backup_data.py
	@echo "✓ Database backed up"

clean: ## Clean cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	@echo "✓ Cleaned"

clean-all: clean docker-clean ## Clean everything including Docker
	@echo "✓ Everything cleaned"

migrate: ## Run database migrations
	alembic upgrade head
	@echo "✓ Database migrated"

requirements: ## Generate requirements.txt from pyproject.toml
	pip freeze > requirements.txt
	@echo "✓ requirements.txt updated"

check: lint test ## Run all checks (lint + test)
	@echo "✓ All checks passed"

pre-commit: format lint test ## Run pre-commit checks
	@echo "✓ Pre-commit checks passed"

build: clean ## Build distribution packages
	$(PYTHON) -m build
	@echo "✓ Build complete"

install-package: build ## Install package locally
	$(PIP) install -e .
	@echo "✓ Package installed"

docs: ## Generate documentation
	cd docs && make html
	@echo "✓ Documentation generated"

serve-docs: docs ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8080

monitor: ## Show system monitoring
	docker-compose exec prometheus curl localhost:9090/metrics

logs-app: ## Show application logs
	tail -f logs/app.log

logs-error: ## Show error logs
	tail -f logs/errors.log

ps: ## Show running processes
	docker-compose ps

stats: ## Show project statistics
	@echo "=== Project Statistics ==="
	@echo "Python files:" $$(find . -name "*.py" | wc -l)
	@echo "Total lines:" $$(find . -name "*.py" -exec wc -l {} + | tail -1 | awk '{print $$1}')
	@echo "Tests:" $$(find tests -name "test_*.py" | wc -l)
	@echo "Commits:" $$(git rev-list --count HEAD 2>/dev/null || echo "N/A")

version: ## Show version information
	@echo "Python:" $$(python --version)
	@echo "Streamlit:" $$(streamlit version)
	@echo "Docker:" $$(docker --version)

.DEFAULT_GOAL := help
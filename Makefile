.PHONY: help install install-dev run test test-unit test-integration test-cov clean format lint migrate seed db-init docker-build docker-up docker-down

# Variables
PYTHON := ./venv/bin/python3
PIP := ./venv/bin/pip
PYTEST := ./venv/bin/pytest
ALEMBIC := ./venv/bin/alembic
UVICORN := ./venv/bin/uvicorn
BLACK := ./venv/bin/black
ISORT := ./venv/bin/isort
FLAKE8 := ./venv/bin/flake8
MYPY := ./venv/bin/mypy

help:
	@echo "Issue Tracker - Available Commands"
	@echo "===================================="
	@echo "Setup & Installation:"
	@echo "  make install          - Install production dependencies"
	@echo "  make install-dev      - Install development dependencies"
	@echo "  make db-init          - Initialize database"
	@echo "  make migrate          - Run database migrations"
	@echo "  make seed             - Seed database with sample data"
	@echo ""
	@echo "Development:"
	@echo "  make run              - Run development server"
	@echo "  make format           - Format code with black and isort"
	@echo "  make lint             - Run linting checks"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run all tests (unit + integration)"
	@echo "  make test-unit        - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make test-e2e         - Run end-to-end tests with Playwright"
	@echo "  make test-all         - Run all tests including E2E"
	@echo "  make test-cov         - Run tests with coverage report"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-up        - Start Docker containers"
	@echo "  make docker-down      - Stop Docker containers"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            - Remove generated files and cache"

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements-dev.txt

run:
	@if [ ! -f .env ]; then \
		echo "Creating .env file from .env.example..."; \
		cp .env.example .env; \
	fi
	@if [ ! -f issue_tracker.db ]; then \
		echo "Database not found. Initializing..."; \
		$(MAKE) db-init; \
		$(MAKE) migrate; \
		$(MAKE) seed; \
	fi
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

db-init:
	$(PYTHON) -m app.db.init_db

migrate:
	$(ALEMBIC) upgrade head

seed:
	$(PYTHON) -m app.db.seed_data

test:
	$(PYTEST) tests/unit/ tests/integration/ -v

test-unit:
	$(PYTEST) tests/unit/ -v

test-integration:
	$(PYTEST) tests/integration/ -v

test-e2e:
	$(PYTEST) tests/e2e/ -v --headed

test-e2e-headless:
	$(PYTEST) tests/e2e/ -v

test-all:
	$(PYTEST) -v

test-cov:
	$(PYTEST) tests/unit/ tests/integration/ --cov=app --cov-report=html --cov-report=term-missing

format:
	$(BLACK) .
	$(ISORT) .

lint:
	$(FLAKE8) app/ tests/
	$(MYPY) app/
	$(BLACK) --check .
	$(ISORT) --check-only .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

# Quick start command
start: install-dev db-init migrate seed run

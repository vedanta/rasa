.PHONY: install dev serve test test-api test-cli lint format clean help

help:
	@echo "RASA Development Commands"
	@echo ""
	@echo "  make install    Install package in editable mode"
	@echo "  make dev        Install with dev dependencies"
	@echo "  make serve      Start the API server with auto-reload"
	@echo "  make test       Run all tests"
	@echo "  make test-api   Run API tests only"
	@echo "  make test-cli   Run CLI tests only"
	@echo "  make lint       Run linter (ruff)"
	@echo "  make format     Format code (black + ruff)"
	@echo "  make clean      Remove cache and build artifacts"

install:
	pip install -e .

dev:
	pip install -e .
	pip install pytest-cov pre-commit

serve:
	uvicorn rasa.api.main:app --reload --port 8000

test:
	pytest -v

test-api:
	pytest tests/test_api_master.py -v -s

test-cli:
	pytest tests/test_cli_end_to_end.py -v -s

lint:
	ruff check .

format:
	black .
	ruff check --fix .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/

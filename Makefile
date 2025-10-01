.PHONY: help install dev run test lint format clean

# Default target
help:
	@echo "Resume Tailor AI - UV Package Manager Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  install     - Install dependencies using UV"
	@echo "  dev         - Install development dependencies"
	@echo "  run         - Run the development server"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code using black"
	@echo "  clean       - Clean up cache and build artifacts"
	@echo "  sync        - Sync dependencies with uv.lock"

# Install production dependencies
install:
	uv sync --no-dev

# Install all dependencies including development
dev:
	uv sync

# Run the development server
run:
	uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Alternative run using the script
run-script:
	uv run python scripts/dev.py

# Run tests
test:
	uv run pytest

# Run linting
lint:
	uv run ruff check .
	uv run ruff format --check .

# Format code
format:
	uv run black .
	uv run ruff format .

# Sync dependencies
sync:
	uv sync

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
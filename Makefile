# PhD Deep Read Workflow Makefile

.PHONY: help install install-dev test test-cov lint format type-check clean setup

# Default target
help:
	@echo "PhD Deep Read Workflow - Available targets:"
	@echo ""
	@echo "  install     - Install core dependencies"
	@echo "  install-dev - Install development dependencies"
	@echo "  test        - Run tests"
	@echo "  test-cov    - Run tests with coverage report"
	@echo "  lint        - Run linters (flake8)"
	@echo "  format      - Format code (black, isort)"
	@echo "  type-check  - Run type checking (mypy)"
	@echo "  check       - Run all checks (lint, format, type-check, test)"
	@echo "  clean       - Clean build artifacts and caches"
	@echo "  setup       - Full setup (install, install-dev, format)"
	@echo ""

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=scripts --cov-report=html --cov-report=term

# Code quality
lint:
	flake8 scripts/ tests/ --max-line-length=88 --extend-ignore=E203,W503

format:
	black scripts/ tests/
	isort scripts/ tests/

type-check:
	mypy scripts/

check: lint format type-check test

# Setup
setup: install install-dev format
	@echo "✅ Setup complete! Next steps:"
	@echo "   1. Install Tesseract OCR: brew install tesseract (macOS) or sudo apt install tesseract-ocr (Linux)"
	@echo "   2. Test the workflow: python scripts/extract.py --help"

# Cleanup
clean:
	rm -rf .pytest_cache/ .mypy_cache/ .coverage htmlcov/ build/ dist/ *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

# Development shortcuts
dev: install-dev
	@echo "Development dependencies installed"

run-test:
	python -m pytest tests/test_extract.py -v

run-extract:
	python scripts/extract.py --help

run-generate:
	python scripts/generate.py --help

run-canvas:
	python scripts/canvas.py --help

run-verify:
	python scripts/verify.py --help

# Documentation
docs-serve:
	mkdocs serve

docs-build:
	mkdocs build

# Package building
build:
	python -m build

publish-test:
	twine upload --repository testpypi dist/*

publish:
	twine upload dist/*
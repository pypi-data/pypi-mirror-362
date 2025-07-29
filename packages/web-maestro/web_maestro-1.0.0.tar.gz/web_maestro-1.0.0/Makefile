.PHONY: help install install-dev format lint check test test-cov clean build docs setup-hooks

# Default target
help:
	@echo "🌐 Web Maestro Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install package in editable mode"
	@echo "  make install-dev  Install with development dependencies"
	@echo "  make setup-hooks  Install pre-commit hooks"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format       Format code with Black and Ruff"
	@echo "  make lint         Run linting checks"
	@echo "  make check        Run all quality checks"
	@echo ""
	@echo "Testing:"
	@echo "  make test         Run tests"
	@echo "  make test-cov     Run tests with coverage"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean        Clean build artifacts"
	@echo "  make build        Build package"
	@echo "  make docs         Serve documentation"
	@echo ""
	@echo "Hatch Commands (recommended):"
	@echo "  hatch run format  Format code"
	@echo "  hatch run lint    Run linting"
	@echo "  hatch run check   Run all checks"
	@echo "  hatch run test    Run tests"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e ".[dev,all-providers]"
	playwright install

setup-hooks:
	pre-commit install
	pre-commit install --hook-type commit-msg

# Code quality targets
format:
	hatch run format

lint:
	hatch run lint

check:
	hatch run check

# Testing targets
test:
	hatch run test

test-cov:
	hatch run test-cov

# Maintenance targets
clean:
	hatch run clean

build:
	hatch build

docs:
	@echo "Documentation commands:"
	@echo "  - View README.md for main documentation"
	@echo "  - Check docs/ directory for detailed guides"
	@echo "  - Run 'python -m http.server 8000' in docs/ to serve locally"

# Development shortcuts
dev-setup: install-dev setup-hooks
	@echo "✅ Development environment ready!"
	@echo "Run 'make help' to see available commands"

# Quick quality check before commit
pre-commit: format lint
	@echo "✅ Pre-commit checks passed!"

# Full validation (like CI)
ci-check: check build
	@echo "✅ CI validation complete!"

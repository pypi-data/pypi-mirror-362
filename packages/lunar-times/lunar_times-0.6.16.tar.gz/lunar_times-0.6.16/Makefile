.PHONY: info setup install test test-coverage coverage-report coverage-html lint clean check run run-debug build status help ci dev-setup quick-check test-all-python test-github-actions pre-commit reset check-invisible check-invisible-detailed clean-invisible pre-publish-clean build-package check-package upload-test-pypi upload-pypi
.DEFAULT_GOAL := info

# Source file tracking
SRC_FILES := $(shell find src -name "*.py" 2>/dev/null || echo "")
TEST_FILES := $(shell find tests -name "*.py" 2>/dev/null || echo "")

# Dependency tracking
.venv/pyvenv.cfg: pyproject.toml
	$(call colorecho,$(YELLOW),Creating/updating virtual environment...)
	@uv sync --extra dev
	@touch .venv/pyvenv.cfg

# Project Configuration
PROJECT_NAME := lunar-times
PYTHON_VERSION := 3.8

# Colors for output (using printf for better compatibility)
# Set NO_COLOR=1 to disable colors
ifdef NO_COLOR
BLUE := 
GREEN := 
YELLOW := 
RED := 
RESET := 
else
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m
endif

# Color-aware echo function
define colorecho
	@printf "$(1)%s$(RESET)\n" "$(2)"
endef

# Default target - show available commands
info:
	$(call colorecho,$(BLUE),$(PROJECT_NAME) Development Makefile)
	@echo ""
	$(call colorecho,$(GREEN),Available targets:)
	@printf "  $(YELLOW)%s$(RESET)        %s\n" "info" "Show this help message (default)"
	@printf "  $(YELLOW)%s$(RESET)       %s\n" "setup" "Initial project setup and dependency installation"
	@printf "  $(YELLOW)%s$(RESET)     %s\n" "install" "Install/update dependencies"
	@printf "  $(YELLOW)%s$(RESET)        %s\n" "test" "Run the test suite"
	@printf "  $(YELLOW)%s$(RESET) %s\n" "test-coverage" "Run tests with coverage reporting"
	@printf "  $(YELLOW)%s$(RESET) %s\n" "coverage-report" "Generate detailed coverage report"
	@printf "  $(YELLOW)%s$(RESET) %s\n" "coverage-html" "Open coverage report in browser"
	@printf "  $(YELLOW)%s$(RESET)        %s\n" "lint" "Run code linting (flake8)"
	@printf "  $(YELLOW)%s$(RESET)       %s\n" "check" "Run all checks (lint + test + type check)"
	@printf "  $(YELLOW)%s$(RESET)         %s\n" "run" "Run the application interactively"
	@printf "  $(YELLOW)%s$(RESET)   %s\n" "run-debug" "Run the application in debug mode (El Paso, TX)"
	@printf "  $(YELLOW)%s$(RESET)       %s\n" "build" "Build the project (runs checks first)"
	@printf "  $(YELLOW)%s$(RESET)       %s\n" "clean" "Clean build artifacts and cache"
	@printf "  $(YELLOW)%s$(RESET)      %s\n" "status" "Show project status and configuration"
	@echo ""
	$(call colorecho,$(GREEN),Advanced targets:)
	@printf "  $(YELLOW)%s$(RESET)          %s\n" "ci" "Run continuous integration checks (check + build)"
	@printf "  $(YELLOW)%s$(RESET) %s\n" "quick-check" "Run quick development checks (lint + test)"
	@printf "  $(YELLOW)%s$(RESET) %s\n" "test-all-python" "Test with multiple Python versions (like CI)"
	@printf "  $(YELLOW)%s$(RESET) %s\n" "test-github-actions" "Test GitHub Actions workflows locally (requires act)"
	@printf "  $(YELLOW)%s$(RESET) %s\n" "pre-commit" "Run comprehensive pre-commit checks"
	@printf "  $(YELLOW)%s$(RESET) %s\n" "check-invisible" "Check for invisible characters in source files"
	@printf "  $(YELLOW)%s$(RESET) %s\n" "check-invisible-detailed" "Show detailed invisible character analysis (dry-run)"
	@printf "  $(YELLOW)%s$(RESET) %s\n" "clean-invisible" "Remove invisible characters from source files"
	@printf "  $(YELLOW)%s$(RESET) %s\n" "pre-publish-clean" "Proactive cleanup for PyPI publishing"
	@printf "  $(YELLOW)%s$(RESET)       %s\n" "reset" "Reset environment (clean + fresh install)"
	@echo ""
	$(call colorecho,$(GREEN),PyPI Publishing:)
	@printf "  $(YELLOW)%s$(RESET) %s\n" "build-package" "Build wheel and source distribution for PyPI"
	@printf "  $(YELLOW)%s$(RESET) %s\n" "check-package" "Validate package integrity with twine"
	@printf "  $(YELLOW)%s$(RESET)  %s\n" "upload-test-pypi" "Upload to Test PyPI (uses .env TWINE_PASSWORD_TEST)"
	@printf "  $(YELLOW)%s$(RESET)  %s\n" "upload-pypi" "Upload to production PyPI (uses .env TWINE_PASSWORD_PROD)"
	@echo ""
	$(call colorecho,$(GREEN),Usage examples:)
	@echo "  make setup     # First-time project setup"
	@echo "  make test      # Run tests"
	@echo "  make check     # Run all quality checks"
	@echo "  make run       # Run the lunar times calculator"
	@echo "  make ci        # Run CI pipeline (check + build)"
	@echo "  make upload-test-pypi # Test PyPI upload (requires .env with tokens)"
	@echo "  make upload-pypi # Production PyPI upload (requires confirmation)"

# Initial project setup
setup:
	$(call colorecho,$(BLUE),Setting up $(PROJECT_NAME)...)
	$(call colorecho,$(YELLOW),Installing Python $(PYTHON_VERSION)...)
	@uv python install $(PYTHON_VERSION)
	$(call colorecho,$(YELLOW),Installing dependencies...)
	@uv sync --extra dev
	$(call colorecho,$(GREEN),✓ Setup complete!)
	@echo ""
	$(call colorecho,$(BLUE),Next steps:)
	@echo "  make test      # Run tests to verify setup"
	@echo "  make run       # Run the application"

# Install/update dependencies
install: .venv/pyvenv.cfg
	$(call colorecho,$(GREEN),✓ Dependencies updated)

# Development setup (alias for convenience)
dev-setup: install

# Run tests
test: install
	$(call colorecho,$(BLUE),Running test suite...)
	@uv run --extra dev python -m pytest tests/ -v
	$(call colorecho,$(GREEN),✓ Tests completed)

# Run tests with coverage
test-coverage: install
	$(call colorecho,$(BLUE),Running tests with coverage...)
	@uv run --extra dev python -m pytest tests/ --cov=src/lunar_times --cov-report=term-missing
	$(call colorecho,$(GREEN),✓ Tests with coverage completed)

# Generate coverage report
coverage-report: install
	$(call colorecho,$(BLUE),Generating coverage report...)
	@uv run --extra dev python -m pytest tests/ --cov=src/lunar_times --cov-report=term-missing --cov-report=html
	$(call colorecho,$(GREEN),✓ Coverage report generated in htmlcov/)

# Open coverage report in browser
coverage-html: coverage-report
	$(call colorecho,$(BLUE),Opening coverage report...)
	@python -m webbrowser htmlcov/index.html || open htmlcov/index.html || xdg-open htmlcov/index.html

# Run linting
lint: install
	$(call colorecho,$(BLUE),Running code linting...)
	@if [ -n "$(SRC_FILES)" ]; then uv run --extra dev flake8 $(SRC_FILES); fi
	@if [ -n "$(TEST_FILES)" ]; then uv run --extra dev flake8 $(TEST_FILES); fi
	$(call colorecho,$(GREEN),✓ Linting completed)



# Type checking
typecheck: install
	$(call colorecho,$(BLUE),Running type checking...)
	@if [ -n "$(SRC_FILES)" ]; then uv run --extra dev mypy $(SRC_FILES); fi
	$(call colorecho,$(GREEN),✓ Type checking completed)

# Run all checks
check: lint typecheck test check-invisible
	$(call colorecho,$(GREEN),✓ All checks passed!)

# Run the application
run: install
	$(call colorecho,$(BLUE),Running $(PROJECT_NAME)...)
	@uv run lunar-times

# Run in debug mode
run-debug: install
	$(call colorecho,$(BLUE),Running $(PROJECT_NAME) in debug mode (El Paso TX)...)
	@uv run lunar-times -d

# Build marker for tracking
.build-marker: $(SRC_FILES) pyproject.toml
	$(call colorecho,$(BLUE),Source files changed - running checks...)
	@$(MAKE) check
	$(call colorecho,$(BLUE),Building $(PROJECT_NAME)...)
	@uv build
	@touch .build-marker
	$(call colorecho,$(GREEN),✓ Build completed)

# Build the project (smart rebuild based on source changes)
build: .build-marker
	$(call colorecho,$(GREEN),✓ Build is up to date)

# Clean build artifacts and cache
clean:
	$(call colorecho,$(BLUE),Cleaning build artifacts...)
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info/
	@rm -rf .pytest_cache/
	@rm -rf __pycache__/
	@rm -rf .mypy_cache/
	@rm -rf htmlcov/
	@rm -f .coverage
	@rm -f .build-marker
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find src tests -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find src tests -name "*.pyc" -type f -delete 2>/dev/null || true
	$(call colorecho,$(GREEN),✓ Cleanup completed)

# Show project status
status:
	$(call colorecho,$(BLUE),$(PROJECT_NAME) Status)
	@echo ""
	$(call colorecho,$(YELLOW),Python Environment:)
	@uv run python --version
	@echo ""
	$(call colorecho,$(YELLOW),Project Version:)
	@grep "version.*=" pyproject.toml
	@echo ""
	$(call colorecho,$(YELLOW),Dependencies Status:)
	@echo "Runtime dependencies:"
	@uv run pip list | grep -E "(requests|geopy|timezonefinder|pytz)" || echo "  Dependencies not installed"
	@echo "Dev dependencies:"
	@uv run --extra dev python -c "import pytest, black, flake8, mypy; print(f'  pytest=={pytest.__version__}, black=={black.__version__}, flake8=={flake8.__version__}, mypy installed')" 2>/dev/null || echo "  Dev dependencies not fully installed"
	@echo ""
	$(call colorecho,$(YELLOW),Test Status:)
	@if [ -d "tests" ] && [ -n "$(TEST_FILES)" ]; then \
		echo "  ✓ Test suite available"; \
		uv run --extra dev python -c "import sys; sys.path.insert(0, 'tests'); import test_cli; tests = [m for cls in [test_cli.TestMoonData, test_cli.TestIntegration] for m in dir(cls) if m.startswith('test_')]; print(f'  {len(tests)} unit tests found')" 2>/dev/null || echo "  Test count unavailable"; \
	else \
		echo "  ✗ No test suite found"; \
	fi
	@echo ""
	$(call colorecho,$(YELLOW),Configuration:)
	@echo "  Python requirement: $(shell grep 'requires-python' pyproject.toml | cut -d'=' -f2 | tr -d ' \"')"
	@echo "  Target Python: $(PYTHON_VERSION)"

# Continuous Integration pipeline
ci: check build
	$(call colorecho,$(GREEN),✓ CI pipeline completed successfully!)



# Quick development check (faster than full check)
quick-check: lint test check-invisible
	$(call colorecho,$(GREEN),✓ Quick check completed!)

# Test with multiple Python versions (like GitHub Actions CI)
test-all-python:
	$(call colorecho,$(BLUE),Testing with multiple Python versions...)
	@if [ ! -f scripts/test_all_python.sh ]; then \
		echo "Error: scripts/test_all_python.sh not found"; \
		exit 1; \
	fi
	@chmod +x scripts/test_all_python.sh
	@./scripts/test_all_python.sh

# Test GitHub Actions workflows locally (requires act tool)
test-github-actions:
	$(call colorecho,$(BLUE),Testing GitHub Actions workflows locally...)
	@if [ ! -f scripts/test_github_actions_local.sh ]; then \
		echo "Error: scripts/test_github_actions_local.sh not found"; \
		exit 1; \
	fi
	@chmod +x scripts/test_github_actions_local.sh
	@./scripts/test_github_actions_local.sh

# Comprehensive pre-commit checks (recommended before every commit)
pre-commit: check
	$(call colorecho,$(GREEN),✓ Pre-commit checks completed!)
	$(call colorecho,$(BLUE),Recommendation: Run 'make test-all-python' before major commits)

# Reset environment (clean + fresh install)
reset: clean
	$(call colorecho,$(BLUE),Resetting environment...)
	@rm -rf .venv/
	@make install
	$(call colorecho,$(GREEN),✓ Environment reset completed!)

# Invisible Character Management
# See docs: scripts/invisible_chars_commands.md for manual detection methods
check-invisible:
	$(call colorecho,$(BLUE),Checking for invisible characters...)
	$(call colorecho,$(YELLOW),Reference: scripts/invisible_chars_commands.md for manual methods)
	@python scripts/clean_invisible_chars.py src
	@python scripts/clean_invisible_chars.py docs
	@python scripts/clean_invisible_chars.py tests
	@python scripts/clean_invisible_chars.py pyproject.toml
	$(call colorecho,$(GREEN),✓ Invisible character check completed)

# Detailed invisible character check (shows what would be cleaned)
check-invisible-detailed:
	$(call colorecho,$(BLUE),Detailed invisible character check...)
	$(call colorecho,$(YELLOW),Showing what would be cleaned without making changes)
	@python scripts/clean_invisible_chars.py src --dry-run
	@python scripts/clean_invisible_chars.py docs --dry-run
	@python scripts/clean_invisible_chars.py tests --dry-run
	@python scripts/clean_invisible_chars.py pyproject.toml --dry-run
	$(call colorecho,$(GREEN),✓ Detailed invisible character check completed)

# Clean invisible characters proactively (with backup)
clean-invisible:
	$(call colorecho,$(BLUE),Cleaning invisible characters...)
	$(call colorecho,$(YELLOW),Creating backups before cleaning (see scripts/invisible_chars_commands.md))
	@python scripts/clean_invisible_chars.py src --clean
	@python scripts/clean_invisible_chars.py docs --clean
	@python scripts/clean_invisible_chars.py tests --clean
	@python scripts/clean_invisible_chars.py pyproject.toml --clean
	$(call colorecho,$(GREEN),✓ Invisible character cleanup completed)

# Proactive invisible character cleanup for publishing
pre-publish-clean: clean-invisible
	$(call colorecho,$(BLUE),Running proactive cleanup for publishing...)
	$(call colorecho,$(YELLOW),Source files cleaned of invisible characters via clean-invisible target)
	$(call colorecho,$(GREEN),✓ Pre-publish cleanup completed)

# PyPI Package Building and Publishing
build-package: .venv/pyvenv.cfg clean pre-publish-clean
	$(call colorecho,$(BLUE),Building package for PyPI...)
	$(call colorecho,$(YELLOW),Package cleaned of invisible characters)
	@uv build
	$(call colorecho,$(GREEN),✓ Package built in dist/)

check-package: build-package
	$(call colorecho,$(BLUE),Checking package integrity...)
	@uv run twine check dist/*
	$(call colorecho,$(GREEN),✓ Package checks passed)

upload-test-pypi: check-package
	$(call colorecho,$(BLUE),Uploading to Test PyPI...)
	$(call colorecho,$(YELLOW),Loading environment from .env file if it exists...)
	@if [ -f .env ]; then export $$(cat .env | grep -v '^#' | xargs) && export TWINE_PASSWORD=$$TWINE_PASSWORD_TEST; fi; \
	uv run twine upload --repository testpypi dist/*
	$(call colorecho,$(GREEN),✓ Uploaded to Test PyPI)

upload-pypi: check-package
	$(call colorecho,$(RED),WARNING: This will upload to the REAL PyPI!)
	$(call colorecho,$(YELLOW),Loading environment from .env file if it exists...)
	@read -p "Are you sure you want to upload to PyPI? (y/N): " confirm && [ "$$confirm" = "y" ]
	@if [ -f .env ]; then export $$(cat .env | grep -v '^#' | xargs) && export TWINE_PASSWORD=$$TWINE_PASSWORD_PROD; fi; \
	uv run twine upload dist/*
	$(call colorecho,$(GREEN),✓ Uploaded to PyPI)

# Help alias
help: info
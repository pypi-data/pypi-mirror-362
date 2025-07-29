# Makefile for Python quality automation

.DEFAULT_GOAL := help

# Variable for passing command-line arguments to run targets
ARGS ?=

# === Help ===

help:
	@echo "Available commands:"
	@echo ""
	@echo "  \033[1mUsage\033[0m: make [target]"
	@echo ""
	@echo "  \033[1mInstallation\033[0m:"
	@echo "    install          - Install project dependencies for development"
	@echo ""
	@echo "  \033[1mQuality & Testing\033[0m:"
	@echo "    lint             - Run Ruff linter"
	@echo "    format           - Run Ruff formatter"
	@echo "    mypy             - Run mypy type checker"
	@echo "    test             - Run pytest"
	@echo "    cc               - Report cyclomatic complexity"
	@echo "    mi               - Report maintainability index"
	@echo "    quality          - Run all static analysis checks (lint, mypy, radon)"
	@echo "    check            - Run all checks including tests and build"
	@echo ""
	@echo "  \033[1mBuild & Distribution\033[0m:"
	@echo "    build            - Build the wheel and sdist packages"
	@echo "    publish          - Publish the package to PyPI"
	@echo "    clean            - Remove build artifacts and temporary files"
	@echo ""
	@echo "  \033[1mProject Execution\033[0m:"
	@echo "    run-<app>        - Run a specific application (e.g., make run-loancalc)"
	@echo ""
	@echo "  \033[1mNote\033[0m: For execution targets, pass arguments via ARGS, e.g.:"
	@echo "    make run-loancalc ARGS=\"annuity --principal 100k\""

# === Installation ===

install:
	uv pip install -e .[dev]

# === Linting and formatting ===

lint:
	uv run ruff check . $(ARGS)

format:
	uv run ruff format .

# === Static typing ===

mypy:
	uv run mypy src/ --install-types

# === Testing ===

test:
	uv run pytest $(ARGS)

# === Code metrics ===

cc:
	uv run radon cc src/ --show-complexity --average --total-average

mi:
	uv run radon mi --show --sort src/

# === Build and Publishing ===

build:
	@echo "📦 Building wheel and sdist with uv into dist/..."
	@uv build

publish-test:
	@echo "🚀 Publishing artifacts to TestPyPI..."
	@uv publish --index testpypi

publish:
	@echo "🚀 Publishing artifacts to PyPI..."
	@uv publish

# The "super-clean" or "distclean" pattern is sometimes used for a more
# aggressive cleanup that also removes the virtual environment, but our
# current `clean` is safer for typical development workflows.
clean:
	@echo "🧹 Cleaning up build artifacts, caches, and temporary files..."
	# Remove Python cache files and compiled bytecode
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -exec rm -rf {} +

	# Remove build artifacts
	@rm -rf dist/ build/ *.egg-info/ .eggs/

	# Remove test and coverage reports/caches
	@rm -rf .pytest_cache/ .coverage

	# Remove static analysis and formatter caches
	@rm -rf .mypy_cache/ .ruff_cache/

	# Remove OS-specific metadata (like macOS .DS_Store)
	@find . -name '.DS_Store' -type f -delete

#distclean: clean
#	@echo "🧹 Removing all git-ignored files and directories..."
#    @git clean -fdX

# === Project Execution ===
# Use a pattern rule to handle all 'run-*' targets dynamically.
# Example: make run-loancalc ARGS="..."

run-%:
	@uv run $* $(ARGS)

# === Quality Aggregation ===

quality: lint mypy cc mi

check: quality test build

.PHONY: help install lint format mypy test cc mi quality check build publish clean distclean
.PHONY: run-loancalc run-hangman run-rps run-billsplitter run-chatbot run-coffeemachine
.PHONY: run-honestcalc run-zookeeper

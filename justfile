# Default command: List all available commands
default:
    @just --list

# Install all dependencies
install:
    echo "📦 Installing dependencies..."
    uv sync

# Update all dependencies
update:
    echo "🔄 Updating dependencies..."
    uv lock --upgrade

# Build workspace packages
build:
    echo "🏗️ Building workspace packages..."
    uv sync --all-packages

# Spin up Docker containers
up:
    echo "🚀 Spinning up Docker containers and attaching to logs..."
    docker compose up -d && docker compose logs -f

# Tear down Docker containers
down:
    echo "🛑 Tearing down Docker containers..."
    docker compose down

# Run tests
test:
    echo "✅ Running tests..."
    uv run pytest

# Run tests with coverage
test-cov:
    echo "📊 Running tests with coverage..."
    uv run pytest --cov=housing-price-orchestrator/src

# Run tests and generate HTML coverage report
test-html:
    echo "🌐 Running tests and generating HTML coverage report..."
    uv run pytest --cov=housing-price-orchestrator/src --cov-report=html

# Lint code
lint:
    echo "🔍 Linting code..."
    uv run ruff check .

# Lint and fix code
lint-fix:
    echo "🔧 Linting and fixing code..."
    uv run ruff check . --fix

# Format code
format:
    echo "✨ Formatting code..."
    uv run ruff format .

# Check formatting
format-check:
    echo "🧐 Checking formatting..."
    uv run ruff format --check .

# Pre-commit hooks
pre-commit-install:
    echo "🔧 Installing pre-commit hooks..."
    pre-commit install

pre-commit:
    echo "🚀 Running pre-commit hooks..."
    pre-commit run --all-files


# Run tests, linting, and formatting check
check: lint format-check test pre-commit
    echo "🎉 All checks passed!"

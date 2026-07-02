# Project Overview
A microservices architecture for orchestrating housing price regression models.

## Build and Test Commands
These commands are available via `just`:

- `just install`: Install all dependencies using `uv sync`.
- `just update`: Update all dependencies using `uv lock --upgrade`.
- `just build`: Build workspace packages.
- `just up`: Spin up Docker containers and attach to logs.
- `just down`: Tear down Docker containers.
- `just test`: Run unit and integration tests using `pytest`.
- `just test-cov`: Run tests with coverage.
- `just test-html`: Run tests and generate an HTML coverage report.
- `just lint`: Run `ruff` check.
- `just lint-fix`: Run `ruff` check and fix issues.
- `just format`: Format code using `ruff` format.
- `just format-check`: Check if the code follows formatting rules.
- `just pre-commit-install`: Install pre-commit hooks.
- `just pre-commit`: Run all pre-commit hooks.
- `just check`: Run linting, formatting check, tests, and pre-commit hooks.

## Architecture and Directory Layout
The project is organized into several main components:

- `housing-price-orchestrator/`: The core service for orchestrating price predictions.
    - `src/provider`: Handles interaction with MLFlow model providers.
    - `src/service`: Contains the primary business logic for pricing services.
    - `src/shared`: Common code shared across the orchestrator, including:
        - `config`: Configuration loading and management.
        - `dto`: Data Transfer Objects.
        - `view`: Request/Response views.
    - `tests`: Unit and integration tests for the orchestrator service.
- `housing-price-model/`: Contains the logic for building and serving the ML model.
- `mlflow-server/`: Infrastructure for serving the MLFlow model.

## Main Repository Conventions
- **Language**: Python 3.13+
- **Tooling**: `uv` for package management, `pydantic` for data validation, `ruff` for linting and formatting.
- **Docstrings**: Use Google-style docstrings for functions and classes.
- **Configuration**: Use `config.yaml` for environment-specific settings, supporting `${VAR_NAME:default}` syntax for environment variable interpolation.
- **Typing**: Mandatory type hints for all function signatures and variable definitions.

## Testing Standards
- **Unit Tests**: Located in `tests/unit/`.
- **Integration Tests**: Located in `tests/integration/`.
- **Pattern**: Follow the `GIVEN / WHEN / THEN` structure for test cases.
- **Mocking**: Use `pytest-mock` for isolating dependencies.
- **Coverage**: Maintain high coverage as verified by `just test-cov`.

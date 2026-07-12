# Housing Price UI

Streamlit-based web interface for the housing price prediction orchestrator.

## Overview

This application provides a user-friendly form to input property details and get price predictions by communicating with the [housing-price-orchestrator](../housing-price-orchestrator/) via HTTP.

## Quick Start

### Local Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest -v

# Start the Streamlit app
uv run streamlit run src/main.py --server.port 8501
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ORCHESTRATOR_URL` | `http://localhost:8000` | Base URL of the orchestrator API |

### Docker

```bash
# Build
docker build --build-arg project_root=. -t housing-price-ui .

# Run
docker run -p 8501:8501 -e ORCHESTRATOR_URL=http://host.docker.internal:8000 housing-price-ui
```

## Project Structure

```
housing-price-ui/
├── src/
│   ├── config/
│   │   └── settings.py      # Pydantic settings (env-based config)
│   ├── client/
│   │   └── orchestrator_client.py  # Async HTTP client for orchestrator
│   ├── models/
│   │   └── prediction_models.py    # Pydantic request/response models
│   ├── ui/
│   │   └── app.py         # Streamlit UI with form and prediction logic
│   └── main.py            # Entry point
├── tests/
│   ├── unit/
│   │   ├── test_app.py
│   │   ├── test_orchestrator_client.py
│   │   ├── test_prediction_models.py
│   │   └── test_settings.py
│   └── integration/
├── Dockerfile
├── pyproject.toml
└── README.md
```

## Architecture

- **Models** ([prediction_models.py](src/models/prediction_models.py)) — Pydantic models mirroring the orchestrator's request/response schema with serialization aliases
- **Config** ([settings.py](src/config/settings.py)) — Environment-based configuration via `pydantic-settings`
- **Client** ([orchestrator_client.py](src/client/orchestrator_client.py)) — Async `httpx` client for single and batch predictions
- **UI** ([app.py](src/ui/app.py)) — Streamlit form organized into expandable sections (Sales, Lot, Neighborhood, Structure, Exterior, Basement, Heating, Living Space, Garage, Porch)

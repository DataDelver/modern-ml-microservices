FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Copy the project into the image
ADD . /app

WORKDIR /app

# Sync the project into a new environment, using the frozen lockfile
RUN uv sync --frozen --no-dev

WORKDIR /app/src

CMD ["uv", "run", "fastapi", "run", "main.py", "--port", "80"]
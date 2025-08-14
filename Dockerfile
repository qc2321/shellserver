# Use Python slim image as base
FROM python:3.11-slim

# Install uv by copying from the official distroless image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Install system dependencies that might be needed for shell commands
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies (excluding the project itself for better caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# Copy the entire project
COPY . .

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Expose any port if needed (MCP typically uses stdin/stdout, but keeping for flexibility)
# EXPOSE 8000

# Set the command to run the server using uv
CMD ["uv", "run", "server.py"]

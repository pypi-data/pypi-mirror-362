# docker/Dockerfile
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Development stage
FROM base as development

WORKDIR /app

# Copy project files
COPY . .

# Install development dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -e ".[dev,docs]"

# Set up pre-commit
RUN . .venv/bin/activate && pre-commit install

EXPOSE 8000 8501

CMD ["/bin/bash"]

# Production stage
FROM base as production

WORKDIR /app

# Copy only necessary files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY README.md LICENSE ./

# Install production dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -e ".[prod]"

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["/bin/bash", "-c", "source .venv/bin/activate && uvicorn openrxn_perovskite_optimizer.api.main:app --host 0.0.0.0 --port 8000"]
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-dev

COPY src ./src
COPY alembic ./alembic
COPY alembic.ini ./

# CMD ["uv", "run", "python", "-m", "enterprise_incident_mcp.web_server"]
CMD ["sh", "-c", "uv run uvicorn enterprise_incident_mcp.web_server:app --host 0.0.0.0 --port ${PORT:-8000}"]
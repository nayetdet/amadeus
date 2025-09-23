# Build Stage
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential=12.9 \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Runtime Stage
FROM python:3.10-slim-bookworm
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
COPY --from=builder --chown=app:app /app /app
EXPOSE 8000
CMD ["uvicorn", "src.amadeus.main:app", "--host", "0.0.0.0", "--port", "8000"]

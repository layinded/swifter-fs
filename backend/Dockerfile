# Use a lightweight Python base image
FROM python:3.10

# Set working directory
WORKDIR /app/

# Set environment variables
# Set Python path so it can find `app`
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install uv (Fast dependency management)
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/
ENV PATH="/app/.venv/bin:$PATH"

# Setup a virtual environment
RUN python -m venv .venv

# Install dependencies
COPY uv.lock pyproject.toml /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv .venv && uv sync --frozen --no-install-project

# Copy application files
COPY ./scripts /app/scripts
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY ./app /app/app
COPY ./custom /app/custom

# Expose the FastAPI default port
EXPOSE 8000

# Final command to start the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

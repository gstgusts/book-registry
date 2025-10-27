# syntax=docker/dockerfile:1

# --- Builder: install dependencies into a virtualenv for a clean runtime layer
FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app

# Install build tools only if needed (current deps are pure-Python; keep minimal)
# If you later add packages that require compilation (e.g., psycopg2, Pillow), uncomment:
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#  && rm -rf /var/lib/apt/lists/*

# Layer caching: copy only requirements first
COPY requirements.txt ./
RUN python -m venv /opt/venv \
 && /opt/venv/bin/pip install --upgrade pip \
 && /opt/venv/bin/pip install -r requirements.txt

# --- Runtime: slim image with only the app and the virtualenv
FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /opt/venv /opt/venv

# Copy the application code
# Contains: app/ package, templates/, config.py, run.py, etc.
COPY . /app

# Ensure the app directory is writable for SQLite db (config defaults to /app/app.db)
RUN chown -R appuser:appuser /app

# Expose port (informational)
EXPOSE 8000

# Optional healthcheck that verifies the TCP port is accepting connections
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD python -c "import os, socket; s=socket.create_connection(('127.0.0.1', int(os.getenv('PORT','8000'))), 2); s.close()"

USER appuser

# Start with Gunicorn using the Flask app factory (create_app in app/__init__.py)
# If you prefer using run:app, replace the target with "run:app".
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "-k", "gthread", "--threads", "8", "app:create_app()"]

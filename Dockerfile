# Dockerfile for Sudoku Backend (FastAPI)
FROM python:3.12-slim

# Prevents Python from writing .pyc, ensures stdout flushing
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies first (better caching)
COPY backend/src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy backend source
COPY backend/src /app/src

# Expose the FastAPI port
EXPOSE 8000

# Run using FastAPI's built-in CLI
CMD ["python", "-m", "fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
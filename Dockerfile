# Dockerfile (backend)
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*

# ✅ Correct requirements path
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# App code
COPY backend/src /app/src

# Bind to App Runner port (default 8080)
ENV PORT=8080
EXPOSE 8080

# Use uvicorn (ships via fastapi[standard] or uvicorn[standard])
CMD sh -c "python -m uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}"
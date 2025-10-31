# ---- Base Image ----
FROM python:3.11-slim

# ---- Security & Env ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ---- Working Directory ----
WORKDIR /app

# ---- System Dependencies ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl && \
    rm -rf /var/lib/apt/lists/*

# ---- Install Python Dependencies ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy Source Code ----
COPY app.py sentiment.py ./

# ---- Non-root User ----
RUN useradd -m appuser
USER appuser

# ---- Expose Port ----
EXPOSE 5002

# ---- Gunicorn Entrypoint ----
CMD ["gunicorn", "--workers", "4", "--threads", "2", "--timeout", "120", \
     "--bind", "0.0.0.0:5002", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
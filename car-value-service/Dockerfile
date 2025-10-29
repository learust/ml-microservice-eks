FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py price.py ./
COPY data ./data
EXPOSE 5001

# Run with gunicorn for production
# --workers 2: Use 2 worker processes
# --worker-class gthread: Use threaded workers for better I/O handling
# --threads 2: Each worker handles 2 threads (total 4 concurrent handlers)
# --timeout 60: Allow 60s for ML model processing
# --bind 0.0.0.0:5001: Listen on all interfaces on port 5001
# --access-logfile -: Log access to stdout
# --error-logfile -: Log errors to stdout
CMD ["gunicorn", "--workers", "2", "--worker-class", "gthread", "--threads", "2", "--timeout", "60", "--bind", "0.0.0.0:5001", "--access-logfile", "-", "--error-logfile", "-", "app:app"]

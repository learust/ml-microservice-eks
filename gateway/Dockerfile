# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the gateway port
EXPOSE 5000

# Run the API gateway with gunicorn to handle multiple requests
# --workers 4: Use 4 worker processes for handling concurrent requests
# --worker-class gthread: Use threaded workers for better I/O handling
# --threads 2: Each worker handles 2 threads (total 8 concurrent handlers)
# --timeout 120: Allow 120s for requests (ML model + sentiment analysis)
# --bind 0.0.0.0:5000: Listen on all interfaces on port 5000
# --access-logfile -: Log access to stdout
# --error-logfile -: Log errors to stdout
CMD ["gunicorn", "--workers", "4", "--worker-class", "gthread", "--threads", "2", "--timeout", "120", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
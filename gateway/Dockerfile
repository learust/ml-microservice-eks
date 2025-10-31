# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the gateway port (Flask default)
EXPOSE 5000

# Run the API gateway Flask app
CMD ["gunicorn", "--workers", "4", "--worker-class", "gthread", "--threads", "2", "--timeout", "120", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
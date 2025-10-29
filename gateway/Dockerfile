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
CMD ["python", "app.py"]
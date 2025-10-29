FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py sentiment.py ./
EXPOSE 5002
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5002", "app:app"]
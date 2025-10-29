FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py price.py ./
COPY data ./data
EXPOSE 5001
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5001", "app:app"]

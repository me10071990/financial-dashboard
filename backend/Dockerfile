# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Upgrade pip first
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["flask", "run"]

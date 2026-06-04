---
name: Deploy Flask App
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Step-by-step workflow to deploy a Flask application. Covers Dockerization, Gunicorn configuration, nginx reverse proxy, environment variables, health checks, and CI/CD pipeline.
tags: [workflow, flask, deployment, docker, gunicorn, nginx, ci-cd]
role: devops-engineer
---

# Deploy Flask App

## 1. Prepare Application

### Environment Variables

```bash
# .env
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@db:5432/myapp
REDIS_URL=redis://cache:6379/0
```

### Health Check Endpoint

```python
# app/health.py
from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "checks": {
            "database": check_db(),
            "redis": check_redis()
        }
    }), 200
```

## 2. Dockerize

### Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn.conf.py", "run:app"]
```

### Gunicorn Config

```python
# gunicorn.conf.py
import os

bind = "0.0.0.0:8000"
workers = int(os.environ.get("WEB_CONCURRENCY", 4))
worker_class = "uvicorn.workers.UvicornWorker"  # If using async
worker_connections = 1000
keepalive = 2
timeout = 30
graceful_timeout = 30
preload_app = True

accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info")
```

## 3. Nginx Reverse Proxy

```nginx
# nginx.conf
upstream app {
    server app:8000;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    location /static {
        alias /var/www/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /health {
        proxy_pass http://app/health;
        access_log off;
    }
}
```

## 4. Docker Compose Stack

```yaml
version: "3.8"

services:
  app:
    build: .
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/myapp
      - REDIS_URL=redis://cache:6379/0
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - static_files:/var/www/static
    depends_on:
      - app

volumes:
  postgres_data:
  static_files:
```

## 5. CI/CD Pipeline (GitHub Actions)

```yaml
name: Deploy Flask App

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest --cov=app --cov-report=xml
      - uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          echo "${{ secrets.SSH_KEY }}" > key.pem
          chmod 600 key.pem
          ssh -i key.pem -o StrictHostKeyChecking=no user@server "cd /app && docker-compose pull && docker-compose up -d"
```

## 6. SSL/TLS (Let's Encrypt)

```bash
docker run --rm \
  -v "$(pwd)/certbot-data:/etc/letsencrypt" \
  -v "$(pwd)/certbot-www:/var/www/certbot" \
  certbot/certbot certonly \
  --webroot -w /var/www/certbot \
  -d example.com -d www.example.com
```

## 7. Rollback Procedure

```bash
# Tag current deployment
docker tag myapp:latest myapp:backup-$(date +%Y%m%d)

# Deploy new version
docker-compose up -d

# If issues detected:
docker-compose stop app
docker tag myapp:backup-$(date +%Y%m%d) myapp:latest
docker-compose up -d app
```

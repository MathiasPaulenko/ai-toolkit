---
name: Flask API
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Production-grade skill for building REST APIs with Flask. Covers app factory, blueprints, extensions, configuration, testing, serialization, error handling, pagination, Docker, and deployment.
tags: [flask, python, rest-api, backend, microservices, web]
trigger: When the user asks to create, refactor, fix, or explain a Flask REST API, app factory, blueprints, extensions, configuration, testing, serialization, or deployment.
min_version: 2.3.0
---

# Flask API Skill

## Description

Comprehensive skill for building production-ready REST APIs with Flask. Covers the modern Application Factory pattern, Blueprint-based routing, popular extensions, environment-based configuration, request validation, serialization, error handling, pagination, testing with pytest, and Docker deployment.

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Application Factory](#2-application-factory)
3. [Configuration](#3-configuration)
4. [Blueprints](#4-blueprints)
5. [Extensions](#5-extensions)
6. [Request Validation & Serialization](#6-request-validation--serialization)
7. [Error Handling](#7-error-handling)
8. [Pagination](#8-pagination)
9. [Authentication](#9-authentication)
10. [Testing](#10-testing)
11. [Docker & Deployment](#11-docker--deployment)
12. [Best Practices Checklist](#12-best-practices-checklist)
13. [Common Pitfalls](#13-common-pitfalls)
14. [References](#14-references)

## When to Invoke

- Creating or refactoring a Flask REST API project
- Implementing the Application Factory pattern
- Organizing routes with Blueprints
- Integrating Flask extensions (SQLAlchemy, Migrate, JWT, CORS, Marshmallow)
- Setting up environment-based configuration (dev, test, prod)
- Validating and serializing API requests/responses
- Implementing custom error handlers and consistent JSON responses
- Adding pagination to list endpoints
- Setting up authentication (JWT, API keys)
- Writing tests with pytest and the Flask test client
- Dockerizing and deploying a Flask application

---

## 1. Project Setup

### Directory Layout

```
project/
  app/
    __init__.py           # create_app() factory
    config.py             # Config classes
    extensions.py         # Initialized extensions
    api/
      __init__.py         # Blueprint registration
      users.py            # User routes
      posts.py            # Post routes
    models/
      __init__.py
      user.py
      post.py
    schemas/
      __init__.py
      user_schema.py
    utils/
      __init__.py
      responses.py        # Standardized JSON responses
      pagination.py
    tests/
      conftest.py         # Pytest fixtures
      test_users.py
      test_posts.py
  migrations/             # Flask-Migrate
  Dockerfile
  docker-compose.yml
  requirements.txt
  .env                    # Local secrets (not committed)
  .flaskenv               # FLASK_APP, FLASK_ENV
  wsgi.py                 # Entry point for production
```

### Installation

```bash
pip install "Flask>=2.3.0"

# Core extensions for REST APIs
pip install Flask-SQLAlchemy Flask-Migrate Flask-JWT-Extended Flask-CORS Flask-Marshmallow marshmallow-sqlalchemy

# Validation
pip install pydantic email-validator

# Testing
pip install pytest pytest-flask factory-boy

# Production server
pip install gunicorn
```

### .flaskenv

```bash
FLASK_APP=wsgi.py
FLASK_DEBUG=1
```

---

## 2. Application Factory

The Application Factory is the modern pattern for Flask. It enables multiple app instances with different configurations and simplifies testing.

```python
# app/__init__.py
from flask import Flask
from app.config import config_by_name
from app.extensions import init_extensions
from app.api import init_blueprints


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    init_extensions(app)
    init_blueprints(app)
    register_error_handlers(app)

    return app


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found", "message": str(error)}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500
```

### Entry Point

```python
# wsgi.py
import os
from app import create_app

config_name = os.environ.get("FLASK_CONFIG", "production")
app = create_app(config_name)
```

---

## 3. Configuration

### Config Classes

```python
# app/config.py
import os
from typing import Dict


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = 3600


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///dev.db"
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    JWT_ACCESS_TOKEN_EXPIRES = 60


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  # Required


config_by_name: Dict[str, type] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
```

---

## 4. Blueprints

Blueprints decouple routes into reusable, testable modules.

```python
# app/api/__init__.py
from flask import Blueprint
from .users import users_bp
from .posts import posts_bp


def init_blueprints(app) -> None:
    app.register_blueprint(users_bp, url_prefix="/api/v1/users")
    app.register_blueprint(posts_bp, url_prefix="/api/v1/posts")
```

```python
# app/api/users.py
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.schemas.user_schema import UserSchema
from app.extensions import db

users_bp = Blueprint("users", __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users_bp.route("/", methods=["GET"])
def get_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "items": users_schema.dump(users.items),
        "total": users.total,
        "pages": users.pages,
        "page": page,
    })


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    user = User.query.get_or_404(user_id)
    return user_schema.dump(user)


@users_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201


@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    errors = user_schema.validate(data, partial=True)
    if errors:
        return jsonify({"errors": errors}), 400

    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user_schema.dump(user)


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204
```

### Best Practices for Blueprints

- **One blueprint per domain entity** (`users`, `posts`, `auth`).
- **URL prefix in `init_blueprints`**, not in individual routes.
- **Schema instance at module level** for reuse.
- **Use `get_or_404`** for single-resource lookups; returns 404 automatically.

---

## 5. Extensions

Initialize extensions in a dedicated module to avoid circular imports with the factory.

```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
ma = Marshmallow()


def init_extensions(app) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    ma.init_app(app)
```

### Model Example

```python
# app/models/user.py
from app.extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"
```

### Database Commands

```bash
flask db init        # Initialize migrations (run once)
flask db migrate     # Generate migration script
flask db upgrade     # Apply migration
```

---

## 6. Request Validation & Serialization

### Marshmallow Schemas

```python
# app/schemas/user_schema.py
from app.extensions import ma
from app.models.user import User
from marshmallow import validate, ValidationError


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = ma.session

    username = ma.auto_field(validate=validate.Length(min=3, max=80))
    email = ma.auto_field(validate=validate.Email())
```

### Pydantic Alternative

```python
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
```

### Validation in Views

```python
from pydantic import ValidationError

@users_bp.route("/", methods=["POST"])
def create_user():
    try:
        user_data = UserCreate(**request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    # ... create user
```

---

## 7. Error Handling

### Standardized JSON Errors

```python
# app/utils/responses.py
from flask import jsonify
from http import HTTPStatus


def success_response(data, status=HTTPStatus.OK):
    return jsonify({"success": True, "data": data}), status


def error_response(message, status=HTTPStatus.BAD_REQUEST, errors=None):
    payload = {"success": False, "error": message}
    if errors:
        payload["details"] = errors
    return jsonify(payload), status
```

### Global Exception Handlers

```python
# app/__init__.py
from werkzeug.exceptions import HTTPException
from app.utils.responses import error_response


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return error_response(e.description, e.code)

    @app.errorhandler(404)
    def handle_not_found(e):
        return error_response("Resource not found", 404)

    @app.errorhandler(500)
    def handle_server_error(e):
        return error_response("Internal server error", 500)

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return error_response("Validation failed", 400, e.messages)
```

---

## 8. Pagination

### SQLAlchemy Pagination

```python
@users_bp.route("/", methods=["GET"])
def get_users():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    pagination = User.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "data": users_schema.dump(pagination.items),
        "meta": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        },
    })
```

### Reusable Pagination Helper

```python
# app/utils/pagination.py
from flask import request


def paginated_response(query, schema, max_per_page=100):
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), max_per_page)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        "data": schema.dump(pagination.items),
        "meta": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        },
    }
```

---

## 9. Authentication

### JWT with Flask-JWT-Extended

```python
# app/api/auth.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()

    if user and user.check_password(data.get("password")):
        token = create_access_token(identity=user.id)
        return jsonify({"access_token": token})

    return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({"user_id": current_user_id})
```

### Token Refresh Pattern

```python
from flask_jwt_extended import create_refresh_token, jwt_refresh_token_required

@auth_bp.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user_id = get_jwt_identity()
    new_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_token})
```

---

## 10. Testing

### Pytest Fixtures

```python
# app/tests/conftest.py
import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
```

### API Tests

```python
# app/tests/test_users.py
import pytest
from app.models.user import User


def test_get_users(client):
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert response.is_json


def test_create_user(client):
    data = {"username": "testuser", "email": "test@example.com"}
    response = client.post("/api/v1/users/", json=data)
    assert response.status_code == 201
    assert response.json["username"] == "testuser"


def test_create_user_invalid_email(client):
    data = {"username": "test", "email": "invalid-email"}
    response = client.post("/api/v1/users/", json=data)
    assert response.status_code == 400


def test_get_user_not_found(client):
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404
```

### Test with Authentication

```python
@pytest.fixture
def auth_headers(client):
    # Create and login a user
    client.post("/api/v1/auth/register", json={
        "username": "testadmin",
        "email": "admin@test.com",
        "password": "password123",
    })
    response = client.post("/api/v1/auth/login", json={
        "username": "testadmin",
        "password": "password123",
    })
    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_protected_endpoint(client, auth_headers):
    response = client.get("/api/v1/auth/protected", headers=auth_headers)
    assert response.status_code == 200
```

---

## 11. Docker & Deployment

### Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=wsgi.py
ENV FLASK_CONFIG=production

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
```

### docker-compose.yml

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_CONFIG=production
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Gunicorn Production Entry

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "wsgi:create_app()"
```

---

## 12. Best Practices Checklist

- [ ] Application Factory pattern used (`create_app()`)
- [ ] Configuration is environment-based (`development`, `testing`, `production`)
- [ ] Extensions initialized in `extensions.py` (no circular imports)
- [ ] Routes organized in Blueprints, one per domain
- [ ] Marshmallow or Pydantic used for validation and serialization
- [ ] Error handlers return consistent JSON structure
- [ ] Pagination enforced on all list endpoints (max 100 per page)
- [ ] Authentication uses JWT with refresh token pattern
- [ ] Tests use `app.test_client()` with `testing` config
- [ ] Database is `sqlite:///:memory:` in test config
- [ ] Migrations managed with Flask-Migrate
- [ ] `.env` stores secrets; `.flaskenv` stores Flask vars
- [ ] Dockerfile uses multi-stage build or slim base image
- [ ] Gunicorn is used in production (not Flask dev server)
- [ ] CORS configured for known origins only (not `*`) in production
- [ ] SQLAlchemy `get_or_404` used for single-resource lookups
- [ ] `check_password_hash` used for password storage (never plaintext)
- [ ] Rate limiting applied on auth and sensitive endpoints

---

## 13. Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| Circular imports | `from app import db` in models with factory | Use `extensions.py` with deferred `init_app` |
| `RuntimeError: Working outside of application context` | DB query outside `app_context()` | Use `with app.app_context()` or fixtures |
| Mutable default args in routes | Using `[]` or `{}` as default | Use `None` and initialize inside function |
| Tests writing to dev DB | Wrong config or missing `TESTING` | Set `SQLALCHEMY_DATABASE_URI` to `:memory:` |
| 500 on validation errors | No error handler for `ValidationError` | Register `@app.errorhandler(ValidationError)` |
| Exposing stack traces | `DEBUG = True` in production | Set `DEBUG = False`; use custom 500 handler |
| Missing CORS headers | Frontend can't access API | Use `flask-cors` with specific origins |
| N+1 queries | Lazy loading in loops | Use `joinedload` or `selectinload` from SQLAlchemy |
| Password in plaintext | Storing raw password string | Use `werkzeug.security.generate_password_hash` |
| No rate limiting | Brute-force on login | Add `Flask-Limiter` to sensitive endpoints |

---

## 14. References

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/)
- [Marshmallow Validation](https://marshmallow.readthedocs.io/en/stable/)
- [Pydantic](https://docs.pydantic.dev/)
- [Gunicorn](https://docs.gunicorn.org/)
- Related skills: `fastapi-templates`, `django-patterns`, `sqlalchemy-alembic-expert-best-practices-code-review`

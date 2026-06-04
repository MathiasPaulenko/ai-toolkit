---
name: Generate API Test Suite
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a complete REST API test suite from an OpenAPI spec or endpoint description. Covers CRUD, auth, validation, error codes, and contract testing.
tags: [qa, api-testing, rest, openapi, contract-testing, pytest]
role: qa-engineer
model: any
trigger: When the user asks to generate API tests, REST test suite, or endpoint tests.
---

# Generate API Test Suite

Given an OpenAPI specification, Swagger doc, or endpoint description, generate a comprehensive API test suite.

## Test Categories

### 1. HTTP Methods & Status Codes
- GET, POST, PUT, PATCH, DELETE
- 200, 201, 204, 400, 401, 403, 404, 409, 422, 500

### 2. Authentication & Authorization
- Valid/invalid tokens
- Expired tokens
- Missing/ malformed headers
- Role-based access (admin vs user)

### 3. Request Validation
- Required fields missing
- Invalid data types
- String length limits
- Numeric ranges
- Enum violations
- Date format validation

### 4. Response Contract
- Schema validation (JSON Schema)
- Required response fields
- Data type correctness
- Pagination metadata

### 5. Business Logic
- State transitions
- Concurrent updates
- Idempotency (POST with idempotency key)
- Rate limiting behavior

## Output Format (pytest)

```python
import pytest
import requests

BASE_URL = "https://api.example.com/v1"

class TestUsersEndpoint:
    def test_create_user_success(self, auth_headers):
        payload = {"email": "test@example.com", "name": "Alice"}
        resp = requests.post(f"{BASE_URL}/users", json=payload, headers=auth_headers)
        assert resp.status_code == 201
        assert resp.json()["id"] is not None
        assert resp.json()["email"] == payload["email"]

    def test_create_user_missing_email_returns_422(self, auth_headers):
        payload = {"name": "Alice"}
        resp = requests.post(f"{BASE_URL}/users", json=payload, headers=auth_headers)
        assert resp.status_code == 422
        assert "email" in resp.json()["detail"][0]["loc"]
```

## Additional Outputs

- Postman collection JSON
- cURL examples for manual testing
- Data fixtures for test setup
- Environment variables template

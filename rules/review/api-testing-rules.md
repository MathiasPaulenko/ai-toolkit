---
name: API Testing Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Rules for designing, writing, and reviewing API tests. Covers idempotency, contract validation, error handling, mocking, and test data isolation.
tags: [api-testing, rest, graphql, rules, qa]
role: api-tester
type: rules
language: en
---

# API Testing Rules

## 1. Test Isolation

### Rule 1.1: Independent Tests
- Each API test must create its own data and clean up after execution.
- Never assume data exists from a previous test.

```python
# Good
@pytest.fixture
def test_user():
    user = api.create_user({"name": "Alice", "email": "alice@test.com"})
    yield user
    api.delete_user(user["id"])

# Bad
# Uses hardcoded user ID from another test
def test_get_user():
    res = api.get("/users/1")  # May fail if test order changes
```

### Rule 1.2: Use Unique Identifiers
- Generate unique values for names, emails, and codes to avoid collisions.

```python
import uuid
email = f"test-{uuid.uuid4()}@example.com"
```

## 2. Idempotency & Statelessness

### Rule 2.1: Test Idempotent Operations
- GET, PUT, and DELETE must be safe to retry.
- Verify no side effects on repeated identical requests.

```python
def test_put_idempotent():
    payload = {"status": "active"}
    r1 = api.put("/orders/123", payload)
    r2 = api.put("/orders/123", payload)
    assert r1.status_code == r2.status_code == 200
    assert r1.json() == r2.json()
```

### Rule 2.2: No Shared State Between Tests
- Database state modified in test A must not affect test B.

## 3. Contract Validation

### Rule 3.1: Validate Response Schema
- Every API test must verify the response structure, not just status code.

```python
# Good
assert "id" in res.json()
assert isinstance(res.json()["id"], int)
assert res.json()["created_at"] is not None

# Bad
assert res.status_code == 200  # Empty body would pass
```

### Rule 3.2: Test Contract Changes
- When API contract changes, update tests before merging.
- Use schema validation libraries (jsonschema, zod, Joi).

## 4. Error Handling

### Rule 4.1: Test All Error Paths
- Every endpoint must have tests for 400, 401, 403, 404, 422, and 500.

```python
@pytest.mark.parametrize("code,payload,expected", [
    (400, None, 400),                    # Missing body
    (401, valid_payload, 401),           # No auth
    (403, valid_payload, 403),           # Wrong permissions
    (404, valid_payload, 404),           # Resource not found
    (422, {"email": "invalid"}, 422),    # Validation error
])
def test_error_cases(code, payload, expected):
    res = api.post("/users", payload, headers=auth_header if code != 401 else {})
    assert res.status_code == expected
```

### Rule 4.2: Meaningful Error Messages
- Error responses must be tested for clarity and actionable detail.

```python
assert res.json()["error"]["code"] == "INVALID_EMAIL"
assert "email" in res.json()["error"]["details"]
```

## 5. Mocking & External Dependencies

### Rule 5.1: Mock External APIs
- Tests must not depend on third-party APIs being available.
- Use WireMock, Mountebank, or framework-native mocking.

```python
# Good
responses.add(responses.GET, "https://payments.example.com/charge",
              json={"status": "approved"}, status=200)

# Bad
res = requests.post("https://api.example.com/charge")  # Real API call
```

### Rule 5.2: Verify Mock Interactions
- Ensure mocks were called with expected parameters.

```python
assert len(responses.calls) == 1
assert responses.calls[0].request.json()["amount"] == 1000
```

## 6. Performance & Concurrency

### Rule 6.1: Include Performance Assertions
- API tests should verify response times against SLAs.

```python
assert res.elapsed.total_seconds() < 0.5  # 500ms SLA
```

### Rule 6.2: Test Concurrent Access
- Race conditions must be tested where applicable.

```python
from concurrent.futures import ThreadPoolExecutor

def test_concurrent_stock_update():
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(buy_item, item_id=1) for _ in range(10)]
    results = [f.result().status_code for f in futures]
    assert results.count(200) == 1  # Only 1 succeeds
    assert results.count(409) == 9   # 9 get conflict
```

## 7. Security

### Rule 7.1: Test Authentication & Authorization
- Unauthenticated requests return 401.
- Authenticated but unauthorized requests return 403.

### Rule 7.2: Test Input Validation
- SQL injection, XSS, and path traversal payloads must be rejected.

```python
malicious = "'; DROP TABLE users; --"
res = api.post("/search", {"query": malicious})
assert res.status_code in [400, 422]
```

## Checklist

- [ ] Tests create and clean up their own data
- [ ] Response schema validated beyond status code
- [ ] Error codes 400, 401, 403, 404, 422 tested
- [ ] External APIs mocked
- [ ] Response time within SLA
- [ ] Concurrent access tested where applicable
- [ ] Security payloads rejected

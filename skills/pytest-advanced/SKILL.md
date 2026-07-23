---
name: pytest-advanced
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Advanced pytest patterns: parametrization, fixtures (session/module/function), conftest.py, plugins (cov, xdist, mock), markers, and CI integration."
tags: [pytest, python, testing, fixtures, plugins]
role: qa-engineer
model: any
trigger: When the user asks about advanced pytest, fixtures, conftest, parametrization, or Python testing patterns.
---

# Pytest Advanced

Master pytest for professional Python testing.

## 1. Project Structure

```
tests/
â”œâ”€â”€ conftest.py          # Shared fixtures, hooks, plugins
â”œâ”€â”€ unit/
â”‚   â”œâ”€â”€ test_models.py
â”‚   â””â”€â”€ test_services.py
â”œâ”€â”€ integration/
â”‚   â””â”€â”€ test_api.py
â””â”€â”€ e2e/
    â””â”€â”€ test_flows.py
pytest.ini               # Markers, testpaths, addopts
pyproject.toml           # Coverage thresholds, tool config
```

## 2. Fixtures Lifecycle

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from myapp.database import SessionLocal

@pytest.fixture(scope="session")
def db_engine():
    """Create engine once for entire test run."""
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Fresh transaction per test; rollback on exit."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="module")
def client():
    """TestClient reused for all tests in a module."""
    from fastapi.testclient import TestClient
    from myapp.main import app
    with TestClient(app) as c:
        yield c
```

## 3. Parametrization

```python
# Multiple inputs for same test logic
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("world", 5),
    ("", 0),
    ("pytest", 6),
])
def test_string_length(input, expected):
    assert len(input) == expected

# Parametrize fixtures
@pytest.fixture(params=["redis", "memcached"])
def cache_backend(request):
    if request.param == "redis":
        return RedisCache()
    return MemcachedCache()

def test_cache_set_get(cache_backend):
    cache_backend.set("key", "value")
    assert cache_backend.get("key") == "value"
```

## 4. Custom Markers & Hooks

```python
# pytest.ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    requires_db: marks tests that need a database
    smoke: marks tests as smoke tests (run first)

testpaths = tests
addopts = -v --tb=short --strict-markers
```

```python
# conftest.py â€” hook to add custom CLI option
def pytest_addoption(parser):
    parser.addoption("--run-slow", action="store_true", default=False,
                     help="run slow tests")

def pytest_collection_modifyitems(config, items):
    if not config.getoption("--run-slow"):
        skip_slow = pytest.mark.skip(reason="need --run-slow option")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
```

## 5. Monkeypatch & Mock

```python
# Built-in monkeypatch
def test_get_weather(monkeypatch):
    def mock_fetch(city):
        return {"temp": 25, "city": city}

    monkeypatch.setattr("myapp.weather.fetch_weather", mock_fetch)
    result = get_weather_summary("Madrid")
    assert result["temp"] == 25

# unittest.mock
from unittest.mock import Mock, patch, MagicMock

def test_send_notification():
    with patch("myapp.notify.smtp_client") as mock_smtp:
        mock_smtp.send_message.return_value = True
        result = send_email("user@test.com", "Hello")
        assert result is True
        mock_smtp.send_message.assert_called_once()

# MagicMock for complex objects
repo = MagicMock()
repo.find_by_email.return_value = None
repo.save.return_value = User(id=1, email="a@b.com")
```

## 6. Coverage Configuration

```toml
# pyproject.toml
[tool.coverage.run]
source = ["myapp"]
branch = true
omit = ["*/tests/*", "*/venv/*"]

[tool.coverage.report]
fail_under = 80
skip_covered = true
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
```

```bash
pytest --cov=myapp --cov-report=term-missing --cov-report=html
```

## 7. Parallel Execution (pytest-xdist)

```bash
# Run tests in parallel across CPU cores
pytest -n auto

# Run tests in parallel with 4 workers
pytest -n 4 --dist=loadfile  # group by file to avoid DB conflicts
```

```ini
# pytest.ini for CI
[pytest]
addopts = -n auto --maxfail=5
```

## 8. Async Testing (pytest-asyncio)

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch():
    result = await fetch_data("https://api.example.com")
    assert result["status"] == "ok"

# Fixture for async dependencies
@pytest.fixture
async def async_client():
    async with AsyncClient() as client:
        yield client
```

## 9. Snapshot Testing (pytest-snapshot or syrupy)

```python
# syrupy
import pytest

def test_api_response(snapshot, client):
    response = client.get("/api/users/1")
    assert response.json() == snapshot

# First run creates snapshot; subsequent runs compare
```

## 10. CI Integration

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: pytest -n auto --cov=myapp --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    files: ./coverage.xml
    fail_ci_if_error: true
```

## 11. Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Fixtures doing too much | Split into composable fixtures |
| Global state in fixtures | Use `yield` + teardown, or context managers |
| `time.sleep()` in tests | Use `freezegun` or event-based waiting |
| No markers for slow tests | Add `@pytest.mark.slow` + filter |
| Hardcoded test data | Use factories (factory_boy, faker) |
| Asserting exact dicts | Use snapshot testing or partial matchers |

## 12. Related Resources

- Skills: `behave-bdd`, `testcontainers`, `flask-api`
- Prompts: `generate-flaky-test-diagnosis`, `generate-qa-metrics-dashboard`

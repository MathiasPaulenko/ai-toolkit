---
name: Python Coding Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Coding standards and conventions for Python projects. Covers type hints, docstrings, import ordering, line length, f-strings, pathlib, and modern Python idioms.
tags: [python, coding-rules, style-guide, pep8, type-hints]
role: coding-standard
type: rules
language: en
---

# Python Coding Rules

## 1. Type Hints

- Use type hints on **all public functions** and **class attributes**.
- Use `typing` generics: `list[str]`, `dict[str, int]`, `set[str]` (Python 3.9+).
- Use `|` for unions: `str | None` instead of `Optional[str]` (Python 3.10+).
- Use `Protocol` for structural subtyping.
- Use `@dataclass` or `TypedDict` instead of raw `dict` for structured data.

```python
# Good
def create_user(name: str, email: str, age: int | None = None) -> User:
    ...

# Bad
def create_user(name, email, age=None):
    ...
```

## 2. Imports

Order: **stdlib** > **third-party** > **local**.
Separate groups with blank lines.

```python
# Good
import os
from pathlib import Path
from datetime import datetime

from flask import Flask
from sqlalchemy import Column, Integer, String

from app.models import User
from app.utils import hash_password
```

- Use **absolute imports** over relative imports.
- Import specific names, not modules: `from pathlib import Path` not `import pathlib`.
- Avoid wildcard imports (`from module import *`).

## 3. String Formatting

- Use **f-strings** for all string formatting.
- Use `pathlib.Path` for path manipulation.

```python
# Good
name = "Alice"
greeting = f"Hello, {name}!"

# Bad
greeting = "Hello, %s!" % name
greeting = "Hello, {}!".format(name)
```

## 4. Line Length and Formatting

- Maximum **88 characters** per line (Black default).
- Use **Black** for automated formatting.
- Use **isort** for import sorting.
- Use **ruff** for fast linting.

```bash
black src/ tests/
isort src/ tests/
ruff check src/ tests/
```

## 5. Docstrings

Use **Google style** docstrings with `Args`, `Returns`, `Raises`.

```python
def authenticate_user(username: str, password: str) -> User | None:
    """Authenticate a user by username and password.

    Args:
        username: The user's login name.
        password: The user's plain-text password.

    Returns:
        The authenticated User object, or None if authentication fails.

    Raises:
        DatabaseError: If the database connection is unavailable.
    """
```

## 6. Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | `snake_case` | `user_service.py` |
| Classes | `PascalCase` | `UserRepository` |
| Functions | `snake_case` | `get_user_by_id` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Private | `_leading_underscore` | `_internal_helper` |
| Variables | `snake_case` | `user_list` |

## 7. Modern Python Idioms

- Use `match`/`case` for complex branching (Python 3.10+).
- Use `:=` walrus operator for assignment expressions where it improves readability.
- Use `enumerate()` instead of manual counters.
- Use `zip()` for parallel iteration.
- Use `any()`/`all()` for boolean aggregation.
- Use `next()` with default instead of manual index access.

```python
# Good
for i, item in enumerate(items):
    ...

# Good
if any(user.is_admin for user in users):
    ...

# Good
first_active = next((u for u in users if u.is_active), None)
```

## 8. Error Handling

- Catch **specific exceptions**, never bare `except:`.
- Use `raise from` when wrapping exceptions.
- Log exceptions with context before re-raising.

```python
# Good
try:
    user = db.get_user(user_id)
except DatabaseError as e:
    logger.error("Failed to fetch user %s: %s", user_id, e)
    raise ServiceError("User lookup failed") from e

# Bad
try:
    user = db.get_user(user_id)
except:
    pass
```

## 9. File and Resource Management

- Use `with` statements for all file and resource operations.
- Use `pathlib.Path` instead of `os.path`.

```python
# Good
from pathlib import Path

config_path = Path(__file__).parent / "config.yaml"
with config_path.open("r") as f:
    data = yaml.safe_load(f)

# Bad
import os
config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(config_path, "r") as f:
    data = yaml.load(f)
```

## 10. Functions and Classes

- Functions should do **one thing**; max ~30 lines.
- Class methods should use `@staticmethod` or `@classmethod` when appropriate.
- Prefer composition over inheritance.
- Use `__slots__` for memory-efficient data classes.

## 11. Testing

- Use **pytest** for all tests.
- Name test functions descriptively: `test_user_login_with_valid_credentials`.
- Use fixtures for shared setup, not module-level state.
- Parametrize repetitive test cases.

```python
import pytest

@pytest.mark.parametrize("username,password,expected", [
    ("alice", "pass123", True),
    ("bob", "wrong", False),
    ("charlie", "", False),
])
def test_authenticate(username, password, expected):
    assert authenticate(username, password) == expected
```

## 12. Configuration and Secrets

- Use environment variables for configuration.
- Use `python-dotenv` for local development.
- Never commit secrets to version control.

```python
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]
SECRET_KEY = os.environ["SECRET_KEY"]
```

## Enforcement

```bash
# Pre-commit hook
pip install pre-commit
pre-commit install

# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.2.0
    hooks:
      - id: ruff
```

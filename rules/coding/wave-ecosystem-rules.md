---
name: Wave Ecosystem Coding Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Coding conventions for contributing to any Wave ecosystem repo. Covers Python 3.11+ standards, async-first patterns, Pydantic v2 models, testing, linting, and documentation requirements.
tags: [coding-rules, async, type-hints, pydantic]
role: coding-standard
type: rules
language: en
---

# Wave Ecosystem Coding Rules

## 1. Python Version and Type Hints

- Target **Python 3.11+** for all Wave ecosystem packages.
- Use full type hints on **all functions, methods, and class attributes**.
- Pass `mypy --strict` with zero errors.
- Use modern union syntax: `str | None` instead of `Optional[str]`.
- Use built-in generics: `list[str]`, `dict[str, int]`, `set[str]`.
- Use `TypeAlias` for complex type aliases.
- Use `Protocol` for structural subtyping when defining interfaces.

```python
# Good
async def navigate(session: CDPSession, url: str, *, timeout: int = 30000) -> None:
    ...

# Bad
async def navigate(session, url, timeout=30000):
    ...
```

## 2. Async-First

- All I/O operations must be `async`.
- Use `asyncio` as the event loop — no `threading`, no `multiprocessing` for I/O.
- No blocking calls inside async functions (`time.sleep`, `requests.get`, etc.).
- Use `asyncio.wait_for` for timeouts, not manual deadline tracking.
- Use `asyncio.CancelledError` handling for graceful shutdown.
- Use `asyncio.Queue` for producer-consumer patterns.
- Use `asyncio.Event` for signaling between coroutines.

```python
# Good
async def fetch_page(session: CDPSession, url: str) -> str:
    await session.Page.navigate(url=url)
    await session.Page.wait_for_load()
    return await session.Runtime.evaluate(expression="document.title")

# Bad
def fetch_page(session, url):
    session.Page.navigate(url=url)
    time.sleep(2)
    return session.Runtime.evaluate(expression="document.title")
```

### Blocking call exceptions

- `asyncio.run()` in `__main__` entry points is allowed.
- `asyncio.get_event_loop().run_until_complete()` in synchronous wrappers is allowed.
- File I/O in CLI tools may use `aiofiles` or `asyncio.to_thread`.

## 3. Pydantic v2 for Data Models

- Use **Pydantic v2** for all data models, configs, and API schemas.
- Use `BaseModel` with typed fields.
- Use `Field(default=..., description=...)` for field metadata.
- Use `model_config = ConfigDict(...)` for configuration.
- Use validators via `@field_validator` and `@model_validator`.
- Use `model_dump()` for serialization, not `dict()`.
- Use `model_validate()` for parsing, not `parse_obj()`.

```python
from pydantic import BaseModel, Field, ConfigDict


class InterceptConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    phases: list[str] = Field(min_length=1, description="Interception phases")
    url_patterns: list[str] = Field(min_length=1, description="Glob URL patterns")
    resource_types: list[str] | None = Field(default=None, description="Resource type filter")
```

## 4. Docstrings

- Follow **PEP 257** for all docstrings.
- Use **triple-double-quotes** for all docstrings.
- Document all public functions, classes, and modules.
- Include `Args`, `Returns`, `Raises`, and `Examples` sections.
- Use Google-style docstrings.

```python
async def set_breakpoint(
    session: CDPSession,
    *,
    url: str,
    line_number: int,
    condition: str | None = None,
) -> dict[str, str]:
    """Set a breakpoint by URL and line number.

    Args:
        session: Active CDP session.
        url: Script URL to set the breakpoint in.
        line_number: Zero-indexed line number.
        condition: Optional conditional expression.

    Returns:
        Dictionary containing the breakpoint ID.

    Raises:
        CDPError: If the breakpoint cannot be set.

    Examples:
        >>> bp = await set_breakpoint(session, url="app.js", line_number=42)
        >>> bp["breakpointId"]
        '1:0:42'
    """
    ...
```

## 5. Testing

- Maintain **90% test coverage** enforced via `pytest-cov`.
- Use `pytest` as the test framework.
- Use `pytest-asyncio` for async test support.
- Use `pytest-xdist` for parallel test execution.
- Test names: `test_<unit>_<condition>_<expected>`.
- One assertion concept per test — split complex tests.
- Use fixtures for setup and teardown.
- Use `parametrize` for data-driven tests.
- No `sleep()` in tests — use `asyncio.wait_for` with timeouts.
- Mock external dependencies with `unittest.mock.AsyncMock`.

```python
import pytest
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_navigate_returns_title_when_page_loads():
    session = AsyncMock()
    session.Runtime.evaluate.return_value = {"result": {"value": "Example"}}

    result = await fetch_page(session, "https://example.com")

    assert result == "Example"
```

## 6. Linting and Formatting

- `ruff check .` must pass with zero errors.
- `ruff format .` must pass with zero changes.
- `bandit -r src/` must pass with zero high-severity findings.
- `mypy --strict src/` must pass with zero errors.
- Line length: **100 characters**.
- Import sorting: `ruff` default (stdlib > third-party > local).

### Ruff configuration

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "SIM"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### mypy configuration

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
```

## 7. Error Handling

- No bare `except` — always catch specific exceptions.
- No `except Exception` without re-raising or logging.
- No `except: pass` — handle or propagate.
- Use custom exception classes for domain errors.
- Use `logging` for error reporting, not `print`.
- Fail fast — validate inputs at API boundaries.

```python
# Good
class CDPError(Exception):
    """Raised when a CDP command fails."""

async def execute(session: CDPSession, method: str, params: dict) -> dict:
    try:
        return await session.send(method, params)
    except ConnectionError as exc:
        raise CDPError(f"Failed to execute {method}: {exc}") from exc

# Bad
async def execute(session, method, params):
    try:
        return await session.send(method, params)
    except:
        pass
```

## 8. Imports

- No wildcard imports (`from foo import *`).
- Use absolute imports over relative imports.
- Group: stdlib > third-party > local, separated by blank lines.
- Remove unused imports (`ruff` enforces this).

```python
# Good
import asyncio
from pathlib import Path
from typing import Protocol

from pydantic import BaseModel, Field

from cdpwave import CDPSession
from cdpwave.exceptions import CDPError

# Bad
from foo import *
import os, sys, json
```

## 9. Design Principles

- Prefer **composition over inheritance**.
- Prefer **small functions** (max ~30 lines) with single responsibility.
- Prefer **early returns** over deep nesting.
- Prefer **immutable data** when appropriate (`frozen=True` dataclasses, Pydantic `frozen`).
- Prefer **explicit** over implicit.
- No mutable default arguments.
- No global mutable state.
- No magic numbers — use named constants.

```python
# Good
DEFAULT_TIMEOUT_MS: int = 30000

async def navigate(session: CDPSession, url: str, *, timeout: int = DEFAULT_TIMEOUT_MS) -> None:
    ...

# Bad
async def navigate(session, url, timeout=30000):
    ...
```

## 10. Documentation

- All public APIs must be documented in **mkdocs**.
- Use mkdocs-material theme.
- Include API reference, getting started, and examples.
- Document breaking changes in CHANGELOG.
- Use docstrings as the source of truth for API docs.

### mkdocs configuration

```yaml
site_name: Wave Ecosystem
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - search.suggest
plugins:
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: true
            show_signature_annotations: true
```

## 11. CI/CD Requirements

- All PRs must pass: `ruff check`, `ruff format --check`, `mypy --strict`, `bandit`, `pytest --cov`.
- Coverage must not drop below 90%.
- All PRs must pass on Python 3.11 and 3.12.
- Releases must be tagged with semantic versioning (`vMAJOR.MINOR.PATCH`).
- Changelog must be updated in the same PR as the code change.

### GitHub Actions CI template

```yaml
name: CI

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install ruff mypy bandit
      - run: ruff check .
      - run: ruff format --check .
      - run: mypy --strict src/
      - run: bandit -r src/

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -e ".[dev]"
      - run: pytest --cov --cov-fail-under=90
```

## 12. Package Structure

```
package-name/
  src/
    package_name/
      __init__.py
      exceptions.py
      models.py          # Pydantic models
      session.py         # Main session class
      domains/           # CDP/BiDi domain modules
        __init__.py
        network.py
        page.py
        ...
  tests/
    unit/
    integration/
    e2e/
  docs/
  pyproject.toml
  README.md
  CHANGELOG.md
```

## Checklist for Contributors

- [ ] Python 3.11+ compatible
- [ ] Full type hints (`mypy --strict` passes)
- [ ] Async-first (no blocking I/O)
- [ ] Pydantic v2 for data models
- [ ] Docstrings on all public APIs (PEP 257, Google-style)
- [ ] 90% test coverage
- [ ] `ruff check` passes
- [ ] `ruff format --check` passes
- [ ] `bandit` passes
- [ ] No bare `except`, no wildcard imports, no mutable defaults
- [ ] Composition over inheritance
- [ ] Public APIs documented in mkdocs
- [ ] CHANGELOG updated

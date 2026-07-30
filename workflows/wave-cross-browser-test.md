---
name: Cross-Browser Test Workflow
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "End-to-end workflow for writing and running cross-browser tests with bidiwave and cdpwave. Covers scenario identification, test writing, parallel execution, failure analysis, and CI/CD integration."
tags: [cross-browser, testing, bidiwave, cdpwave]
role: test-architect
---

# Cross-Browser Test Workflow

End-to-end workflow for writing and running cross-browser tests using the Wave ecosystem (bidiwave + cdpwave).

## Prerequisites

- [ ] Python 3.11+ installed
- [ ] `pip install bidiwave cdpwave wavexis pytest pytest-asyncio pytest-xdist`
- [ ] Chrome 112+ installed (for cdpwave and bidiwave)
- [ ] Firefox installed (for bidiwave cross-browser)
- [ ] Edge installed (for bidiwave cross-browser)
- [ ] Target application accessible (staging or local)

## Phase 1: Identify Test Scenarios and Target Browsers

### Step 1: Define Test Scenarios

List the critical user journeys to test:

```markdown
- [ ] Scenario 1: User login flow
- [ ] Scenario 2: Product search and filter
- [ ] Scenario 3: Shopping cart operations
- [ ] Scenario 4: Checkout and payment
- [ ] Scenario 5: User registration
```

### Step 2: Define Target Browsers

| Browser | Tool | Priority | Notes |
|---------|------|----------|-------|
| Chrome | bidiwave + cdpwave | High | Primary browser, CDP escape hatch |
| Firefox | bidiwave | High | Cross-browser compatibility |
| Edge | bidiwave | Medium | Chromium-based, BiDi supported |
| Safari | Manual / external | Low | No BiDi support, manual testing |

### Step 3: Define Compatibility Matrix

Map scenarios to browsers:

| Scenario | Chrome | Firefox | Edge |
|----------|--------|---------|------|
| Login | Yes | Yes | Yes |
| Search | Yes | Yes | Yes |
| Cart | Yes | Yes | Yes |
| Checkout | Yes | Yes | Yes |
| Registration | Yes | Yes | Yes |

## Phase 2: Write Tests with bidiwave

### Step 1: Create Test Structure

```text
tests/
  cross-browser/
    __init__.py
    conftest.py
    test_login.py
    test_search.py
    test_cart.py
    test_checkout.py
    test_registration.py
```

### Step 2: Create conftest.py with Browser Fixtures

```python
import asyncio
from typing import AsyncGenerator

import pytest
from bidiwave import BiDiSession


@pytest.fixture
async def browser(request: pytest.FixtureRequest) -> AsyncGenerator[BiDiSession, None]:
    browser_name = request.param
    session = await BiDiSession.connect(
        f"ws://localhost:9222",
        browser=browser_name,
    )
    yield session
    await session.close()


@pytest.fixture
async def chrome(browser: BiDiSession) -> AsyncGenerator[BiDiSession, None]:
    async with browser.new_context() as context:
        async with context.new_page() as page:
            yield page


browsers = ["chrome", "firefox", "edge"]
```

### Step 3: Write Cross-Browser Tests

```python
import pytest

from .conftest import browsers


@pytest.mark.parametrize("browser", browsers, indirect=True)
class TestLogin:
    @pytest.mark.asyncio
    async def test_user_can_login_with_valid_credentials(self, chrome):
        await chrome.navigate(url="https://staging.example.com/login")
        await chrome.wait_for(selector="#username")

        await chrome.input(selector="#username", text="testuser")
        await chrome.input(selector="#password", text="testpass")
        await chrome.click(selector="#submit")

        await chrome.wait_for(selector=".dashboard", timeout=10000)

        url = await chrome.get_url()
        assert "/dashboard" in url

    @pytest.mark.asyncio
    async def test_user_sees_error_with_invalid_credentials(self, chrome):
        await chrome.navigate(url="https://staging.example.com/login")
        await chrome.wait_for(selector="#username")

        await chrome.input(selector="#username", text="wronguser")
        await chrome.input(selector="#password", text="wrongpass")
        await chrome.click(selector="#submit")

        await chrome.wait_for(selector=".error-message", timeout=10000)

        text = await chrome.get_text(selector=".error-message")
        assert "invalid" in text.lower()
```

### Step 4: Add Chrome-Specific Assertions with cdpwave

For Chrome-only features (CPU profiling, heap snapshots, code coverage), use cdpwave as an escape hatch:

```python
import pytest
from cdpwave import CDPSession


@pytest.mark.asyncio
@pytest.mark.only_browser("chrome")
async def test_no_memory_leak_after_login():
    """Chrome-specific: verify no memory leak using cdpwave HeapProfiler."""
    session = await CDPSession.connect("ws://localhost:9222")
    await session.HeapProfiler.enable()
    await session.Page.enable()

    await session.Page.navigate(url="https://staging.example.com/login")
    await session.Page.wait_for_load()

    # Take before snapshot
    before = await session.HeapProfiler.take_heap_snapshot()

    # Perform login
    await session.Runtime.evaluate(expression="""
        document.querySelector('#username').value = 'testuser';
        document.querySelector('#password').value = 'testpass';
        document.querySelector('#submit').click();
    """)

    await asyncio.sleep(3)

    # Take after snapshot
    after = await session.HeapProfiler.take_heap_snapshot()

    # Compare (simplified — use heap-analysis.py pattern for full comparison)
    assert len(after["nodes"]) <= len(before["nodes"]) * 1.1  # 10% tolerance

    await session.HeapProfiler.disable()
    await session.close()
```

## Phase 3: Set Up Browser Endpoints

### Step 1: Start Chrome with Remote Debugging

```bash
google-chrome --remote-debugging-port=9222 --headless --no-sandbox
```

### Step 2: Start Firefox with BiDi

```bash
firefox --remote-debugging-port=9224 --headless
```

### Step 3: Start Edge with Remote Debugging

```bash
msedge --remote-debugging-port=9226 --headless --no-sandbox
```

### Step 4: Configure Endpoints in conftest.py

```python
BROWSER_ENDPOINTS = {
    "chrome": "ws://localhost:9222",
    "firefox": "ws://localhost:9224",
    "edge": "ws://localhost:9226",
}


@pytest.fixture
async def browser(request: pytest.FixtureRequest) -> AsyncGenerator[BiDiSession, None]:
    browser_name = request.param
    endpoint = BROWSER_ENDPOINTS[browser_name]
    session = await BiDiSession.connect(endpoint, browser=browser_name)
    yield session
    await session.close()
```

## Phase 4: Run Tests in Parallel

### Step 1: Run Across Browsers in Parallel

```bash
pytest tests/cross-browser/ -n auto --dist loadscope
```

### Step 2: Run Specific Browser

```bash
pytest tests/cross-browser/ -k "chrome" --asyncio-mode=auto
```

### Step 3: Run with Coverage

```bash
pytest tests/cross-browser/ --cov=src --cov-report=html --cov-fail-under=90
```

### Step 4: Run with Verbose Output

```bash
pytest tests/cross-browser/ -v --tb=short --asyncio-mode=auto
```

## Phase 5: Analyze Failures and Generate Reports

### Step 1: Capture Screenshots on Failure

```python
@pytest.fixture
async def page(browser):
    async with browser.new_context() as context:
        async with context.new_page() as page:
            yield page
        # Screenshot on failure
        if hasattr(page, "_failed"):
            await page.screenshot(path=f"artifacts/failure-{browser.name}.png")
```

### Step 2: Generate HTML Report

```bash
pytest tests/cross-browser/ --html=reports/cross-browser-report.html --self-contained-html
```

### Step 3: Generate JUnit XML for CI

```bash
pytest tests/cross-browser/ --junitxml=reports/junit.xml
```

### Step 4: Upload Artifacts

```bash
# Zip all artifacts
tar -czf artifacts.tar.gz artifacts/ reports/
```

## Phase 6: Integrate into CI/CD Pipeline

### GitHub Actions Workflow

```yaml
name: Cross-Browser Tests

on: [pull_request]

jobs:
  cross-browser-test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        browser: [chrome, firefox, edge]
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install browsers
        run: |
          if [ "${{ matrix.browser }}" = "chrome" ]; then
            wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
            sudo dpkg -i google-chrome-stable_current_amd64.deb
          elif [ "${{ matrix.browser }}" = "firefox" ]; then
            sudo apt-get install -y firefox
          elif [ "${{ matrix.browser }}" = "edge" ]; then
            curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
            sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
            sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list'
            sudo apt-get update
            sudo apt-get install microsoft-edge-stable
          fi

      - name: Install dependencies
        run: |
          pip install bidiwave cdpwave wavexis pytest pytest-asyncio pytest-xdist pytest-html

      - name: Start browser
        run: |
          if [ "${{ matrix.browser }}" = "chrome" ]; then
            google-chrome --remote-debugging-port=9222 --headless --no-sandbox &
          elif [ "${{ matrix.browser }}" = "firefox" ]; then
            firefox --remote-debugging-port=9224 --headless &
          elif [ "${{ matrix.browser }}" = "edge" ]; then
            msedge --remote-debugging-port=9226 --headless --no-sandbox &
          fi
          sleep 3

      - name: Run tests
        run: |
          pytest tests/cross-browser/ -k "${{ matrix.browser }}" \
            --html=reports/report-${{ matrix.browser }}.html \
            --junitxml=reports/junit-${{ matrix.browser }}.xml \
            --asyncio-mode=auto

      - name: Upload artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ matrix.browser }}
          path: |
            reports/
            artifacts/
```

## Checklist

- [ ] Test scenarios identified and documented
- [ ] Target browsers defined (Chrome, Firefox, Edge)
- [ ] Compatibility matrix created
- [ ] Test structure created (`tests/cross-browser/`)
- [ ] `conftest.py` with browser fixtures
- [ ] Cross-browser tests written with bidiwave
- [ ] Chrome-specific tests added with cdpwave (if needed)
- [ ] Browser endpoints configured
- [ ] Tests run in parallel (`pytest -n auto`)
- [ ] Screenshots captured on failure
- [ ] HTML and JUnit reports generated
- [ ] CI/CD pipeline configured (GitHub Actions)
- [ ] Artifacts uploaded on failure

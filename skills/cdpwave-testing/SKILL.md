---
name: CDPWave Testing
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Write browser automation tests with cdpwave at the CDP level. Async test patterns, multi-tab sessions, event handling, screenshots in CI, escape hatch for uncovered CDP methods."
tags: [cdp, browser-testing, python-async, chrome-devtools]
trigger: When the user asks about testing with cdpwave, needs to write CDP-level browser tests, wants async patterns for Chrome DevTools Protocol in Python, or needs to migrate from pyppeteer/pychrome to cdpwave.
---

# CDPWave Testing

## Description

cdpwave is a low-level Chrome DevTools Protocol (CDP) client for Python. It talks directly to Chrome's WebSocket endpoint — no Node.js, no ChromeDriver, no Selenium, no Playwright. Just pure async Python with full type hints. It is the CDP backend that powers wavexis and wavexis-mcp.

This skill covers writing browser automation tests with cdpwave at the CDP level, including async test patterns, multi-tab sessions, event handling, screenshots in CI, and the escape hatch for uncovered CDP methods.

## When to Invoke

- Writing CDP-level browser tests in Python
- Needing direct Chrome DevTools Protocol access without abstractions
- Migrating from pyppeteer or pychrome to cdpwave
- Setting up pytest-asyncio fixtures for CDP testing
- Needing multi-tab session management in tests
- Handling CDP events in async test flows
- Using the escape hatch for CDP methods without typed wrappers

## Prerequisites

- Python 3.11+
- A Chromium-based browser (Chrome, Edge, Brave, or Chromium) installed
- `pip install cdpwave`
- `pip install pytest pytest-asyncio` (for testing)

## CDPClient Setup

### Launch a new browser

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        result = await session.runtime.evaluate("document.title", return_by_value=True)
        print(result["result"]["value"])
        await session.close()

asyncio.run(main())
```

### Connect to an existing browser

```python
from cdpwave import CDPClient

async with await CDPClient.connect(host="localhost", port=9222) as client:
    session = await client.new_page("https://example.com")
```

### Connect via direct WebSocket URL

```python
from cdpwave import CDPClient

async with await CDPClient.connect(ws_url="ws://localhost:9222/devtools/page/123") as client:
    session = await client.new_page("https://example.com")
```

### Launch options

```python
client = await CDPClient.launch(
    headless=False,
    browser_path="/usr/bin/google-chrome",
    extra_args=["--disable-gpu", "--no-sandbox"],
    keepalive_interval=30,
    keepalive_timeout=10,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `headless` | `bool` | `True` | Run browser without UI |
| `browser_path` | `str \| None` | Auto-detect | Path to browser executable |
| `extra_args` | `list[str]` | `[]` | Extra Chrome flags |
| `keepalive_interval` | `int` | `30` | WebSocket ping interval (seconds) |
| `keepalive_timeout` | `int` | `10` | WebSocket pong timeout (seconds) |

## Session Management

### Create and close sessions

```python
async with await CDPClient.launch() as client:
    session = await client.new_page("https://example.com")
    # Work with session...
    await session.close()
```

### Multi-tab sessions

```python
async with await CDPClient.launch() as client:
    tab1 = await client.new_page("https://example.com")
    tab2 = await client.new_page("https://example.org")

    title1 = await tab1.runtime.evaluate("document.title", return_by_value=True)
    title2 = await tab2.runtime.evaluate("document.title", return_by_value=True)

    print(title1["result"]["value"])  # "Example Domain"
    print(title2["result"]["value"])  # "IANA-managed domains"

    # Track all active sessions
    for sid, session in client.sessions.items():
        print(f"Session {sid}: {await session.runtime.evaluate('location.href', return_by_value=True)}")
```

### Session lifecycle

```python
session = await client.new_page("https://example.com")

# Navigate
await session.page.navigate("https://example.org")

# Reload
await session.page.reload()

# Go back / forward
await session.page.navigate("https://example.com")
await session.page.go_back()
await session.page.go_forward()

# Close
await session.close()
```

## Domain Methods

cdpwave implements all 60 CDP domains with 689 typed methods. Each session exposes domains as properties:

```python
session.runtime   # Runtime domain — evaluate, callFunction, etc.
session.page      # Page domain — navigate, screenshot, PDF, etc.
session.network   # Network domain — intercept, throttle, headers, etc.
session.dom       # DOM domain — query, attributes, etc.
session.emulation # Emulation domain — device, viewport, etc.
session.target    # Target domain — tabs, workers, etc.
```

### Runtime domain

```python
# Evaluate JavaScript
result = await session.runtime.evaluate(
    "document.title",
    return_by_value=True,
)
print(result["result"]["value"])

# Call a function
result = await session.runtime.call_function(
    "function() { return document.querySelectorAll('a').length; }",
    return_by_value=True,
)
print(result["result"]["value"])

# Evaluate with await
result = await session.runtime.evaluate(
    "await fetch('/api/data').then(r => r.json())",
    await_promise=True,
    return_by_value=True,
)
```

### Page domain

```python
# Navigate
await session.page.navigate("https://example.com")

# Screenshot
screenshot = await session.page.capture_screenshot()
with open("screenshot.png", "wb") as f:
    f.write(bytes.fromhex(screenshot["data"]))

# Full-page screenshot
screenshot = await session.page.capture_screenshot(capture_beyond_viewport=True)

# PDF
pdf = await session.page.print_to_pdf()
with open("page.pdf", "wb") as f:
    f.write(bytes.fromhex(pdf["data"]))

# Get navigation history
history = await session.page.get_navigation_history()
```

### Network domain

```python
# Enable network tracking
await session.network.enable()

# Set extra headers
await session.network.set_extra_http_headers({
    "Authorization": "Bearer token123",
})

# Block requests
await session.network.set_blocked_urls(["*.ads.example.com/*"])

# Throttle
await session.network.emulate_network_conditions(
    offline=False,
    download_throughput=1_000_000,
    upload_throughput=500_000,
    latency=100,
)
```

### DOM domain

```python
# Get document
doc = await session.dom.get_document()

# Query selector
node = await session.dom.query_selector(
    node_id=doc["root"]["nodeId"],
    selector="#my-element",
)

# Get attributes
attrs = await session.dom.get_attributes(node_id=node["nodeId"])

# Get outer HTML
html = await session.dom.get_outer_html(node_id=node["nodeId"])
```

### Emulation domain

```python
# Set viewport
await session.emulation.set_device_metrics_override(
    width=375,
    height=667,
    device_scale_factor=2,
    mobile=True,
)

# Set geolocation
await session.emulation.set_geolocation_override(
    latitude=37.7749,
    longitude=-122.4194,
    accuracy=100,
)

# Set timezone
await session.emulation.set_timezone_override("America/Los_Angeles")
```

## Event Handling

### Listen for events

```python
async with await CDPClient.launch() as client:
    session = await client.new_page("https://example.com")

    def on_console(msg):
        print(f"[console] {msg['args']}")

    session.on("Runtime.consoleAPICalled", on_console)

    # Wait for a specific event
    await session.wait_for_event("Page.loadEventFired")
```

### Common events

| Event | Domain | Description |
|-------|--------|-------------|
| `Page.loadEventFired` | Page | Page load completed |
| `Page.frameNavigated` | Page | Frame navigation |
| `Runtime.consoleAPICalled` | Runtime | Console log |
| `Runtime.exceptionThrown` | Runtime | JS exception |
| `Network.requestWillBeSent` | Network | Request started |
| `Network.responseReceived` | Network | Response received |
| `Network.loadingFinished` | Network | Loading completed |
| `Target.targetCreated` | Target | New target (tab, worker) |
| `Target.targetDestroyed` | Target | Target closed |

### Event-driven test pattern

```python
async def test_page_load_emits_events(session):
    events = []

    session.on("Page.frameNavigated", lambda e: events.append("navigated"))
    session.on("Page.loadEventFired", lambda e: events.append("loaded"))

    await session.page.navigate("https://example.com")
    await session.wait_for_event("Page.loadEventFired")

    assert "navigated" in events
    assert "loaded" in events
```

## Escape Hatch

Call any CDP method, even if cdpwave doesn't have a typed wrapper:

```python
# Performance metrics
result = await session.send("Performance.getMetrics", {})
print(result["metrics"])

# Heap snapshot
result = await session.send("HeapProfiler.takeHeapSnapshot", {})

# Any CDP method
result = await session.send("Any.CDPMethod", {"param": "value"})
```

### When to use the escape hatch

- CDP method not yet wrapped in cdpwave
- Need access to experimental CDP features
- Testing new CDP domains before typed support
- Quick prototyping before committing to a typed wrapper

## Browser Detection

cdpwave automatically detects installed Chromium-based browsers:

```python
from cdpwave import CDPClient

# Auto-detect: finds Chrome, Edge, Brave, or Chromium
client = await CDPClient.launch()

# Explicit browser path
client = await CDPClient.launch(browser_path="/usr/bin/brave-browser")

# Check what was detected
print(client.browser_info)
```

### Detection order

1. Google Chrome
2. Microsoft Edge
3. Brave
4. Chromium

### HTTP discovery

```python
from cdpwave import CDPClient

# Access /json/version and /json/list endpoints
info = await CDPClient.discover(host="localhost", port=9222)
print(info.version)
print(info.targets)
```

## WebSocket Keepalive

cdpwave maintains the WebSocket connection with automatic ping/pong:

```python
client = await CDPClient.launch(
    keepalive_interval=30,  # Send ping every 30s
    keepalive_timeout=10,   # Wait 10s for pong before reconnecting
)
```

### Connection management

```python
# The context manager handles cleanup automatically
async with await CDPClient.launch() as client:
    session = await client.new_page("https://example.com")
    # Connection is maintained throughout
    # Cleanup happens on context exit

# Manual management (advanced)
client = await CDPClient.launch()
try:
    session = await client.new_page("https://example.com")
    # ...
finally:
    await client.close()
```

## Integration with pytest-asyncio

### Basic test

```python
import pytest
from cdpwave import CDPClient

@pytest.mark.asyncio
async def test_page_title():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        result = await session.runtime.evaluate("document.title", return_by_value=True)
        assert result["result"]["value"] == "Example Domain"
        await session.close()
```

### With fixtures

```python
# conftest.py
import pytest
from cdpwave import CDPClient

@pytest.fixture
async def client():
    async with await CDPClient.launch(headless=True) as client:
        yield client

@pytest.fixture
async def session(client):
    session = await client.new_page("https://example.com")
    yield session
    await session.close()

# test_example.py
@pytest.mark.asyncio
async def test_title(session):
    result = await session.runtime.evaluate("document.title", return_by_value=True)
    assert result["result"]["value"] == "Example Domain"

@pytest.mark.asyncio
async def test_screenshot(session):
    screenshot = await session.page.capture_screenshot()
    assert screenshot["data"]  # base64-encoded PNG data
```

### pytest.ini configuration

```ini
[pytest]
asyncio_mode = auto
```

### Running tests

```bash
pytest tests/ -v
pytest tests/ -k "test_page" -v
pytest tests/ --tb=short
```

## CI/CD Patterns

### Screenshot in CI

```python
import pytest
from cdpwave import CDPClient
import base64

@pytest.mark.asyncio
async def test_visual_regression():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        screenshot = await session.page.capture_screenshot(capture_beyond_viewport=True)

        with open("current.png", "wb") as f:
            f.write(bytes.fromhex(screenshot["data"]))

        # Compare with baseline
        # (use Pillow, pixelmatch, or your preferred tool)
```

### Headless-only CI

```python
@pytest.fixture
async def client():
    async with await CDPClient.launch(
        headless=True,
        extra_args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
    ) as client:
        yield client
```

### Parallel test isolation

```python
@pytest.fixture
async def session(client):
    """Each test gets its own tab for isolation."""
    session = await client.new_page("about:blank")
    yield session
    await session.close()
```

## Best Practices

- **Use context managers** — `async with` ensures cleanup even on exceptions.
- **Close sessions explicitly** — `await session.close()` frees resources promptly.
- **Use `return_by_value=True`** — serializes JS results to Python values.
- **Use `await_promise=True`** — for async JS expressions that return Promises.
- **Enable only needed domains** — `await session.network.enable()` before network events.
- **Use the escape hatch sparingly** — prefer typed methods when available.
- **Set keepalive for long sessions** — prevents WebSocket timeouts in CI.
- **Use `--no-sandbox` in Docker** — required for Chrome in containers.
- **Capture full-page screenshots** — `capture_beyond_viewport=True` for complete page.
- **Isolate tests with separate tabs** — each test gets its own session.

## Common Pitfalls

- **Forgetting `await`** — all CDP calls are async; missing `await` silently does nothing.
- **Not enabling domains** — events won't fire without `enable()` calls (e.g., `network.enable()`).
- **Headless detection differences** — some sites behave differently in headless mode; use `--stealth` args.
- **WebSocket timeout in CI** — increase `keepalive_interval` for slow CI runners.
- **Resource leaks** — always use `async with` or explicit `close()` in `finally`.
- **Session vs client confusion** — `client` manages the browser; `session` is a single tab/page.
- **Return format** — `evaluate` returns `{"result": {"value": ...}}`, not the value directly.
- **Docker without `--no-sandbox`** — Chrome requires `--no-sandbox` in containers.

## References

- `references/cdp-domains.md` — All 60 CDP domains reference
- `references/async-patterns.md` — asyncio patterns for CDP testing
- `references/migration-pyppeteer.md` — Migration from pyppeteer/pychrome
- `assets/templates/test_screenshot.py` — Screenshot test template
- `assets/templates/test_multi_tab.py` — Multi-tab test template
- `assets/templates/test_events.py` — Event handling test template
- `assets/templates/conftest.py` — pytest-asyncio fixtures for cdpwave
- [cdpwave on GitHub](https://github.com/MathiasPaulenko/cdpwave)
- [cdpwave documentation](https://mathiaspaulenko.github.io/cdpwave/)
- [CDP protocol spec](https://chromedevtools.github.io/devtools-protocol/)

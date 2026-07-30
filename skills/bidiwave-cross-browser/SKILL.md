---
name: BiDiWave Cross-Browser
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Cross-browser testing with bidiwave using the W3C WebDriver BiDi protocol. Works with Chrome, Firefox, and Edge. RemoteValue pattern matching, preload scripts, web extensions, CDP bridge."
tags: [webdriver-bidi, cross-browser, w3c, firefox-chrome]
trigger: When the user asks about cross-browser testing with bidiwave, needs W3C WebDriver BiDi protocol access in Python, wants to run tests across Chrome/Firefox/Edge, or needs RemoteValue pattern matching.
---

# BiDiWave Cross-Browser

## Description

bidiwave is a low-level WebDriver BiDi client for Python. It speaks the W3C WebDriver BiDi protocol directly — no Selenium, no Playwright, no Node.js. Unlike CDP (which is Chromium-specific), BiDi is a W3C standard that works across Chrome, Firefox, and Edge. It is the BiDi backend that powers wavexis and wavexis-mcp.

This skill covers cross-browser testing with bidiwave, including browsing contexts, script evaluation with RemoteValue pattern matching, input simulation, network interception, storage, emulation, permissions, preload scripts, web extensions, CDP bridge, event streaming, and reconnection.

## When to Invoke

- Writing cross-browser tests that must work on Chrome, Firefox, and Edge
- Needing W3C WebDriver BiDi protocol access in Python
- Using RemoteValue `match` pattern narrowing for typed JS results
- Setting up preload scripts that run before page load
- Installing web extensions during tests
- Using CDP bridge for Chrome-specific features within BiDi workflows
- Migrating from Selenium/Playwright to a standard protocol
- Needing network interception, emulation, or permissions in cross-browser tests

## Prerequisites

- Python 3.11+
- A BiDi-capable browser endpoint:
  - Chrome/Edge: ChromeDriver or EdgeDriver running with BiDi support
  - Firefox: Firefox with `--remote-debugging-port` (BiDi is native, no driver needed)
- `pip install bidiwave`
- `pip install pytest pytest-asyncio` (for testing)

## BiDiClient Setup

### Connect to a BiDi endpoint

```python
import asyncio
from bidiwave import BiDiClient, StringValue

async def main():
    async with await BiDiClient.connect("ws://localhost:9515/session") as client:
        async with await client.browsing.open("https://example.com") as page:
            result = await page.evaluate("document.title")
            match result:
                case StringValue(value=title):
                    print(f"Title: {title}")
```

### Connect to Chrome/Edge via ChromeDriver

```bash
# Start ChromeDriver
chromedriver --port=9515
```

```python
async with await BiDiClient.connect("ws://localhost:9515/session") as client:
    # ...
```

### Connect to Firefox (native BiDi)

```bash
# Start Firefox with remote debugging
firefox --headless --remote-debugging-port=9223 --no-remote
```

```python
async with await BiDiClient.connect("ws://localhost:9223/session") as client:
    # ...
```

### Connect to Edge via EdgeDriver

```bash
# Start EdgeDriver
msedgedriver --port=9516
```

```python
async with await BiDiClient.connect("ws://localhost:9516/session") as client:
    # ...
```

### Connection options

```python
client = await BiDiClient.connect(
    "ws://localhost:9515/session",
    reconnect=True,
    max_retries=5,
    backoff_base=0.5,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | `str` | Required | WebSocket URL of BiDi endpoint |
| `reconnect` | `bool` | `True` | Auto-reconnect on disconnect |
| `max_retries` | `int` | `5` | Max reconnection attempts |
| `backoff_base` | `float` | `0.5` | Base delay for exponential backoff |

## Browsing Contexts

### Open and close contexts

```python
async with await client.browsing.open("https://example.com") as page:
    result = await page.evaluate("document.title")
    # Page auto-closes on context exit
```

### Navigation

```python
async with await client.browsing.open("https://example.com") as page:
    # Navigate
    await page.navigate("https://example.org")

    # Reload
    await page.reload()

    # Go back / forward
    await page.traverse_history("back")
    await page.traverse_history("forward")
```

### Screenshots

```python
async with await client.browsing.open("https://example.com") as page:
    screenshot = await page.screenshot()
    with open("screenshot.png", "wb") as f:
        f.write(screenshot)
```

### Viewport control

```python
from bidiwave import ViewportSize

await client.browsing.set_viewport(
    page.id,
    viewport=ViewportSize(width=375, height=812),
    device_pixel_ratio=3.0,
)
```

### Element waiting

```python
# Wait for an element via CSS selector
await page.wait_for_element("#my-element", timeout=10)

# Wait via XPath
await page.wait_for_element("//div[@id='content']", locator="xpath", timeout=10)
```

### PDF printing

```python
pdf = await page.print_to_pdf()
with open("page.pdf", "wb") as f:
    f.write(pdf)
```

### Dialog handling

```python
async with await client.browsing.open("https://example.com") as page:
    # Handle alert dialogs
    await page.handle_user_prompt(accept=True, user_text=None)
```

## Script Evaluation

### Basic evaluation

```python
result = await page.evaluate("document.title")
match result:
    case StringValue(value=title):
        print(f"Title: {title}")
```

### RemoteValue pattern matching

```python
from bidiwave import (
    StringValue, NumberValue, BooleanValue,
    NullValue, UndefinedValue, ArrayValue, ObjectValue,
)

result = await page.evaluate("JSON.stringify({name: 'test', count: 42})")
match result:
    case StringValue(value=json_str):
        data = json.loads(json_str)
        print(data["name"], data["count"])
```

### Evaluate and call functions

```python
# Call a function with arguments
result = await page.evaluate(
    "(a, b) => a + b",
    args=[1, 2],
)
match result:
    case NumberValue(value=sum_val):
        assert sum_val == 3
```

### Realm inspection

```python
# Get all realms (execution contexts)
realms = await client.script.get_realms()
for realm in realms:
    print(f"Realm: {realm.realm_id}, origin: {realm.origin}")
```

### User activation

```python
# Simulate user activation (trusted click)
await page.evaluate("navigator.userActivation.isActive", user_activation=True)
```

## Input Simulation

### Click

```python
await client.input.click(page.id, x=100, y=200)
```

### Type text

```python
await client.input.type_text(page.id, "Hello, world!")
```

### Press keys

```python
await client.input.press_key(page.id, "Enter")
await client.input.press_key(page.id, "Control+a")
```

### Scroll

```python
await client.input.scroll(page.id, delta_y=500)
await client.input.scroll(page.id, delta_x=300)
```

### Drag and drop

```python
await client.input.drag_and_drop(page.id, 100, 100, 300, 300)
```

### File upload

```python
await client.input.set_files(page.id, "/path/to/file.txt")
```

## Network Interception

### Block requests

```python
intercept = await client.network.add_intercept(
    phases=["beforeRequestSent"],
    url_patterns=["*ads.example.com*"],
)

# ... browse ...

await client.network.remove_intercept(intercept.intercept_id)
```

### Modify requests

```python
intercept = await client.network.add_intercept(
    phases=["beforeRequestSent"],
    url_patterns=["*api.example.com*"],
)

# Modify request headers
await client.network.add_headers({
    "Authorization": "Bearer token123",
})
```

### Mock responses

```python
intercept = await client.network.add_intercept(
    phases=["responseStarted"],
    url_patterns=["*api.example.com/data*"],
)

# Provide a mock response
await client.network.provide_response(
    intercept_id=intercept.intercept_id,
    status_code=200,
    headers={"Content-Type": "application/json"},
    body='{"mocked": true}',
)
```

### Extra headers

```python
await client.network.set_extra_headers(
    headers={"X-Custom-Header": "value"},
    contexts=[page.id],
)
```

### Authentication

```python
await client.network.continue_with_auth(
    request_id=req_id,
    credentials={"username": "admin", "password": "pass"},
)
```

## Storage

### Cookies

```python
from bidiwave import Cookie

# Set a cookie
await client.storage.set_cookie(
    page.id,
    cookie=Cookie(
        name="session",
        value="abc123",
        domain="example.com",
        http_only=True,
        secure=True,
        same_site="strict",
    ),
)

# Get all cookies
cookies = await client.storage.get_cookies(page.id)
for c in cookies:
    print(f"{c.name}={c.value}")

# Delete a cookie
await client.storage.delete_cookie(page.id, "session")
```

### Partition keys

```python
# Cookies with partition key (CHIPS)
await client.storage.set_cookie(
    page.id,
    cookie=Cookie(
        name="partitioned",
        value="data",
        domain="example.com",
        partition_key={"top_level_site": "https://example.com"},
    ),
)
```

### Cookie change monitoring

```python
async def on_cookie_change(event):
    print(f"Cookie changed: {event}")

client.on("storage.cookieChanged", on_cookie_change)
await client.session.subscribe(["storage.cookieChanged"])
```

## Emulation

### Geolocation

```python
await client.emulation.set_geolocation_override(
    coordinates={"latitude": 35.6762, "longitude": 139.6503, "accuracy": 1.0},
    contexts=[page.id],
)
```

### Locale

```python
await client.emulation.set_locale_override(
    locale="ja-JP",
    contexts=[page.id],
)
```

### Timezone

```python
await client.emulation.set_timezone_override(
    timezone="Asia/Tokyo",
    contexts=[page.id],
)
```

### User agent

```python
await client.emulation.set_user_agent_override(
    user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
    contexts=[page.id],
)
```

### Network conditions

```python
await client.emulation.set_network_conditions(
    network_conditions={
        "offline": False,
        "download_throughput": 50000,
        "upload_throughput": 25000,
        "latency": 400,
    },
    contexts=[page.id],
)
```

### Screen orientation

```python
await client.emulation.set_screen_orientation_override(
    orientation={"type": "portraitPrimary", "angle": 0},
    contexts=[page.id],
)
```

## Permissions

### Grant permissions

```python
await client.permissions.set_permission(
    descriptor={"name": "geolocation"},
    state="granted",
    contexts=[page.id],
)
```

### Deny permissions

```python
await client.permissions.set_permission(
    descriptor={"name": "notifications"},
    state="denied",
    contexts=[page.id],
)
```

### Common permissions

| Permission | Descriptor | States |
|------------|------------|--------|
| Geolocation | `{"name": "geolocation"}` | `granted`, `denied`, `prompt` |
| Notifications | `{"name": "notifications"}` | `granted`, `denied`, `prompt` |
| Camera | `{"name": "camera"}` | `granted`, `denied`, `prompt` |
| Microphone | `{"name": "microphone"}` | `granted`, `denied`, `prompt` |
| Clipboard | `{"name": "clipboard-read"}` | `granted`, `denied`, `prompt` |

## Preload Scripts

### Add a preload script

```python
result = await client.preload.add_preload_script(
    function_declaration="() => { window.__testMode = true; }",
)

async with await client.browsing.open("https://example.com") as page:
    value = await page.evaluate("window.__testMode")
    print(f"Test mode: {value}")

await client.preload.remove_preload_script(result.script)
```

### Preload with channel communication

```python
result = await client.preload.add_preload_script(
    function_declaration="""
    (channel) => {
        channel.postMessage('page loaded');
        window.__channel = channel;
    }
    """,
    arguments=[{"type": "channel", "value": {"channel": "test-channel"}}],
)

# Listen for channel messages
async def on_channel(event):
    print(f"Channel message: {event}")

client.on("script.message", on_channel)
await client.session.subscribe(["script.message"])
```

### User context support

```python
result = await client.preload.add_preload_script(
    function_declaration="() => { window.__loaded = true; }",
    user_contexts=["default"],
)
```

## Web Extensions

### Install

```python
result = await client.web_extension.install("/path/to/extension.crx")
print(f"Installed: {result}")
```

### Uninstall

```python
await client.web_extension.uninstall(result.extension)
```

## CDP Bridge

Access Chrome DevTools Protocol for Chrome-specific features:

```python
# Use CDP bridge for Chrome-specific features
cdp_result = await client.cdp.send_command(
    method="Page.captureScreenshot",
    params={"format": "png"},
)
```

### When to use CDP bridge

- Chrome-specific CDP methods not in BiDi spec
- Features only available in Chromium (e.g., `Page.printToPDF` options)
- Debugging Chrome-specific behavior
- Accessing CDP-only domains (e.g., `HeapProfiler`, `Performance`)

## Event Streaming

### Subscribe to events

```python
async with await BiDiClient.connect(url) as client:
    async def on_log(entry):
        print(f"[{entry.level}] {entry.text}")

    client.on("log.entryAdded", on_log)
    await client.session.subscribe(["log.entryAdded"])

    async with await client.browsing.open("https://example.com") as page:
        await page.evaluate("console.log('hello!')")
        await asyncio.sleep(2)
```

### Common event types

| Event | Module | Description |
|-------|--------|-------------|
| `log.entryAdded` | Log | Console log entry |
| `browsingContext.navigationStarted` | Browsing | Navigation started |
| `browsingContext.fragmentNavigated` | Browsing | Fragment navigation |
| `browsingContext.domContentLoaded` | Browsing | DOM content loaded |
| `browsingContext.load` | Browsing | Page fully loaded |
| `browsingContext.closed` | Browsing | Context closed |
| `network.beforeRequestSent` | Network | Request about to be sent |
| `network.responseStarted` | Network | Response started |
| `network.responseCompleted` | Network | Response completed |
| `network.fetchError` | Network | Fetch error |
| `network.authRequired` | Network | Authentication required |
| `script.realmCreated` | Script | New realm created |
| `script.realmDestroyed` | Script | Realm destroyed |
| `script.message` | Script | Channel message |
| `storage.cookieChanged` | Storage | Cookie changed |
| `input.fileDialogOpened` | Input | File dialog opened |
| `browsingContext.userPromptOpened` | Browsing | Dialog/alert opened |
| `browsingContext.downloadWillBegin` | Browsing | Download starting |
| `network.dataReceived` | Network | Data received |
| `network.requestSent` | Network | Request sent |
| `script.callFunction` | Script | Function called |
| `browsingContext.navigationAborted` | Browsing | Navigation aborted |
| `browsingContext.navigationFailed` | Browsing | Navigation failed |
| `browsingContext.screenshot` | Browsing | Screenshot taken |
| `preload.scriptAdded` | Preload | Preload script added |
| `preload.scriptRemoved` | Preload | Preload script removed |
| `web_extension.installed` | WebExtension | Extension installed |

### Error isolation

Event handlers are isolated — an exception in one handler does not affect others:

```python
async def handler_a(event):
    raise ValueError("oops")

async def handler_b(event):
    print("Still works!")

client.on("log.entryAdded", handler_a)
client.on("log.entryAdded", handler_b)
# handler_b still runs even if handler_a raises
```

## Reconnection

bidiwave automatically reconnects with exponential backoff:

```python
client = await BiDiClient.connect(
    url,
    reconnect=True,
    max_retries=5,
    backoff_base=0.5,  # 0.5s, 1s, 2s, 4s, 8s
)
```

### Reconnection behavior

- Detects WebSocket disconnection
- Waits with exponential backoff between attempts
- Re-subscribes to all previously subscribed events
- Restores event handlers
- Fails after `max_retries` attempts

## Integration with pytest-asyncio

### Basic test

```python
import pytest
from bidiwave import BiDiClient, StringValue

@pytest.mark.asyncio
async def test_page_title():
    async with await BiDiClient.connect("ws://localhost:9515/session") as client:
        async with await client.browsing.open("https://example.com") as page:
            result = await page.evaluate("document.title")
            match result:
                case StringValue(value=title):
                    assert title == "Example Domain"
```

### Cross-browser parametrized test

```python
@pytest.mark.parametrize("endpoint,browser", [
    ("ws://localhost:9515/session", "chrome"),
    ("ws://localhost:9223/session", "firefox"),
    ("ws://localhost:9516/session", "edge"),
])
@pytest.mark.asyncio
async def test_cross_browser_title(endpoint, browser):
    async with await BiDiClient.connect(endpoint) as client:
        async with await client.browsing.open("https://example.com") as page:
            result = await page.evaluate("document.title")
            match result:
                case StringValue(value=title):
                    assert title == "Example Domain"
```

### With fixtures

```python
# conftest.py
import pytest
from bidiwave import BiDiClient

@pytest.fixture
async def client():
    async with await BiDiClient.connect("ws://localhost:9515/session") as client:
        yield client

@pytest.fixture
async def page(client):
    async with await client.browsing.open("https://example.com") as page:
        yield page
```

## Best Practices

- **Use context managers** — `async with` ensures cleanup of pages and connections.
- **Use `match` for RemoteValue** — pattern matching is type-safe and Pythonic.
- **Subscribe before navigating** — subscribe to events before opening pages.
- **Remove intercepts after use** — network intercepts persist until removed.
- **Remove preload scripts after use** — they apply to all future page loads.
- **Use `user_contexts` for isolation** — separate contexts for separate tests.
- **Set permissions before triggering** — grant/deny before the page requests.
- **Use CDP bridge sparingly** — prefer BiDi methods for cross-browser compatibility.
- **Handle `match` exhaustively** — cover all RemoteValue variants or use a fallback.
- **Use reconnection for long sessions** — prevents test failures from transient drops.

## Common Pitfalls

- **Forgetting to subscribe** — events won't fire without `session.subscribe()`.
- **Not removing intercepts** — blocked URLs persist across tests if not removed.
- **Preload scripts apply globally** — they run on all future page loads until removed.
- **RemoteValue is not a plain value** — use `match` to extract the inner value.
- **Firefox vs Chrome differences** — some BiDi features behave differently across browsers.
- **CDP bridge is Chrome-only** — using CDP bridge on Firefox will fail.
- **Driver required for Chrome/Edge** — Firefox has native BiDi, but Chrome/Edge need drivers.
- **Event handler exceptions** — isolated but logged; check logs if handlers seem to not run.
- **Context vs page confusion** — `page.id` is the browsing context ID used by modules.

## References

- `references/bidi-modules.md` — All 12 BiDi modules reference
- `references/remote-value-patterns.md` — RemoteValue match patterns
- `references/browser-setup.md` — Chrome, Firefox, Edge setup guide
- `references/protocol-reference.md` — W3C WebDriver BiDi spec reference
- `assets/templates/test_cross_browser.py` — Cross-browser test template
- `assets/templates/test_network_intercept.py` — Network interception template
- `assets/templates/test_emulation.py` — Emulation template
- `assets/templates/conftest.py` — pytest-asyncio fixtures for bidiwave
- [bidiwave on GitHub](https://github.com/MathiasPaulenko/bidiwave)
- [bidiwave documentation](https://mathiaspaulenko.github.io/bidiwave/)
- [W3C WebDriver BiDi spec](https://w3c.github.io/webdriver-bidi/)

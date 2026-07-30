# Migration from pyppeteer/pychrome to cdpwave

> Step-by-step guide for migrating browser automation code from pyppeteer or pychrome to cdpwave.

## Why Migrate

| Feature | pyppeteer | pychrome | cdpwave |
|---------|-----------|----------|---------|
| Python 3.11+ | Partial | Yes | Yes |
| Type hints | No | Partial | Full (`mypy --strict`) |
| Async-first | Yes | No (sync) | Yes |
| CDP coverage | Partial | Full (raw) | Full (typed) |
| Browser detection | Bundled Chromium | Manual | Auto-detect Chrome/Edge/Brave |
| WebSocket keepalive | No | No | Yes |
| Escape hatch | No | Yes (raw) | Yes (`session.send()`) |
| Multi-tab sessions | Yes | Manual | Yes (`client.sessions`) |
| Event helpers | Yes | No | Yes (`on()`, `wait_for_event()`) |
| Maintained | Stale | Stale | Active |

## Installation

```bash
# Uninstall old packages (optional)
pip uninstall pyppeteer pychrome

# Install cdpwave
pip install cdpwave
```

## API Mapping: pyppeteer to cdpwave

### Browser launch

**pyppeteer:**
```python
import pyppeteer

browser = await pyppeteer.launch(headless=True)
page = await browser.newPage()
await page.goto("https://example.com")
```

**cdpwave:**
```python
from cdpwave import CDPClient

async with await CDPClient.launch(headless=True) as client:
    session = await client.new_page("https://example.com")
```

### Connect to existing browser

**pyppeteer:**
```python
browser = await pyppeteer.connect(browserWSEndpoint="ws://localhost:9222/devtools/browser/123")
```

**cdpwave:**
```python
async with await CDPClient.connect(host="localhost", port=9222) as client:
    # ...
```

### Evaluate JavaScript

**pyppeteer:**
```python
title = await page.title()
result = await page.evaluate("document.title")
```

**cdpwave:**
```python
result = await session.runtime.evaluate("document.title", return_by_value=True)
title = result["result"]["value"]
```

### Screenshot

**pyppeteer:**
```python
await page.screenshot({"path": "screenshot.png"})
```

**cdpwave:**
```python
screenshot = await session.page.capture_screenshot()
with open("screenshot.png", "wb") as f:
    f.write(bytes.fromhex(screenshot["data"]))
```

### Full-page screenshot

**pyppeteer:**
```python
await page.screenshot({"path": "full.png", "fullPage": True})
```

**cdpwave:**
```python
screenshot = await session.page.capture_screenshot(capture_beyond_viewport=True)
with open("full.png", "wb") as f:
    f.write(bytes.fromhex(screenshot["data"]))
```

### PDF

**pyppeteer:**
```python
await page.pdf({"path": "page.pdf"})
```

**cdpwave:**
```python
pdf = await session.page.print_to_pdf()
with open("page.pdf", "wb") as f:
    f.write(bytes.fromhex(pdf["data"]))
```

### Click

**pyppeteer:**
```python
await page.click("#button")
```

**cdpwave:**
```python
# Get element coordinates via DOM
doc = await session.dom.get_document()
node = await session.dom.query_selector(node_id=doc["root"]["nodeId"], selector="#button")
box = await session.dom.get_box_model(node_id=node["nodeId"])
x = box["model"]["content"][0]
y = box["model"]["content"][1]
await session.input.dispatch_mouse_event(
    type="mousePressed", x=x, y=y, button="left",
)
await session.input.dispatch_mouse_event(
    type="mouseReleased", x=x, y=y, button="left",
)
```

### Type text

**pyppeteer:**
```python
await page.type("#input", "hello world")
```

**cdpwave:**
```python
await session.input.insert_text("hello world")
```

### Wait for selector

**pyppeteer:**
```python
await page.waitForSelector(".dynamic-content", timeout=10000)
```

**cdpwave:**
```python
js = """
() => new Promise((resolve, reject) => {
    const el = document.querySelector('.dynamic-content');
    if (el) return resolve(true);
    const observer = new MutationObserver(() => {
        if (document.querySelector('.dynamic-content')) {
            observer.disconnect();
            resolve(true);
        }
    });
    observer.observe(document.body, {childList: true, subtree: true});
    setTimeout(() => { observer.disconnect(); reject(false); }, 10000);
})
"""
await session.runtime.evaluate(js, await_promise=True, return_by_value=True)
```

### Set viewport

**pyppeteer:**
```python
await page.setViewport({"width": 375, "height": 667})
```

**cdpwave:**
```python
await session.emulation.set_device_metrics_override(
    width=375, height=667, device_scale_factor=2, mobile=True,
)
```

### Cookies

**pyppeteer:**
```python
cookies = await page.cookies()
await page.setCookie({"name": "foo", "value": "bar", "domain": "example.com"})
```

**cdpwave:**
```python
await session.network.enable()
cookies = await session.network.get_cookies()
await session.network.set_cookie(name="foo", value="bar", domain="example.com")
```

### Request interception

**pyppeteer:**
```python
await page.setRequestInterception(True)

async def intercept(request):
    if "ads" in request.url:
        await request.abort()
    else:
        await request.continue_()

page.on("request", intercept)
```

**cdpwave:**
```python
await session.network.enable()
await session.network.set_blocked_urls(["*ads*"])
# Or use Fetch domain for full interception
await session.fetch.enable()
```

### Events

**pyppeteer:**
```python
page.on("console", lambda msg: print(msg.text))
page.on("pageerror", lambda err: print(err))
```

**cdpwave:**
```python
session.on("Runtime.consoleAPICalled", lambda msg: print(msg["args"]))
session.on("Runtime.exceptionThrown", lambda err: print(err["exceptionDetails"]))
```

## API Mapping: pychrome to cdpwave

### Browser connection

**pychrome:**
```python
import pychrome

browser = pychrome.Browser(url="http://localhost:9222")
tab = browser.new_tab()
tab.start()
```

**cdpwave:**
```python
from cdpwave import CDPClient

async with await CDPClient.connect(host="localhost", port=9222) as client:
    session = await client.new_page("https://example.com")
```

### Call CDP method

**pychrome:**
```python
tab.Page.navigate(url="https://example.com")
result = tab.Runtime.evaluate(expression="document.title", returnByValue=True)
```

**cdpwave:**
```python
await session.page.navigate("https://example.com")
result = await session.runtime.evaluate("document.title", return_by_value=True)
```

### Event handling

**pychrome:**
```python
tab.Page.loadEventFired = lambda: print("Page loaded")
```

**cdpwave:**
```python
session.on("Page.loadEventFired", lambda: print("Page loaded"))
await session.wait_for_event("Page.loadEventFired")
```

### Raw CDP call

**pychrome:**
```python
result = tab.call_method("Performance.getMetrics")
```

**cdpwave:**
```python
result = await session.send("Performance.getMetrics", {})
```

## Key Differences

### Return format

pyppeteer returns values directly. cdpwave returns CDP response dicts:

```python
# pyppeteer
title = await page.title()  # "Example Domain"

# cdpwave
result = await session.runtime.evaluate("document.title", return_by_value=True)
title = result["result"]["value"]  # "Example Domain"
```

### Sync vs async

pychrome is synchronous. cdpwave is fully async:

```python
# pychrome (sync)
tab.Page.navigate(url="https://example.com")

# cdpwave (async)
await session.page.navigate("https://example.com")
```

### Browser management

pyppeteer downloads its own Chromium. cdpwave uses your installed browser:

```python
# pyppeteer — downloads Chromium on first run
browser = await pyppeteer.launch()

# cdpwave — detects Chrome, Edge, Brave, or Chromium
client = await CDPClient.launch()
```

### Context manager

cdpwave encourages context managers for cleanup:

```python
# cdpwave — automatic cleanup
async with await CDPClient.launch() as client:
    session = await client.new_page("https://example.com")
    # Cleanup on exit

# pyppeteer — manual cleanup
browser = await pyppeteer.launch()
try:
    page = await browser.newPage()
    # ...
finally:
    await browser.close()
```

## Migration Checklist

- [ ] Replace `pyppeteer.launch()` with `CDPClient.launch()`
- [ ] Replace `pyppeteer.connect()` with `CDPClient.connect()`
- [ ] Replace `browser.newPage()` with `client.new_page()`
- [ ] Replace `page.goto()` with `session.page.navigate()`
- [ ] Replace `page.evaluate()` with `session.runtime.evaluate()`
- [ ] Replace `page.screenshot()` with `session.page.capture_screenshot()`
- [ ] Replace `page.pdf()` with `session.page.print_to_pdf()`
- [ ] Replace `page.setViewport()` with `session.emulation.set_device_metrics_override()`
- [ ] Replace `page.cookies()` with `session.network.get_cookies()`
- [ ] Replace `page.type()` with `session.input.insert_text()`
- [ ] Replace `page.click()` with DOM query + `session.input.dispatch_mouse_event()`
- [ ] Replace `page.waitForSelector()` with JS Promise + `runtime.evaluate(await_promise=True)`
- [ ] Replace `page.on("console")` with `session.on("Runtime.consoleAPICalled")`
- [ ] Replace `page.on("pageerror")` with `session.on("Runtime.exceptionThrown")`
- [ ] Replace `page.on("request")` with `session.on("Network.requestWillBeSent")`
- [ ] Replace `page.on("response")` with `session.on("Network.responseReceived")`
- [ ] Replace `pychrome.Browser()` with `CDPClient.connect()`
- [ ] Replace `tab.call_method()` with `session.send()`
- [ ] Add `await` to all CDP calls (if coming from pychrome)
- [ ] Update result access from direct values to `result["result"]["value"]`
- [ ] Remove pyppeteer Chromium download dependency
- [ ] Add `async with` context managers for automatic cleanup

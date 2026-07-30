# Migration Guide — From pyppeteer / pychrome to cdpwave

> Step-by-step migration from pyppeteer or pychrome to cdpwave.

## Why Migrate?

| Problem | pyppeteer / pychrome | cdpwave |
|---------|----------------------|---------|
| Type safety | Untyped responses | Typed dicts, `mypy --strict` |
| CDP coverage | Partial | Full 60 domains, 689 methods |
| Maintenance | pyppeteer unmaintained | Actively maintained |
| Async | pyppeteer uses custom loop | Standard `asyncio` |
| Escape hatch | None | `session.send("Any.CDPMethod", params)` |
| Browser detection | Manual | Auto-detect Chrome, Edge, Brave, Chromium |
| Multi-tab | Complex | `client.sessions` property, native |
| Event handling | Basic | `session.on()`, `session.wait_for_event()` |

## Migration Steps

### 1. Install cdpwave

```bash
pip install cdpwave
```

### 2. Replace browser launch

**pyppeteer:**
```python
import pyppeteer

async def main():
    browser = await pyppeteer.launch(headless=True)
    page = await browser.newPage()
    await page.goto("https://example.com")
    # ...
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
```

**cdpwave:**
```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        # ...
        await session.close()

asyncio.run(main())
```

### 3. Replace page evaluation

**pyppeteer:**
```python
title = await page.evaluate("document.title")
```

**cdpwave:**
```python
result = await session.runtime.evaluate("document.title", return_by_value=True)
title = result["result"]["value"]
```

### 4. Replace screenshots

**pyppeteer:**
```python
await page.screenshot({"path": "out.png"})
```

**cdpwave:**
```python
screenshot = await session.page.capture_screenshot()
with open("out.png", "wb") as f:
    f.write(bytes.fromhex(screenshot["data"]))
```

### 5. Replace navigation

**pyppeteer:**
```python
await page.goto("https://example.com")
await page.goBack()
await page.goForward()
await page.reload()
```

**cdpwave:**
```python
await session.page.navigate("https://example.com")
# Navigation history is available via session.page
```

### 6. Replace event handling

**pyppeteer:**
```python
page.on("console", lambda msg: print(msg.text))
```

**cdpwave:**
```python
def on_console(msg):
    print(f"[console] {msg['args']}")

session.on("Runtime.consoleAPICalled", on_console)
```

### 7. Replace multi-tab

**pyppeteer:**
```python
page1 = await browser.newPage()
page2 = await browser.newPage()
```

**cdpwave:**
```python
tab1 = await client.new_page("https://example.com")
tab2 = await client.new_page("https://example.org")
# Each tab is an independent Session with its own method namespace
```

### 8. Use the escape hatch

For any CDP method that cdpwave doesn't have a typed wrapper for:

```python
result = await session.send("Performance.getMetrics", {})
print(result["metrics"])
```

## API Mapping Table

| pyppeteer | cdpwave |
|-----------|---------|
| `pyppeteer.launch()` | `CDPClient.launch()` |
| `pyppeteer.connect()` | `CDPClient.connect(host=, port=)` |
| `browser.newPage()` | `client.new_page(url)` |
| `browser.close()` | Context exit (`async with`) |
| `page.goto(url)` | `session.page.navigate(url)` |
| `page.evaluate(expr)` | `session.runtime.evaluate(expr, return_by_value=True)` |
| `page.screenshot()` | `session.page.capture_screenshot()` |
| `page.content()` | `session.dom.get_document()` |
| `page.click(selector)` | JS via `session.runtime.evaluate()` |
| `page.type(selector, text)` | JS via `session.runtime.evaluate()` |
| `page.waitForSelector(selector)` | JS via `session.runtime.evaluate()` with polling |
| `page.waitForFunction(fn)` | `session.wait_for_event("Page.loadEventFired")` |
| `page.on("console", handler)` | `session.on("Runtime.consoleAPICalled", handler)` |
| `page.cookies()` | `session.network.get_cookies()` |
| `page.setCookie(cookie)` | `session.network.set_cookie(...)` |
| `page.emulate(options)` | `session.emulation.set_device_metrics_override(...)` |

## pychrome Migration

pychrome is a synchronous CDP client. Migration to cdpwave adds async + types:

**pychrome:**
```python
import pychrome

browser = pychrome.Browser(url="http://localhost:9222")
tab = browser.new_tab()
tab.start()
tab.Page.navigate(url="https://example.com")
tab.Runtime.evaluate(expression="document.title")
tab.stop()
```

**cdpwave:**
```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.connect(host="localhost", port=9222) as client:
        session = await client.new_page("https://example.com")
        result = await session.runtime.evaluate("document.title", return_by_value=True)
        print(result["result"]["value"])
        await session.close()

asyncio.run(main())
```

Key differences:
- Async instead of sync (use `asyncio.run()`)
- Typed responses instead of raw dicts
- Context manager for automatic cleanup
- Method names use `snake_case` instead of `dot.notation`

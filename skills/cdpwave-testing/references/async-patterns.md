# Async Patterns for CDP Testing

> asyncio patterns for writing robust CDP-level browser tests with cdpwave.

## Core async Concepts

### Event loop

cdpwave is async-first, built on `asyncio`. All CDP calls are coroutines:

```python
import asyncio
from cdpwave import CDPClient

async def main():
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        result = await session.runtime.evaluate("document.title", return_by_value=True)
        print(result["result"]["value"])

asyncio.run(main())
```

### Concurrent operations

Use `asyncio.gather` for parallel CDP calls:

```python
async def test_parallel_eval(session):
    results = await asyncio.gather(
        session.runtime.evaluate("document.title", return_by_value=True),
        session.runtime.evaluate("document.URL", return_by_value=True),
        session.runtime.evaluate("document.querySelectorAll('a').length", return_by_value=True),
    )
    title = results[0]["result"]["value"]
    url = results[1]["result"]["value"]
    link_count = results[2]["result"]["value"]
```

### Multi-tab concurrency

```python
async def test_multi_tab_concurrent():
    async with await CDPClient.launch(headless=True) as client:
        tab1 = await client.new_page("https://example.com")
        tab2 = await client.new_page("https://example.org")

        results = await asyncio.gather(
            tab1.runtime.evaluate("document.title", return_by_value=True),
            tab2.runtime.evaluate("document.title", return_by_value=True),
        )

        assert results[0]["result"]["value"] == "Example Domain"
        assert results[1]["result"]["value"] == "IANA-managed domains"

        await tab1.close()
        await tab2.close()
```

## Waiting Patterns

### Wait for event

```python
async def test_wait_for_load(session):
    await session.page.enable()
    await session.page.navigate("https://example.com")
    await session.wait_for_event("Page.loadEventFired")
    # Page is fully loaded
```

### Wait with timeout

```python
async def test_wait_with_timeout(session):
    await session.page.navigate("https://example.com")
    try:
        await asyncio.wait_for(
            session.wait_for_event("Page.loadEventFired"),
            timeout=10,
        )
    except asyncio.TimeoutError:
        pytest.fail("Page did not load within 10 seconds")
```

### Wait for selector (via JS)

```python
async def wait_for_selector(session, selector: str, timeout: float = 10):
    js = f"""
    () => new Promise((resolve, reject) => {{
        const el = document.querySelector('{selector}');
        if (el) return resolve(true);
        const observer = new MutationObserver(() => {{
            if (document.querySelector('{selector}')) {{
                observer.disconnect();
                resolve(true);
            }}
        }});
        observer.observe(document.body, {{childList: true, subtree: true}});
        setTimeout(() => {{ observer.disconnect(); reject(false); }}, {timeout * 1000});
    }})
    """
    await session.runtime.evaluate(js, await_promise=True, return_by_value=True)

async def test_wait_for_dynamic_content(session):
    await session.page.navigate("https://example.com")
    await wait_for_selector(session, ".dynamic-content", timeout=15)
    # Element is now present
```

### Polling pattern

```python
async def poll_until(session, condition_js: str, interval: float = 0.5, timeout: float = 10):
    elapsed = 0
    while elapsed < timeout:
        result = await session.runtime.evaluate(condition_js, return_by_value=True)
        if result["result"].get("value"):
            return True
        await asyncio.sleep(interval)
        elapsed += interval
    return False

async def test_poll_for_value(session):
    await session.page.navigate("https://example.com")
    found = await poll_until(
        session,
        "document.querySelector('.counter')?.textContent === '100'",
        timeout=20,
    )
    assert found, "Counter did not reach 100"
```

## Event Collection Patterns

### Collect events during navigation

```python
async def test_collect_network_events(session):
    requests = []
    responses = []

    session.on("Network.requestWillBeSent", lambda e: requests.append(e))
    session.on("Network.responseReceived", lambda e: responses.append(e))

    await session.network.enable()
    await session.page.navigate("https://example.com")
    await session.wait_for_event("Page.loadEventFired")

    assert len(requests) > 0
    assert len(responses) > 0
```

### Filter events

```python
async def test_filter_xhr_requests(session):
    xhr_requests = []

    def on_request(event):
        if event.get("type") == "XHR":
            xhr_requests.append(event)

    session.on("Network.requestWillBeSent", on_request)

    await session.network.enable()
    await session.page.navigate("https://example.com")
    await session.wait_for_event("Page.loadEventFired")

    # Only XHR requests
    for req in xhr_requests:
        assert "api" in req["request"]["url"]
```

### Event with async callback

```python
async def test_async_event_handler(session):
    results = []

    async def on_response(event):
        # Async processing
        body = await session.network.get_response_body(request_id=event["requestId"])
        results.append(body)

    session.on("Network.responseReceived", lambda e: asyncio.create_task(on_response(e)))

    await session.network.enable()
    await session.page.navigate("https://example.com")
    await session.wait_for_event("Page.loadEventFired")
    await asyncio.sleep(1)  # Allow async handlers to complete
```

## Error Handling Patterns

### Try/except with CDP calls

```python
async def test_handle_navigation_error(session):
    try:
        await session.page.navigate("https://nonexistent.example")
        await session.wait_for_event("Page.loadEventFired", timeout=5)
    except asyncio.TimeoutError:
        # Expected for non-resolving domain
        pass
```

### Assert on JS exceptions

```python
async def test_catch_js_exception(session):
    exceptions = []
    session.on("Runtime.exceptionThrown", lambda e: exceptions.append(e))
    await session.runtime.enable()

    await session.runtime.evaluate("undefinedVar.foo")

    assert len(exceptions) == 1
    assert "undefinedVar" in exceptions[0]["exceptionDetails"]["text"]
```

### Cleanup pattern

```python
async def test_with_cleanup():
    client = await CDPClient.launch(headless=True)
    try:
        session = await client.new_page("https://example.com")
        result = await session.runtime.evaluate("document.title", return_by_value=True)
        assert result["result"]["value"] == "Example Domain"
    finally:
        await client.close()
```

## pytest-asyncio Patterns

### Fixture with setup/teardown

```python
@pytest.fixture
async def browser():
    client = await CDPClient.launch(headless=True)
    yield client
    await client.close()

@pytest.fixture
async def page(browser):
    session = await browser.new_page("https://example.com")
    await session.page.enable()
    yield session
    await session.close()
```

### Parametrized tests

```python
@pytest.mark.parametrize("url,title", [
    ("https://example.com", "Example Domain"),
    ("https://example.org", "IANA-managed domains"),
])
@pytest.mark.asyncio
async def test_page_titles(page, url, title):
    await page.page.navigate(url)
    await page.wait_for_event("Page.loadEventFired")
    result = await page.runtime.evaluate("document.title", return_by_value=True)
    assert result["result"]["value"] == title
```

### Session-scoped browser

```python
@pytest.fixture(scope="session")
async def browser():
    client = await CDPClient.launch(headless=True)
    yield client
    await client.close()

@pytest.fixture
async def page(browser):
    """Each test gets a fresh tab."""
    session = await browser.new_page("about:blank")
    yield session
    await session.close()
```

## Timeout Patterns

### Global timeout

```python
async def test_with_global_timeout():
    async with asyncio.timeout(30):
        async with await CDPClient.launch(headless=True) as client:
            session = await client.new_page("https://example.com")
            await session.wait_for_event("Page.loadEventFired")
            # ... test logic ...
```

### Per-step timeout

```python
async def test_per_step_timeout(session):
    # Navigate with 10s timeout
    await asyncio.wait_for(
        session.page.navigate("https://example.com"),
        timeout=10,
    )
    # Wait for load with 15s timeout
    await asyncio.wait_for(
        session.wait_for_event("Page.loadEventFired"),
        timeout=15,
    )
    # Evaluate with 5s timeout
    result = await asyncio.wait_for(
        session.runtime.evaluate("document.title", return_by_value=True),
        timeout=5,
    )
```

## Retry Patterns

### Retry on failure

```python
async def retry_async(coro_factory, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            return await coro_factory()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(delay)

async def test_with_retry(session):
    result = await retry_async(
        lambda: session.runtime.evaluate("document.title", return_by_value=True),
        max_retries=3,
    )
    assert result["result"]["value"]
```

### Retry with backoff

```python
async def retry_with_backoff(coro_factory, max_retries=5, base_delay=0.5):
    for attempt in range(max_retries):
        try:
            return await coro_factory()
        except Exception:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            await asyncio.sleep(delay)
```

## CI-Specific Patterns

### Headless with no-sandbox

```python
@pytest.fixture
async def client():
    async with await CDPClient.launch(
        headless=True,
        extra_args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
    ) as client:
        yield client
```

### Screenshot on failure

```python
@pytest.fixture
async def session(client):
    session = await client.new_page("about:blank")
    yield session
    # Take screenshot on failure
    if hasattr(session, "_test_failed"):
        screenshot = await session.page.capture_screenshot()
        with open(f"failure_{session._test_name}.png", "wb") as f:
            f.write(bytes.fromhex(screenshot["data"]))
    await session.close()
```

### Parallel test isolation

```python
@pytest.fixture
async def isolated_session(client):
    """Each test gets its own tab with clean state."""
    session = await client.new_page("about:blank")
    yield session
    await session.close()
```

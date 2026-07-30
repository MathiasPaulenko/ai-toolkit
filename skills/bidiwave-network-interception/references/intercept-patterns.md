# Common Interception Patterns

> Recipes for common network interception scenarios with bidiwave.

## Pattern 1: Block All Ads and Trackers

```python
async def block_ads(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=[
            "*/google-analytics.com/*",
            "*/googletagmanager.com/*",
            "*/doubleclick.net/*",
            "*/facebook.net/*",
            "*/facebook.com/tr*",
            "*/amazon-adsystem.com/*",
            "*/criteo.com/*",
            "*/hotjar.com/*",
            "*/segment.com/*",
            "*/mixpanel.com/*",
            "*/adservice.google.com/*",
            "*/ads.yahoo.com/*",
            "*/bing.com/ads/*",
            "*/taboola.com/*",
            "*/outbrain.com/*"
        ]
    )

    async for event in session.network.stream_intercepted_requests():
        await session.network.continue_response(
            request_id=event["requestId"],
            status_code=403
        )
```

## Pattern 2: Block All Images for Faster Load

```python
async def block_images(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*"],
        resource_types=["image", "media"]
    )

    async for event in session.network.stream_intercepted_requests():
        await session.network.continue_response(
            request_id=event["requestId"],
            status_code=403
        )
```

## Pattern 3: Mock API Endpoints

```python
async def mock_api(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/api/*"]
    )

    mocks = {
        "*/api/users": (200, '{"users": [{"id": 1, "name": "Alice"}]}'),
        "*/api/products": (200, '{"products": [{"id": 1, "name": "Widget"}]}'),
        "*/api/error": (500, '{"error": "Internal Server Error"}'),
        "*/api/notfound": (404, '{"error": "Not Found"}'),
        "*/api/rate-limited": (429, '{"error": "Too Many Requests"}'),
    }

    async for event in session.network.stream_intercepted_requests():
        url = event["request"]["url"]
        matched = False

        for pattern, (status, body) in mocks.items():
            import fnmatch
            if fnmatch.fnmatch(url, f"*{pattern}*"):
                await session.network.provide_response(
                    request_id=event["requestId"],
                    status_code=status,
                    headers={"Content-Type": "application/json"},
                    body=body
                )
                matched = True
                break

        if not matched:
            await session.network.continue_request(
                request_id=event["requestId"]
            )
```

## Pattern 4: Add Auth Headers

```python
import os

async def add_auth(session):
    token = os.environ.get("TEST_API_TOKEN", "default-token")

    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/api/*"]
    )

    async for event in session.network.stream_intercepted_requests():
        headers = event["request"]["headers"]
        headers["Authorization"] = f"Bearer {token}"

        await session.network.continue_request(
            request_id=event["requestId"],
            headers=headers
        )
```

## Pattern 5: Redirect Staging to Production

```python
async def redirect_staging_to_prod(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*staging.example.com*"]
    )

    async for event in session.network.stream_intercepted_requests():
        original_url = event["request"]["url"]
        new_url = original_url.replace("staging.example.com", "production.example.com")

        await session.network.continue_request(
            request_id=event["requestId"],
            url=new_url
        )
```

## Pattern 6: Bypass Cache

```python
async def bypass_cache(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*"]
    )

    async for event in session.network.stream_intercepted_requests():
        headers = event["request"]["headers"]
        headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        headers["Pragma"] = "no-cache"

        await session.network.continue_request(
            request_id=event["requestId"],
            headers=headers
        )
```

## Pattern 7: Strip Cookies

```python
async def strip_cookies(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*"]
    )

    async for event in session.network.stream_intercepted_requests():
        headers = event["request"]["headers"]
        headers.pop("Cookie", None)
        headers.pop("cookie", None)

        await session.network.continue_request(
            request_id=event["requestId"],
            headers=headers
        )
```

## Pattern 8: Handle HTTP Basic Auth

```python
async def handle_basic_auth(session):
    intercept = await session.network.add_intercept(
        phases=["authRequired"],
        url_patterns=["*"]
    )

    async for event in session.network.stream_auth_required():
        await session.network.continue_with_auth(
            request_id=event["requestId"],
            credentials={
                "type": "password",
                "username": "testuser",
                "password": "testpass"
            }
        )
```

## Pattern 9: Collect All API Traffic

```python
async def collect_api_traffic(session):
    collector = await session.network.add_data_collector(
        url_patterns=["*/api/*"],
        include_request_bodies=True,
        include_response_bodies=True,
        include_headers=True
    )

    await session.browsing_context.navigate(url="https://example.com")

    data = await session.network.get_collected_data(
        collector_id=collector["collectorId"]
    )

    for entry in data["networkEntries"]:
        req = entry["request"]
        resp = entry.get("response", {})
        print(f"{req['method']} {req['url']} -> {resp.get('status', 'N/A')}")

    await session.network.remove_data_collector(
        collector_id=collector["collectorId"]
    )
```

## Pattern 10: Simulate Slow Network

```python
async def simulate_slow_network(session, delay_seconds: float = 2.0):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/api/*"]
    )

    async for event in session.network.stream_intercepted_requests():
        await asyncio.sleep(delay_seconds)
        await session.network.continue_request(
            request_id=event["requestId"]
        )
```

## Pattern 11: Log All Network Traffic

```python
async def log_traffic(session):
    async for event in session.network.stream_response_completed():
        url = event["request"]["url"]
        status = event["response"]["status"]
        mime = event["response"]["mimeType"]
        size = event["response"]["bodySize"]
        time_ms = event["response"]["timings"].get("total", 0)

        print(f"[{status}] {mime:30s} {size:>8}B {time_ms:>8.0f}ms {url}")
```

## Pattern 12: Modify Response Headers

```python
async def modify_response_headers(session):
    intercept = await session.network.add_intercept(
        phases=["responseStarted"],
        url_patterns=["*"]
    )

    async for event in session.network.stream_intercepted_requests():
        headers = event.get("response", {}).get("headers", {})
        headers["X-Intercepted"] = "true"
        headers["X-Frame-Options"] = "DENY"

        await session.network.continue_response(
            request_id=event["requestId"],
            headers=headers
        )
```

## References

- `references/bidi-network-module.md` — BiDi network module API reference
- [WebDriver BiDi — Network module](https://w3c.github.io/webdriver-bidi/#module-network)

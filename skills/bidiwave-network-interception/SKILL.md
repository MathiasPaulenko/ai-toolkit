---
name: BiDiWave Network Interception
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Network interception with bidiwave. Block requests, modify requests, mock responses, auth handling, cache control, response body retrieval."
tags: [network-interception, bidi, mocking, request-modification]
trigger: When the user asks about network interception with bidiwave, needs to block or modify requests, wants to mock responses, needs auth handling, or wants to retrieve response bodies.
---

# BiDiWave Network Interception

## Description

Network interception with bidiwave — block requests by pattern, modify request headers and bodies, mock responses with custom status codes, handle authentication, control cache behavior, and retrieve response bodies using the BiDi network module.

## When to Invoke

- Blocking requests by URL pattern (ads, trackers, third-party scripts)
- Modifying request headers or bodies before they reach the server
- Mocking API responses for testing
- Handling authentication headers automatically
- Controlling cache behavior for performance testing
- Retrieving response bodies for inspection
- Tracking all network requests and responses with data collectors

## Prerequisites

- `pip install bidiwave`
- Chrome or Edge with BiDi support (Chrome 112+)
- Basic familiarity with bidiwave (see `bidiwave-cross-browser` skill)
- Python 3.11+ with `asyncio`

## Network Interception

### network.add_intercept()

The BiDi network module provides `network.add_intercept()` to intercept requests at specific phases:

```python
import asyncio
from bidiwave import BiDiSession

async def basic_intercept():
    session = await BiDiSession.connect("ws://localhost:9222")

    # Add an intercept for all requests before they are sent
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*"]
    )

    # Remove the intercept when done
    await session.network.remove_intercept(intercept_id=intercept["interceptId"])

    await session.close()
```

### Interception phases

| Phase | Description | When it fires |
|-------|-------------|---------------|
| `beforeRequestSent` | Before request is sent to server | Request headers and body can be modified |
| `responseStarted` | When response headers arrive | Response headers can be modified, body can be mocked |
| `authRequired` | When authentication is required | Auth credentials can be provided |

### URL patterns

BiDi supports glob-style URL patterns:

| Pattern | Matches |
|---------|---------|
| `*` | All URLs |
| `*/api/*` | Any URL containing `/api/` |
| `https://example.com/*` | Any URL on example.com |
| `*/analytics.js` | Any URL ending in `/analytics.js` |
| `https://*.example.com/*` | Any subdomain of example.com |

## Blocking Requests

### Block by URL pattern

```python
async def block_requests(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=[
            "*/google-analytics.com/*",
            "*/googletagmanager.com/*",
            "*/doubleclick.net/*",
            "*/facebook.net/*"
        ]
    )

    # Subscribe to network events to see blocked requests
    async for event in session.network.stream_blocked_requests():
        print(f"Blocked: {event['request']['url']}")

    await session.network.remove_intercept(intercept_id=intercept["interceptId"])
```

### Block all third-party requests

```python
async def block_third_party(session, first_party_domain: str):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*"]
    )

    async for event in session.network.stream_intercepted_requests():
        url = event["request"]["url"]
        if first_party_domain not in url:
            # Block the request
            await session.network.continue_response(
                request_id=event["requestId"],
                status_code=403
            )
        else:
            # Allow the request to proceed
            await session.network.continue_request(
                request_id=event["requestId"]
            )

    await session.network.remove_intercept(intercept_id=intercept["interceptId"])
```

### Block by resource type

```python
async def block_images(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*"],
        resource_types=["image"]  # block only images
    )

    async for event in session.network.stream_intercepted_requests():
        await session.network.continue_response(
            request_id=event["requestId"],
            status_code=403
        )
```

### Resource types

| Type | Description |
|------|-------------|
| `document` | HTML documents |
| `script` | JavaScript files |
| `stylesheet` | CSS files |
| `image` | Image files |
| `media` | Audio/video |
| `font` | Font files |
| `xhr` | XMLHttpRequest |
| `fetch` | Fetch API |
| `websocket` | WebSocket |
| `manifest` | Manifest files |
| `other` | Other |

## Modifying Requests

### Modify request headers

```python
async def modify_headers(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/api/*"]
    )

    async for event in session.network.stream_intercepted_requests():
        # Add custom headers
        headers = event["request"]["headers"]
        headers["Authorization"] = "Bearer test-token-123"
        headers["X-Test-Environment"] = "true"
        headers["X-Request-ID"] = "test-001"

        await session.network.continue_request(
            request_id=event["requestId"],
            headers=headers
        )

    await session.network.remove_intercept(intercept_id=intercept["interceptId"])
```

### Remove headers

```python
async def remove_headers(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*"]
    )

    async for event in session.network.stream_intercepted_requests():
        headers = event["request"]["headers"]
        # Remove cookies for testing
        headers.pop("Cookie", None)
        headers.pop("cookie", None)

        await session.network.continue_request(
            request_id=event["requestId"],
            headers=headers
        )
```

### Modify request body

```python
async def modify_body(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/api/submit*"]
    )

    async for event in session.network.stream_intercepted_requests():
        # Replace the request body
        new_body = '{"name": "Test User", "email": "test@example.com"}'

        await session.network.continue_request(
            request_id=event["requestId"],
            body=new_body
        )
```

### Modify request URL

```python
async def redirect_requests(session, from_domain: str, to_domain: str):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=[f"*{from_domain}*"]
    )

    async for event in session.network.stream_intercepted_requests():
        original_url = event["request"]["url"]
        new_url = original_url.replace(from_domain, to_domain)

        await session.network.continue_request(
            request_id=event["requestId"],
            url=new_url
        )
```

### Modify request method

```python
async def change_method(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/api/data*"]
    )

    async for event in session.network.stream_intercepted_requests():
        await session.network.continue_request(
            request_id=event["requestId"],
            method="POST"
        )
```

## Mocking Responses

### Mock with custom status and body

```python
async def mock_response(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/api/users*"]
    )

    async for event in session.network.stream_intercepted_requests():
        mock_body = '{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}'

        await session.network.provide_response(
            request_id=event["requestId"],
            status_code=200,
            headers={"Content-Type": "application/json"},
            body=mock_body
        )
```

### Mock error responses

```python
async def mock_errors(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/api/*"]
    )

    async for event in session.network.stream_intercepted_requests():
        url = event["request"]["url"]

        if "/api/error" in url:
            await session.network.provide_response(
                request_id=event["requestId"],
                status_code=500,
                headers={"Content-Type": "application/json"},
                body='{"error": "Internal Server Error"}'
            )
        elif "/api/notfound" in url:
            await session.network.provide_response(
                request_id=event["requestId"],
                status_code=404,
                headers={"Content-Type": "application/json"},
                body='{"error": "Not Found"}'
            )
        elif "/api/rate-limited" in url:
            await session.network.provide_response(
                request_id=event["requestId"],
                status_code=429,
                headers={"Content-Type": "application/json", "Retry-After": "60"},
                body='{"error": "Too Many Requests"}'
            )
        else:
            await session.network.continue_request(
                request_id=event["requestId"]
            )
```

### Mock with delay

```python
async def mock_with_delay(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/api/slow*"]
    )

    async for event in session.network.stream_intercepted_requests():
        # Simulate slow response
        await asyncio.sleep(3)

        await session.network.provide_response(
            request_id=event["requestId"],
            status_code=200,
            headers={"Content-Type": "application/json"},
            body='{"data": "delayed response"}'
        )
```

### Mock redirect

```python
async def mock_redirect(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/old-page*"]
    )

    async for event in session.network.stream_intercepted_requests():
        await session.network.provide_response(
            request_id=event["requestId"],
            status_code=301,
            headers={"Location": "https://example.com/new-page"}
        )
```

## Authentication Handling

### Provide credentials

```python
async def handle_auth(session):
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

    await session.network.remove_intercept(intercept_id=intercept["interceptId"])
```

### Cancel authentication

```python
async def cancel_auth(session):
    intercept = await session.network.add_intercept(
        phases=["authRequired"],
        url_patterns=["*"]
    )

    async for event in session.network.stream_auth_required():
        await session.network.continue_with_auth(
            request_id=event["requestId"],
            credentials={"type": "cancel"}
        )
```

### Provide proxy auth

```python
async def proxy_auth(session):
    intercept = await session.network.add_intercept(
        phases=["authRequired"],
        url_patterns=["*"]
    )

    async for event in session.network.stream_auth_required():
        await session.network.continue_with_auth(
            request_id=event["requestId"],
            credentials={
                "type": "proxy",
                "username": "proxyuser",
                "password": "proxypass"
            }
        )
```

## Cache Control

### Override cache behavior

```python
async def bypass_cache(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*"]
    )

    async for event in session.network.stream_intercepted_requests():
        # Force no-cache by adding cache-control header
        headers = event["request"]["headers"]
        headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        headers["Pragma"] = "no-cache"

        await session.network.continue_request(
            request_id=event["requestId"],
            headers=headers
        )
```

### Force cache hit

```python
async def force_cache(session):
    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/static/*"]
    )

    async for event in session.network.stream_intercepted_requests():
        headers = event["request"]["headers"]
        headers["Cache-Control"] = "max-age=86400"

        await session.network.continue_request(
            request_id=event["requestId"],
            headers=headers
        )
```

## Response Body Retrieval

### Get response body

```python
async def get_response_body(session, network_id: str):
    result = await session.network.get_response_body(
        network_id=network_id
    )
    # Returns: { "body": "...", "base64Encoded": bool }

    if result["base64Encoded"]:
        import base64
        body = base64.b64decode(result["body"])
    else:
        body = result["body"]

    return body
```

### Track all responses

```python
async def track_responses(session):
    # Subscribe to response completed events
    async for event in session.network.stream_response_completed():
        url = event["request"]["url"]
        status = event["response"]["status"]
        mime_type = event["response"]["mimeType"]
        body_size = event["response"]["bodySize"]

        print(f"{status} {mime_type} {body_size}B — {url}")

        # Get the response body
        if "text" in event["response"]:
            body = event["response"]["text"][:200]
            print(f"  Body preview: {body}")
```

## Data Collectors

BiDi data collectors track network requests and responses for analysis:

```python
async def collect_network_data(session):
    # Start a network data collector
    collector = await session.network.add_data_collector(
        url_patterns=["*/api/*"],
        include_request_bodies=True,
        include_response_bodies=True
    )

    # Navigate and interact
    await session.browsing_context.navigate(url="https://example.com")

    # Retrieve collected data
    data = await session.network.get_collected_data(
        collector_id=collector["collectorId"]
    )

    for entry in data["networkEntries"]:
        print(f"Request: {entry['request']['method']} {entry['request']['url']}")
        print(f"Response: {entry['response']['status']}")
        if "body" in entry.get("response", {}):
            print(f"Body: {entry['response']['body'][:200]}")

    await session.network.remove_data_collector(
        collector_id=collector["collectorId"]
    )
```

### Data collector options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `url_patterns` | `array` | `["*"]` | URL patterns to collect |
| `include_request_bodies` | `bool` | `false` | Include request bodies |
| `include_response_bodies` | `bool` | `false` | Include response bodies |
| `include_cookies` | `bool` | `false` | Include cookies |
| `include_headers` | `bool` | `true` | Include headers |

## Combined Interception Example

```python
import asyncio
from bidiwave import BiDiSession

async def combined_interception():
    session = await BiDiSession.connect("ws://localhost:9222")

    # 1. Block trackers
    block_intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=[
            "*/google-analytics.com/*",
            "*/googletagmanager.com/*",
            "*/facebook.net/*"
        ]
    )

    # 2. Mock API responses
    mock_intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/api/users*"]
    )

    # 3. Add auth headers to API calls
    header_intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/api/*"]
    )

    # Start a data collector
    collector = await session.network.add_data_collector(
        url_patterns=["*/api/*"],
        include_response_bodies=True
    )

    # Navigate
    await session.browsing_context.navigate(url="https://example.com")

    # Process intercepted requests
    async for event in session.network.stream_intercepted_requests():
        url = event["request"]["url"]

        if "google-analytics" in url or "facebook" in url:
            await session.network.continue_response(
                request_id=event["requestId"],
                status_code=403
            )
        elif "/api/users" in url:
            await session.network.provide_response(
                request_id=event["requestId"],
                status_code=200,
                headers={"Content-Type": "application/json"},
                body='{"users": [{"id": 1, "name": "Alice"}]}'
            )
        elif "/api/" in url:
            headers = event["request"]["headers"]
            headers["Authorization"] = "Bearer test-token"
            await session.network.continue_request(
                request_id=event["requestId"],
                headers=headers
            )
        else:
            await session.network.continue_request(
                request_id=event["requestId"]
            )

    # Get collected data
    data = await session.network.get_collected_data(
        collector_id=collector["collectorId"]
    )

    # Clean up
    await session.network.remove_intercept(intercept_id=block_intercept["interceptId"])
    await session.network.remove_intercept(intercept_id=mock_intercept["interceptId"])
    await session.network.remove_intercept(intercept_id=header_intercept["interceptId"])
    await session.network.remove_data_collector(collector_id=collector["collectorId"])
    await session.close()

asyncio.run(combined_interception())
```

## Best Practices

- **Remove intercepts when done** — leftover intercepts affect all subsequent navigation.
- **Use specific URL patterns** — `*` intercepts everything and adds overhead.
- **Always handle unmatched requests** — use `continue_request()` as a fallback.
- **Mock at `beforeRequestSent`** — prevents real network calls entirely.
- **Use data collectors for analysis** — less overhead than streaming events.
- **Batch intercepts by purpose** — one for blocking, one for mocking, one for headers.
- **Handle auth at `authRequired` phase** — not at `beforeRequestSent`.
- **Use `provide_response()` for mocks** — not `continue_response()` which expects a real response.
- **Decode base64 bodies** — check `base64Encoded` flag before using response bodies.
- **Test with and without intercepts** — ensure intercepts don't break normal behavior.

## Common Pitfalls

- **Forgetting to remove intercepts** — intercepts persist until removed or session closes.
- **Not handling all intercepted requests** — unhandled requests hang indefinitely.
- **Wrong phase for mocking** — `responseStarted` is too late to mock; use `beforeRequestSent`.
- **Overlapping URL patterns** — multiple intercepts matching the same URL cause conflicts.
- **Blocking too broadly** — `*` pattern blocks everything including the page itself.
- **Not decoding base64** — binary responses are base64-encoded in the protocol.
- **Auth credentials in code** — use environment variables for credentials.
- **Missing `continue_request()` fallback** — always provide a default path.

## References

- `references/bidi-network-module.md` — BiDi network module API reference
- `references/intercept-patterns.md` — Common interception patterns
- `assets/templates/block-ads.py` — Ad blocking template
- `assets/templates/mock-api.py` — API mocking template
- `assets/templates/modify-headers.py` — Header modification template
- [WebDriver BiDi Specification — Network](https://w3c.github.io/webdriver-bidi/#module-network)
- [BiDiWave documentation](https://github.com/MathiasPaulenko/bidiwave)

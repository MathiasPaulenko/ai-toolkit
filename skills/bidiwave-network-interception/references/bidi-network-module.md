# BiDi Network Module API Reference

> Complete reference for the WebDriver BiDi network module as implemented in bidiwave.

## Overview

The BiDi network module provides request interception, response mocking, authentication handling, and network data collection through the WebDriver BiDi protocol.

## Enabling the Network Module

```python
await session.network.enable()
```

Most network methods work without explicit enabling, but data collectors and event streaming require it.

## add_intercept

Add a network intercept at one or more phases.

```python
result = await session.network.add_intercept(
    phases=["beforeRequestSent", "responseStarted"],
    url_patterns=["*/api/*"],
    resource_types=["xhr", "fetch"]  # optional
)
# Returns: { "interceptId": "..." }
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `phases` | `array` | yes | Interception phases |
| `url_patterns` | `array` | yes | Glob-style URL patterns |
| `resource_types` | `array` | no | Filter by resource type |

### Phases

| Phase | Fires | Can modify |
|-------|-------|------------|
| `beforeRequestSent` | Before request is sent | URL, method, headers, body |
| `responseStarted` | When response headers arrive | Response status, headers |
| `authRequired` | When auth is needed | Auth credentials |

## remove_intercept

Remove a network intercept.

```python
await session.network.remove_intercept(
    intercept_id="intercept123"
)
```

## continue_request

Continue an intercepted request, optionally modifying it.

```python
await session.network.continue_request(
    request_id="request123",
    url="https://modified.example.com/api",  # optional
    method="POST",  # optional
    headers={"X-Custom": "value"},  # optional
    body="new body content",  # optional
    cookies=[{"name": "session", "value": "abc"}]  # optional
)
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `request_id` | `str` | yes | Intercepted request ID |
| `url` | `str` | no | Override request URL |
| `method` | `str` | no | Override HTTP method |
| `headers` | `dict` | no | Override request headers |
| `body` | `str` | no | Override request body |
| `cookies` | `array` | no | Override request cookies |

## continue_response

Continue an intercepted response, optionally modifying status and headers.

```python
await session.network.continue_response(
    request_id="request123",
    status_code=403,  # optional
    headers={"X-Blocked": "true"},  # optional
    body="Blocked"  # optional
)
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `request_id` | `str` | yes | Intercepted request ID |
| `status_code` | `int` | no | Override response status |
| `headers` | `dict` | no | Override response headers |
| `body` | `str` | no | Override response body |

## provide_response

Provide a complete mock response without contacting the server.

```python
await session.network.provide_response(
    request_id="request123",
    status_code=200,
    headers={"Content-Type": "application/json"},
    body='{"data": "mocked"}'
)
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `request_id` | `str` | yes | Intercepted request ID |
| `status_code` | `int` | yes | HTTP status code |
| `headers` | `dict` | no | Response headers |
| `body` | `str` | no | Response body |

## continue_with_auth

Provide authentication credentials for an `authRequired` intercept.

```python
await session.network.continue_with_auth(
    request_id="request123",
    credentials={
        "type": "password",
        "username": "user",
        "password": "pass"
    }
)
```

### Credential types

| Type | Fields | Description |
|------|--------|-------------|
| `password` | `username`, `password` | HTTP Basic/Digest auth |
| `proxy` | `username`, `password` | Proxy authentication |
| `cancel` | none | Cancel the auth request |

## get_response_body

Retrieve the body of a completed response.

```python
result = await session.network.get_response_body(
    network_id="network123"
)
# Returns: { "body": "...", "base64Encoded": bool }
```

## Data Collectors

### add_data_collector

Start collecting network data for matching requests.

```python
result = await session.network.add_data_collector(
    url_patterns=["*/api/*"],
    include_request_bodies=True,
    include_response_bodies=True,
    include_cookies=False,
    include_headers=True
)
# Returns: { "collectorId": "..." }
```

### get_collected_data

Retrieve data collected by a data collector.

```python
data = await session.network.get_collected_data(
    collector_id="collector123"
)
# Returns: { "networkEntries": [...] }
```

### remove_data_collector

Remove a data collector.

```python
await session.network.remove_data_collector(
    collector_id="collector123"
)
```

## Event Streaming

### stream_intercepted_requests

Async generator yielding intercepted request events.

```python
async for event in session.network.stream_intercepted_requests():
    print(event["request"]["url"])
    await session.network.continue_request(request_id=event["requestId"])
```

### stream_blocked_requests

Async generator yielding blocked request events.

```python
async for event in session.network.stream_blocked_requests():
    print(f"Blocked: {event['request']['url']}")
```

### stream_auth_required

Async generator yielding auth-required events.

```python
async for event in session.network.stream_auth_required():
    await session.network.continue_with_auth(
        request_id=event["requestId"],
        credentials={"type": "password", "username": "u", "password": "p"}
    )
```

### stream_response_completed

Async generator yielding completed response events.

```python
async for event in session.network.stream_response_completed():
    print(f"{event['response']['status']} — {event['request']['url']}")
```

## Event Objects

### InterceptedRequest event

| Field | Type | Description |
|-------|------|-------------|
| `requestId` | `str` | Unique request ID |
| `request` | `object` | Request data |
| `interceptId` | `str` | Matching intercept ID |
| `phase` | `str` | Interception phase |
| `resourceType` | `str` | Resource type |

### Request object

| Field | Type | Description |
|-------|------|-------------|
| `url` | `str` | Request URL |
| `method` | `str` | HTTP method |
| `headers` | `dict` | Request headers |
| `body` | `str` | Request body (if available) |
| `cookies` | `array` | Request cookies |
| `timings` | `object` | Request timings |

### Response object

| Field | Type | Description |
|-------|------|-------------|
| `status` | `int` | HTTP status code |
| `statusText` | `str` | HTTP status text |
| `headers` | `dict` | Response headers |
| `mimeType` | `str` | MIME type |
| `bodySize` | `int` | Body size in bytes |
| `content` | `object` | Content info |
| `fromCache` | `bool` | Whether from cache |
| `timings` | `object` | Response timings |

## Methods Reference

| Method | Description |
|--------|-------------|
| `enable` | Enable network module |
| `disable` | Disable network module |
| `add_intercept` | Add network intercept |
| `remove_intercept` | Remove network intercept |
| `continue_request` | Continue intercepted request |
| `continue_response` | Continue intercepted response |
| `provide_response` | Provide mock response |
| `continue_with_auth` | Provide auth credentials |
| `get_response_body` | Get response body |
| `add_data_collector` | Start data collector |
| `get_collected_data` | Get collected data |
| `remove_data_collector` | Remove data collector |
| `stream_intercepted_requests` | Stream intercepted events |
| `stream_blocked_requests` | Stream blocked events |
| `stream_auth_required` | Stream auth events |
| `stream_response_completed` | Stream response events |

## References

- [WebDriver BiDi — Network module](https://w3c.github.io/webdriver-bidi/#module-network)
- `references/intercept-patterns.md` — Common interception patterns

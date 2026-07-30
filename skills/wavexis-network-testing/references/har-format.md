# HAR File Format Reference

> Complete reference of the HAR (HTTP Archive) 1.2 format as captured by wavexis.

## Overview

HAR (HTTP Archive) is a JSON-based format for recording HTTP transactions. wavexis captures all network traffic during a page load and outputs a standard HAR 1.2 file.

## HAR Structure

```json
{
  "log": {
    "version": "1.2",
    "creator": {
      "name": "wavexis",
      "version": "1.0.0"
    },
    "pages": [...],
    "entries": [...]
  }
}
```

## Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `log.version` | `str` | HAR format version (`"1.2"`) |
| `log.creator` | `object` | Tool that generated the HAR |
| `log.creator.name` | `str` | Tool name (`"wavexis"`) |
| `log.creator.version` | `str` | Tool version |
| `log.pages` | `array` | Page-level timing information |
| `log.entries` | `array` | Individual HTTP requests/responses |

## Page Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique page identifier |
| `title` | `str` | Page title |
| `startedDateTime` | `str` | ISO 8601 start time |
| `pageTimings` | `object` | Page-level timings |

### pageTimings

| Field | Type | Description |
|-------|------|-------------|
| `onContentLoad` | `float` | DOMContentLoaded time (ms) |
| `onLoad` | `float` | Load event time (ms) |

## Entry Object

Each entry represents a single HTTP request/response pair.

| Field | Type | Description |
|-------|------|-------------|
| `startedDateTime` | `str` | ISO 8601 request start time |
| `time` | `float` | Total time in ms |
| `request` | `object` | HTTP request data |
| `response` | `object` | HTTP response data |
| `timings` | `object` | Detailed timing breakdown |
| `serverIPAddress` | `str` | Server IP address |
| `connection` | `str` | Connection ID |
| `pageref` | `str` | Reference to page object |

## Request Object

| Field | Type | Description |
|-------|------|-------------|
| `method` | `str` | HTTP method (GET, POST, etc.) |
| `url` | `str` | Full request URL |
| `httpVersion` | `str` | HTTP version (HTTP/1.1, HTTP/2) |
| `headers` | `array` | Request headers |
| `queryString` | `array` | Query parameters |
| `cookies` | `array` | Request cookies |
| `headersSize` | `int` | Headers size in bytes |
| `bodySize` | `int` | Body size in bytes |
| `postData` | `object` | POST body data (if present) |

### Header Object

```json
{
  "name": "Content-Type",
  "value": "application/json"
}
```

### QueryString Object

```json
{
  "name": "page",
  "value": "1"
}
```

### PostData Object

| Field | Type | Description |
|-------|------|-------------|
| `mimeType` | `str` | MIME type of POST body |
| `text` | `str` | POST body text |
| `params` | `array` | Form parameters (for form-encoded) |

## Response Object

| Field | Type | Description |
|-------|------|-------------|
| `status` | `int` | HTTP status code |
| `statusText` | `str` | HTTP status text |
| `httpVersion` | `str` | HTTP version |
| `headers` | `array` | Response headers |
| `cookies` | `array` | Response cookies |
| `content` | `object` | Response body content |
| `redirectURL` | `str` | Redirect URL (if 3xx) |
| `headersSize` | `int` | Headers size in bytes |
| `bodySize` | `int` | Body size in bytes |

### Content Object

| Field | Type | Description |
|-------|------|-------------|
| `size` | `int` | Content size in bytes |
| `mimeType` | `str` | MIME type |
| `text` | `str` | Response body text (if `--include-bodies`) |
| `encoding` | `str` | Encoding if body is base64 (`"base64"`) |
| `compression` | `int` | Compression in bytes (decoded - encoded) |

## Timings Object

| Field | Type | Description |
|-------|------|-------------|
| `blocked` | `float` | Time spent blocked (ms) |
| `dns` | `float` | DNS resolution time (ms) |
| `connect` | `float` | TCP connection time (ms) |
| `ssl` | `float` | SSL/TLS handshake time (ms) |
| `send` | `float` | Time sending request (ms) |
| `wait` | `float` | Time waiting for response (TTFB) (ms) |
| `receive` | `float` | Time receiving response (ms) |

## Resource Types

wavexis categorizes requests by resource type:

| Type | Description |
|------|-------------|
| `document` | HTML documents |
| `script` | JavaScript files |
| `stylesheet` | CSS files |
| `image` | Image files |
| `xhr` | XMLHttpRequest |
| `fetch` | Fetch API requests |
| `font` | Font files |
| `websocket` | WebSocket connections |
| `manifest` | Manifest files |
| `other` | Other resources |

## Analyzing HAR Files

### With jq

```bash
# List all API calls
cat traffic.har | jq '.log.entries[] | select(.request.url | test("/api/")) | {url: .request.url, status: .response.status, time: .time}'

# Find slow requests
cat traffic.har | jq '.log.entries[] | {url: .request.url, time: .time} | select(.time > 1000)'

# Total transfer size
cat traffic.har | jq '[.log.entries[].response.bodySize] | add'

# Requests by status code
cat traffic.har | jq '.log.entries | group_by(.response.status) | map({status: .[0].response.status, count: length})'
```

### With Python

```python
import json

with open("traffic.har") as f:
    har = json.load(f)

entries = har["log"]["entries"]

# Total requests
print(f"Total requests: {len(entries)}")

# API calls only
api_calls = [e for e in entries if "/api/" in e["request"]["url"]]
print(f"API calls: {len(api_calls)}")

# Slow requests (> 1s)
slow = [e for e in entries if e["time"] > 1000]
for e in slow:
    print(f"  {e['time']:.0f}ms - {e['request']['url']}")

# Total size
total_size = sum(e["response"]["bodySize"] for e in entries)
print(f"Total size: {total_size / 1024:.1f} KB")
```

## References

- [HAR 1.2 Specification](http://www.softwareishard.com/blog/har-12-spec/)
- [HAR Viewer](http://www.softwareishard.com/blog/har-viewer/)
- [Chrome DevTools HAR export](https://developer.chrome.com/docs/devtools/network/reference/#export)

---
name: WaveXis Network Testing
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Network testing with wavexis. HAR capture, request interception, response mocking, network throttling, WebSocket inspection, request modification."
tags: [network, har, interception, mocking, throttling]
trigger: When the user asks about network testing with wavexis, needs HAR capture, wants request interception or response mocking, needs network throttling, wants WebSocket inspection, or needs to replay captured HAR files.
---

# WaveXis Network Testing

## Description

Network testing with wavexis — capture HAR files, intercept and mock requests/responses, modify in-flight traffic, simulate network conditions, inspect WebSocket frames, and replay captured HAR files.

## When to Invoke

- Capturing HAR files for network analysis
- Intercepting or mocking API requests
- Modifying request headers or response bodies in-flight
- Simulating slow or unreliable network conditions
- Inspecting WebSocket traffic
- Replaying captured HAR files for testing

## Prerequisites

- `pip install wavexis[cdp]`
- Chrome or Edge installed
- Basic familiarity with wavexis CLI (see `wavexis-cli-automation` skill)

## HAR Capture

### har command

Capture all network traffic during page load as a HAR (HTTP Archive) file:

```bash
wavexis har https://example.com --output traffic.har
```

### HAR with interaction

```bash
wavexis har https://example.com \
    --click "#load-more" \
    --wait-for ".results" \
    --output traffic.har
```

### HAR with filter

```bash
# Only capture API requests
wavexis har https://example.com \
    --url-filter "*/api/*" \
    --output api-traffic.har
```

### HAR options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--output` | `str` | stdout | Output HAR file path |
| `--url-filter` | `str` | None | Only capture matching URLs (regex) |
| `--method-filter` | `str` | None | Only capture matching methods (GET, POST, etc.) |
| `--resource-type` | `str` | None | Filter by type: `xhr`, `fetch`, `script`, `stylesheet`, `image`, `document` |
| `--include-bodies` | `flag` | off | Include request/response bodies in HAR |
| `--click` | `str` | None | Click selector after navigation |
| `--input` | `str` | None | Type into selector after navigation |
| `--wait-for` | `str` | None | Wait for selector before stopping capture |
| `--timeout` | `int` | `30000` | Capture timeout in ms |

### HAR output format

The output is a standard HAR 1.2 file:

```json
{
  "log": {
    "version": "1.2",
    "creator": {
      "name": "wavexis",
      "version": "1.0.0"
    },
    "entries": [
      {
        "request": {
          "method": "GET",
          "url": "https://example.com/api/data",
          "headers": [...],
          "queryString": [...],
          "bodySize": 0
        },
        "response": {
          "status": 200,
          "statusText": "OK",
          "headers": [...],
          "content": {
            "size": 1024,
            "mimeType": "application/json"
          },
          "bodySize": 1024
        },
        "timings": {
          "blocked": 0,
          "dns": 5,
          "connect": 20,
          "send": 1,
          "wait": 45,
          "receive": 10
        },
        "time": 81
      }
    ]
  }
}
```

## Request Interception

### intercept command

Block or allow requests matching a pattern:

```bash
wavexis intercept https://example.com \
    --block "*/ads/*" \
    --block "*/tracker.js" \
    --output result.json
```

### intercept with allow

```bash
wavexis intercept https://example.com \
    --block "*/ads/*" \
    --allow "*/api/*" \
    --output result.json
```

### intercept options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--block` | `str` | None | URL pattern to block (can repeat) |
| `--allow` | `str` | None | URL pattern to allow (overrides block) |
| `--resource-type` | `str` | None | Block by resource type |
| `--output` | `str` | stdout | Output file path |
| `--wait-for` | `str` | None | Wait for selector before stopping |
| `--timeout` | `int` | `30000` | Timeout in ms |

### intercept output

```json
{
  "blocked": [
    "https://ads.example.com/banner.js",
    "https://tracker.example.com/analytics.js"
  ],
  "allowed": [
    "https://api.example.com/data"
  ],
  "total_blocked": 2,
  "total_allowed": 1
}
```

## Response Mocking

### mock command

Mock API responses with custom status, headers, and body:

```bash
wavexis mock https://example.com \
    --url "*/api/users" \
    --status 200 \
    --body '{"users": []}' \
    --content-type "application/json" \
    --output result.json
```

### mock with file

```bash
wavexis mock https://example.com \
    --url "*/api/products" \
    --status 200 \
    --body-file ./mocks/products.json \
    --content-type "application/json" \
    --output result.json
```

### mock with delay

```bash
wavexis mock https://example.com \
    --url "*/api/slow" \
    --status 200 \
    --body '{"data": "delayed"}' \
    --delay 3000 \
    --output result.json
```

### mock multiple endpoints

```bash
wavexis mock https://example.com \
    --mock '*/api/users:200:{"users": []}' \
    --mock '*/api/products:200:{"products": []}' \
    --mock '*/api/error:500:{"error": "Internal"}' \
    --output result.json
```

### mock options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--url` | `str` | None | URL pattern to mock |
| `--status` | `int` | `200` | HTTP status code |
| `--body` | `str` | None | Response body string |
| `--body-file` | `str` | None | Response body from file |
| `--content-type` | `str` | `application/json` | Content-Type header |
| `--header` | `str` | None | Additional response header (can repeat) |
| `--delay` | `int` | `0` | Response delay in ms |
| `--mock` | `str` | None | Shorthand: `url:status:body` (can repeat) |
| `--output` | `str` | stdout | Output file path |
| `--timeout` | `int` | `30000` | Timeout in ms |

## In-Flight Modification

### modify command

Modify request headers or URLs before they reach the server:

```bash
wavexis modify https://example.com \
    --set-header "Authorization: Bearer token123" \
    --set-header "X-Custom: value" \
    --output result.json
```

### modify URL

```bash
wavexis modify https://example.com \
    --rewrite-url "*/staging/*->*/production/*" \
    --output result.json
```

### modify-response command

Modify response headers or body before the browser receives them:

```bash
wavexis modify-response https://example.com \
    --url "*/api/config" \
    --set-header "X-Modified: true" \
    --output result.json
```

### modify options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--set-header` | `str` | None | Set request header (can repeat) |
| `--remove-header` | `str` | None | Remove request header (can repeat) |
| `--rewrite-url` | `str` | None | Rewrite URL pattern: `from->to` |
| `--url` | `str` | None | URL pattern to match for modifications |
| `--output` | `str` | stdout | Output file path |
| `--timeout` | `int` | `30000` | Timeout in ms |

## Network Throttling

### throttle command

Simulate slow or unreliable network conditions:

```bash
wavexis throttle https://example.com \
    --profile slow-3g \
    --output result.json
```

### throttle with CWV

```bash
wavexis throttle https://example.com \
    --profile slow-3g \
    --cwv \
    --output cwv-throttled.json
```

### throttle profiles

| Profile | Download | Upload | Latency | Description |
|---------|----------|--------|---------|-------------|
| `no-throttling` | — | — | — | No throttling |
| `fast-4g` | 4 Mbps | 3 Mbps | 20 ms | Fast 4G |
| `slow-4g` | 1.5 Mbps | 750 kbps | 40 ms | Slow 4G |
| `fast-3g` | 780 kbps | 330 kbps | 150 ms | Fast 3G |
| `slow-3g` | 400 kbps | 400 kbps | 400 ms | Slow 3G |
| `offline` | 0 | 0 | — | Offline |

### custom throttle

```bash
wavexis throttle https://example.com \
    --download 500000 \
    --upload 250000 \
    --latency 300 \
    --output result.json
```

### throttle options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--profile` | `str` | `slow-3g` | Throttle profile name |
| `--download` | `int` | None | Custom download speed in bytes/s |
| `--upload` | `int` | None | Custom upload speed in bytes/s |
| `--latency` | `int` | None | Custom latency in ms |
| `--cwv` | `flag` | off | Measure CWV under throttling |
| `--output` | `str` | stdout | Output file path |
| `--timeout` | `int` | `60000` | Timeout in ms (longer for slow profiles) |

## Network Inspection

### inspect command

Inspect all network requests during page load:

```bash
wavexis inspect https://example.com --output network.json
```

### inspect with filter

```bash
wavexis inspect https://example.com \
    --url-filter "*/api/*" \
    --method "POST" \
    --output api-calls.json
```

### inspect output

```json
{
  "requests": [
    {
      "url": "https://api.example.com/data",
      "method": "GET",
      "resource_type": "fetch",
      "status": 200,
      "status_text": "OK",
      "mime_type": "application/json",
      "encoded_size": 512,
      "decoded_size": 1024,
      "time": 45,
      "protocol": "h2",
      "from_cache": false,
      "from_service_worker": false
    }
  ],
  "total_requests": 1,
  "total_size": 1024,
  "total_time": 45
}
```

### inspect options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--url-filter` | `str` | None | URL pattern filter (regex) |
| `--method` | `str` | None | HTTP method filter |
| `--resource-type` | `str` | None | Resource type filter |
| `--status` | `int` | None | Status code filter |
| `--include-bodies` | `flag` | off | Include request/response bodies |
| `--output` | `str` | stdout | Output file path |
| `--wait-for` | `str` | None | Wait for selector before stopping |
| `--timeout` | `int` | `30000` | Timeout in ms |

## HAR Replay

### har-replay command

Replay a captured HAR file against a target URL:

```bash
wavexis har-replay ./traffic.har --target https://staging.example.com
```

### har-replay with verification

```bash
wavexis har-replay ./traffic.har \
    --target https://staging.example.com \
    --verify \
    --output replay-results.json
```

### har-replay options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--target` | `str` | required | Target URL to replay against |
| `--verify` | `flag` | off | Compare responses with original HAR |
| `--delay` | `int` | `0` | Delay between requests in ms |
| `--url-filter` | `str` | None | Only replay matching URLs |
| `--output` | `str` | stdout | Output file path |
| `--timeout` | `int` | `60000` | Timeout in ms |

## WebSocket Inspection

### WebSocket frame capture

```bash
wavexis inspect https://example.com \
    --websocket \
    --output ws-traffic.json
```

### WebSocket output

```json
{
  "websockets": [
    {
      "url": "wss://example.com/ws",
      "frames": [
        {
          "direction": "send",
          "data": "{\"type\": \"subscribe\", \"channel\": \"updates\"}",
          "timestamp": 1234567890
        },
        {
          "direction": "receive",
          "data": "{\"type\": \"update\", \"data\": {...}}",
          "timestamp": 1234567891
        }
      ]
    }
  ]
}
```

## Multi-Action YAML

### HAR capture with interaction

```yaml
actions:
  - navigate:
      url: https://example.com
      wait_until: networkidle
  - har:
      url_filter: "*/api/*"
      include_bodies: true
      output: api-traffic.har
  - click:
      selector: "#load-data"
  - wait_for:
      selector: ".results"
  - har_stop:
      output: full-traffic.har
```

### Mock and test

```yaml
actions:
  - mock:
          url: "*/api/users"
          status: 200
          body: '{"users": [{"id": 1, "name": "Test User"}]}'
          content_type: application/json
  - navigate:
      url: https://example.com
      wait_until: networkidle
  - assert:
      text: "contains Test User"
  - screenshot:
      full_page: true
```

### Throttle and measure

```yaml
actions:
  - throttle:
      profile: slow-3g
  - navigate:
      url: https://example.com
      wait_until: load
  - cwv:
      mobile: true
      output: cwv-throttled.json
  - screenshot:
      full_page: true
```

## Best Practices

- **Use `--include-bodies` sparingly** — bodies can make HAR files very large.
- **Filter by URL** — use `--url-filter` to focus on relevant traffic.
- **Mock external APIs in tests** — don't depend on third-party services in CI.
- **Throttle with CWV** — always measure CWV under `slow-3g` for real-world performance.
- **Block trackers in tests** — use `intercept --block` to remove noise from analytics.
- **Verify HAR replays** — use `--verify` to detect API response changes.
- **Save HAR files as artifacts** — useful for debugging network issues in CI.
- **Use custom throttle for specific scenarios** — simulate your users' actual network conditions.
- **Inspect WebSocket frames** — debug real-time communication issues.
- **Mock with realistic delays** — use `--delay` to simulate real API latency.

## Common Pitfalls

- **HAR files too large** — use `--url-filter` and avoid `--include-bodies` for large sites.
- **Mock not matching** — URL patterns are regex; escape special characters.
- **Throttle profile too slow** — `slow-3g` can cause timeouts; increase `--timeout`.
- **Intercept blocking too much** — use `--allow` to whitelist critical resources.
- **HAR replay URL mismatch** — the target URL must serve the same paths as the original capture.
- **WebSocket frames missing** — use `--websocket` flag explicitly; not captured by default.
- **Modify headers not applied** — modifications only apply to requests made after navigation starts.
- **Mock delay causing timeout** — keep mock delays shorter than `--timeout`.

## References

- `references/har-format.md` — HAR file format reference
- `references/network-patterns.md` — Common network testing patterns
- `assets/templates/har-capture.yml` — HAR capture template
- `assets/templates/mock-api.yml` — API mocking template
- `assets/templates/throttle-test.yml` — Network throttling template
- [HAR 1.2 Specification](http://www.softwareishard.com/blog/har-12-spec/)
- [Chrome DevTools Network](https://developer.chrome.com/docs/devtools/network/)

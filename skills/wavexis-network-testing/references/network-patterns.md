# Common Network Testing Patterns

> Recipes for common network testing scenarios with wavexis.

## Pattern 1: API Dependency Audit

Capture all API calls a page makes to understand its dependencies.

```bash
wavexis har https://example.com \
    --url-filter "*/api/*" \
    --include-bodies \
    --output api-deps.har
```

### What to look for

- Number of API calls on page load
- Sequential vs parallel requests
- Duplicate or redundant calls
- Large response payloads
- Unauthenticated API calls

## Pattern 2: Block Third-Party Trackers

Remove analytics and ad tracking from test runs for cleaner results.

```bash
wavexis intercept https://example.com \
    --block "*/google-analytics.com/*" \
    --block "*/googletagmanager.com/*" \
    --block "*/facebook.net/*" \
    --block "*/doubleclick.net/*" \
    --output blocked.json
```

### Common patterns to block

```
*/google-analytics.com/*
*/googletagmanager.com/*
*/facebook.net/*
*/doubleclick.net/*
*/adservice.google.com/*
*/amazon-adsystem.com/*
*/criteo.com/*
*/hotjar.com/*
*/segment.com/*
*/mixpanel.com/*
```

## Pattern 3: Mock API for Testing

Replace real API calls with mock data for deterministic tests.

```bash
wavexis mock https://example.com \
    --mock '*/api/users:200:{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}' \
    --mock '*/api/products:200:{"products": [{"id": 1, "name": "Widget", "price": 9.99}]}' \
    --mock '*/api/error:500:{"error": "Internal Server Error"}' \
    --output mock-results.json
```

### Mock with realistic delay

```bash
wavexis mock https://example.com \
    --url "*/api/slow-endpoint" \
    --status 200 \
    --body '{"data": "result"}' \
    --delay 2000 \
    --output result.json
```

## Pattern 4: Test Error Handling

Mock error responses to test how the page handles API failures.

```bash
# Test 500 error handling
wavexis mock https://example.com \
    --url "*/api/data" \
    --status 500 \
    --body '{"error": "Internal Server Error"}' \
    --output error-test.json

# Test timeout handling
wavexis mock https://example.com \
    --url "*/api/data" \
    --status 200 \
    --body '{"data": "late"}' \
    --delay 30000 \
    --output timeout-test.json

# Test 404 handling
wavexis mock https://example.com \
    --url "*/api/missing" \
    --status 404 \
    --body '{"error": "Not Found"}' \
    --output notfound-test.json
```

## Pattern 5: Network Throttling for Performance

Measure how a page performs under different network conditions.

```bash
# Test under Slow 3G
wavexis throttle https://example.com \
    --profile slow-3g \
    --cwv \
    --output slow-3g-cwv.json

# Test under Fast 4G
wavexis throttle https://example.com \
    --profile fast-4g \
    --cwv \
    --output fast-4g-cwv.json

# Compare with no throttling
wavexis cwv https://example.com \
    --output no-throttle-cwv.json
```

## Pattern 6: HAR Replay for Regression Testing

Capture traffic from production and replay against staging.

```bash
# Capture production traffic
wavexis har https://production.example.com \
    --include-bodies \
    --output production.har

# Replay against staging
wavexis har-replay ./production.har \
    --target https://staging.example.com \
    --verify \
    --output replay-results.json
```

### What to check in replay results

- Status code changes (e.g., 200 → 500)
- Response body differences
- New or missing endpoints
- Timing differences

## Pattern 7: WebSocket Debugging

Inspect WebSocket traffic for real-time communication issues.

```bash
wavexis inspect https://example.com \
    --websocket \
    --output ws-traffic.json
```

### Common WebSocket issues

| Issue | Symptom | How to detect |
|-------|---------|---------------|
| Connection failure | No frames captured | Check `websockets` array is empty |
| Message format error | Unexpected JSON | Compare `data` field with expected schema |
| Slow messages | Large timestamps | Check `timestamp` gaps between frames |
| Disconnection | Few frames then stop | Check frame count and last timestamp |
| Wrong channel | Unexpected `type` | Inspect `data` field for `type`/`channel` |

## Pattern 8: Request Header Modification

Add authentication or custom headers for testing.

```bash
wavexis modify https://example.com \
    --set-header "Authorization: Bearer $TEST_TOKEN" \
    --set-header "X-Test-Environment: true" \
    --set-header "X-Request-ID: test-12345" \
    --output result.json
```

## Pattern 9: Response Modification Testing

Modify API responses to test UI behavior with different data.

```bash
wavexis modify-response https://example.com \
    --url "*/api/config" \
    --set-header "X-Modified: true" \
    --output result.json
```

## Pattern 10: Full Network Audit

Comprehensive network analysis combining multiple commands.

```bash
# Step 1: Capture all traffic
wavexis har https://example.com \
    --include-bodies \
    --output full-audit.har

# Step 2: Inspect requests
wavexis inspect https://example.com \
    --output inspection.json

# Step 3: Measure under throttling
wavexis throttle https://example.com \
    --profile slow-3g \
    --cwv \
    --output throttled-cwv.json

# Step 4: Block trackers and re-measure
wavexis intercept https://example.com \
    --block "*/analytics/*" \
    --block "*/ads/*" \
    --output blocked.json
```

## CI Integration

### Network regression test

```bash
# Capture baseline
wavexis har https://staging.example.com \
    --url-filter "*/api/*" \
    --output baseline.har

# Replay in CI
wavexis har-replay ./baseline.har \
    --target https://staging.example.com \
    --verify \
    --assert 'status_code == 200' \
    --output replay.json
```

### Performance under throttling gate

```bash
wavexis throttle https://staging.example.com \
    --profile slow-3g \
    --cwv \
    --assert 'lcp_ms <= 4000' \
    --assert 'cls <= 0.1' \
    --output throttled-cwv.json
```

## References

- `references/har-format.md` — HAR file format reference
- [wavexis CLI documentation](https://github.com/MathiasPaulenko/wavexis)

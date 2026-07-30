# CI Assertions — Patterns and Exit Codes

> Complete reference of wavexis assertion patterns, operators, and CI exit codes.

## Assertion Syntax

Assertions are passed via the `--assert` flag. Multiple `--assert` flags can be used in a single command — all must pass for exit code 0.

```bash
wavexis navigate https://example.com \
    --assert 'title == "Example Domain"' \
    --assert 'text contains "More information"' \
    --output result.json
```

## Assertion Operators

### Equality operators

| Operator | Description | Example | Use case |
|----------|-------------|---------|----------|
| `==` | Exact equality | `title == "Welcome"` | Verify exact title or text |
| `!=` | Inequality | `url != "https://error.example.com"` | Verify not on error page |

### Containment operators

| Operator | Description | Example | Use case |
|----------|-------------|---------|----------|
| `contains` | Substring match | `text contains "Sign In"` | Verify content present |
| `!contains` | Substring absence | `text !contains "Error"` | Verify error absent |

### Regex operators

| Operator | Description | Example | Use case |
|----------|-------------|---------|----------|
| `matches` | Regex match | `url matches "https://.*\.example\.com"` | Pattern validation |
| `!matches` | Regex non-match | `title !matches ".*Error.*"` | Error pattern absence |

### Comparison operators

| Operator | Description | Example | Use case |
|----------|-------------|---------|----------|
| `>` | Greater than | `lcp_ms > 0` | Metric is positive |
| `>=` | Greater or equal | `lcp_ms >= 2500` | Metric meets threshold |
| `<` | Less than | `cls < 0.1` | Metric below threshold |
| `<=` | Less or equal | `inp_ms <= 200` | Metric at or below threshold |

## Assertable Fields

### Navigation fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | `str` | Page title (`<title>` tag) |
| `url` | `str` | Current URL after navigation |
| `text` | `str` | Visible text content of the page |
| `status_code` | `int` | HTTP status code of the response |
| `html` | `str` | Raw HTML of the page |

### CWV fields

| Field | Type | Description |
|-------|------|-------------|
| `lcp_ms` | `int` | Largest Contentful Paint in milliseconds |
| `cls` | `float` | Cumulative Layout Shift score |
| `inp_ms` | `int` | Interaction to Next Paint in milliseconds |
| `fcp_ms` | `int` | First Contentful Paint in milliseconds |
| `tbt_ms` | `int` | Total Blocking Time in milliseconds |
| `tti_ms` | `int` | Time to Interactive in milliseconds |
| `speed_index_ms` | `int` | Speed Index in milliseconds |
| `ttfb_ms` | `int` | Time to First Byte in milliseconds |

### Visual diff fields

| Field | Type | Description |
|-------|------|-------------|
| `diff_percentage` | `float` | Percentage of changed pixels (0-1) |
| `pixels_changed` | `int` | Number of changed pixels |
| `total_pixels` | `int` | Total pixels compared |

### Lighthouse fields

| Field | Type | Description |
|-------|------|-------------|
| `performance_score` | `int` | Lighthouse performance score (0-100) |
| `accessibility_score` | `int` | Lighthouse accessibility score (0-100) |
| `best_practices_score` | `int` | Lighthouse best practices score (0-100) |
| `seo_score` | `int` | Lighthouse SEO score (0-100) |

## Output Format

Each assertion produces a JSON object in the output:

### Pass example

```json
{
  "assert": "title == \"Example Domain\"",
  "result": "Example Domain",
  "status": "PASS"
}
```

### Fail example

```json
{
  "assert": "title == \"Welcome\"",
  "result": "Example Domain",
  "status": "FAIL"
}
```

### Multiple assertions output

```json
{
  "assertions": [
    {
      "assert": "title == \"Example Domain\"",
      "result": "Example Domain",
      "status": "PASS"
    },
    {
      "assert": "text contains \"More information\"",
      "result": "Example Domain\nMore information...",
      "status": "PASS"
    },
    {
      "assert": "url matches \"https://example\\.com\"",
      "result": "https://example.com/",
      "status": "PASS"
    }
  ],
  "summary": {
    "total": 3,
    "passed": 3,
    "failed": 0,
    "status": "PASS"
  }
}
```

## Exit Codes

| Code | Meaning | CI behavior | When it occurs |
|------|---------|-------------|----------------|
| 0 | All assertions passed | Pipeline continues | Every `--assert` returned PASS |
| 1 | One or more assertions failed | Pipeline stops | At least one `--assert` returned FAIL |
| 2 | Runtime error | Pipeline stops | Navigation timeout, browser crash, invalid URL |

### Handling exit codes in CI

```bash
# Bash: stop on any non-zero exit
set -e
wavexis navigate https://example.com --assert 'title == "Welcome"'

# Bash: handle differently
wavexis navigate https://example.com --assert 'title == "Welcome"' --output result.json
exit_code=$?
if [ $exit_code -eq 1 ]; then
    echo "Assertion failed — see result.json"
    exit 1
elif [ $exit_code -eq 2 ]; then
    echo "Runtime error — check browser and URL"
    exit 2
fi
```

```python
# Python: subprocess
import subprocess
result = subprocess.run(
    ["wavexis", "navigate", "https://example.com", "--assert", 'title == "Welcome"'],
    capture_output=True
)
if result.returncode == 0:
    print("Passed")
elif result.returncode == 1:
    print(f"Assertion failed: {result.stdout}")
else:
    print(f"Error: {result.stderr}")
```

## CI Assertion Recipes

### Smoke test after deploy

```bash
wavexis batch ./urls/production.txt \
    --assert 'status_code == 200' \
    --assert 'title !matches ".*Error.*"' \
    --output-dir ./smoke-results/
```

### Login flow assertion

```bash
wavexis navigate https://staging.example.com/login \
    --input "#username" "$CI_USERNAME" \
    --input "#password" "$CI_PASSWORD" \
    --click "#submit" \
    --assert 'url matches "https://staging\.example\.com/dashboard"' \
    --assert 'text !contains "Invalid credentials"' \
    --output login-result.json
```

### CWV deploy gate

```bash
wavexis cwv https://staging.example.com \
    --mobile --throttle \
    --assert 'lcp_ms <= 2500' \
    --assert 'cls <= 0.1' \
    --assert 'inp_ms <= 200' \
    --output cwv-gate.json
```

### Visual regression gate

```bash
wavexis visual-diff https://staging.example.com \
    --baseline ./baselines/homepage.png \
    --threshold 0.1 \
    --assert 'diff_percentage <= 0.1' \
    --output ./diffs/homepage-diff.png
```

### Accessibility gate

```bash
wavexis axe https://staging.example.com \
    --tags wcag2a,wcag2aa \
    --impact-threshold serious \
    --assert \
    --output axe-results.json
```

## References

- [wavexis CLI documentation](https://github.com/MathiasPaulenko/wavexis)
- `references/visual-diff.md` — Visual regression setup and baselines

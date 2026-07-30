---
name: WaveXis CI/CD Integration
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Integrate wavexis into CI/CD pipelines. CI assertions, visual regression, screenshots in PRs, deploy gates with CWV budgets, Docker serve mode."
tags: [ci-cd, assertions, visual-diff, github-actions]
trigger: When the user asks about integrating wavexis into CI/CD, needs CI assertions, wants visual regression testing, needs deploy gates with CWV budgets, or wants Docker serve mode for shared browser instances.
---

# WaveXis CI/CD Integration

## Description

Integrate wavexis into CI/CD pipelines — assertion patterns for automated gates, visual regression testing with baselines, batch processing for multiple URLs, Docker serve mode for shared browser instances, and GitHub Actions integration.

## When to Invoke

- Setting up CI/CD pipelines with wavexis
- Writing CI assertions for automated gates
- Configuring visual regression testing
- Processing multiple URLs in batch mode
- Running wavexis in Docker serve mode
- Creating deploy gates with CWV/performance budgets
- Integrating wavexis with GitHub Actions, GitLab CI, or Jenkins

## Prerequisites

- `pip install wavexis[cdp]`
- Chrome or Edge installed (or Docker with Chrome image)
- Basic familiarity with wavexis CLI (see `wavexis-cli-automation` skill)

## CI Assertion Patterns

### Overview

The `--assert` flag enables CI gate behavior: wavexis exits with code 0 on pass and 1 on fail. Assertions use comparison operators to validate page state, content, metrics, or responses.

### Assertion operators

| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Exact equality | `title == "Welcome"` |
| `!=` | Inequality | `url != "https://error.example.com"` |
| `contains` | Substring match | `text contains "Sign In"` |
| `!contains` | Substring absence | `text !contains "Error"` |
| `matches` | Regex match | `url matches "https://.*\.example\.com"` |
| `!matches` | Regex non-match | `title !matches ".*Error.*"` |
| `>` | Greater than | `lcp_ms > 0` |
| `>=` | Greater or equal | `lcp_ms >= 2500` |
| `<` | Less than | `cls < 0.1` |
| `<=` | Less or equal | `inp_ms <= 200` |

### Assertion examples

#### Title assertion

```bash
wavexis navigate https://example.com \
    --assert 'title == "Example Domain"' \
    --output result.json
```

#### URL assertion after redirect

```bash
wavexis navigate https://example.com/login \
    --input "#username" "admin" \
    --input "#password" "secret" \
    --click "#submit" \
    --assert 'url matches "https://example\.com/dashboard"' \
    --output result.json
```

#### Content assertion

```bash
wavexis navigate https://example.com \
    --assert 'text contains "Welcome"' \
    --assert 'text !contains "Error"' \
    --output result.json
```

#### CWV budget assertion

```bash
wavexis cwv https://example.com \
    --mobile \
    --throttle \
    --assert 'lcp_ms <= 2500' \
    --assert 'cls <= 0.1' \
    --assert 'inp_ms <= 200' \
    --output cwv-results.json
```

#### Multiple assertions

```bash
wavexis navigate https://example.com \
    --assert 'title == "Example Domain"' \
    --assert 'url matches "https://example\.com"' \
    --assert 'text contains "More information"' \
    --output result.json
```

All assertions must pass for exit code 0.

### Output format

```json
{
  "assert": "title == \"Example Domain\"",
  "result": "Example Domain",
  "status": "PASS"
}
```

```json
{
  "assert": "title == \"Welcome\"",
  "result": "Example Domain",
  "status": "FAIL"
}
```

### Exit codes

| Code | Meaning | CI behavior |
|------|---------|-------------|
| 0 | All assertions passed | Pipeline continues |
| 1 | One or more assertions failed | Pipeline stops |
| 2 | Error (navigation timeout, crash) | Pipeline stops |

## Batch Processing

### Batch command

Process multiple URLs in a single run:

```bash
wavexis batch urls.txt --format markdown --output-dir ./results/
```

### Batch with assertions

```bash
wavexis batch urls.txt \
    --assert 'status_code == 200' \
    --assert 'title !matches ".*Error.*"' \
    --output-dir ./results/
```

### Batch with screenshots

```bash
wavexis batch urls.txt \
    --screenshot \
    --full-page \
    --output-dir ./screenshots/
```

### Batch with CWV

```bash
wavexis batch urls.txt \
    --cwv \
    --mobile \
    --throttle \
    --assert 'lcp_ms <= 2500' \
    --output-dir ./cwv-results/
```

### Batch options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--format` | `str` | `markdown` | Output format: `markdown`, `json`, `html` |
| `--output-dir` | `str` | `./output/` | Output directory |
| `--screenshot` | `flag` | off | Take screenshots |
| `--full-page` | `flag` | off | Full page screenshots |
| `--cwv` | `flag` | off | Measure Core Web Vitals |
| `--assert` | `str` | None | Assertion expression |
| `--delay` | `int` | `0` | Delay between URLs in seconds |
| `--concurrent` | `int` | `1` | Concurrent URL processing |
| `--stealth` | `flag` | off | Enable stealth mode |
| `--timeout` | `int` | `30000` | Per-URL timeout in ms |

### Batch URL file format

```
# One URL per line
# Lines starting with # are comments
# Blank lines are ignored

https://example.com/page-1
https://example.com/page-2
https://example.com/page-3
```

## Visual Regression Testing

### visual-diff command

Compare a page screenshot against a baseline image:

```bash
wavexis visual-diff https://example.com \
    --baseline ./baselines/homepage.png \
    --output ./diffs/homepage-diff.png \
    --threshold 0.1
```

### Generating baselines

```bash
wavexis screenshot https://example.com \
    --full-page \
    --output ./baselines/homepage.png
```

### Visual diff with assertion

```bash
wavexis visual-diff https://example.com \
    --baseline ./baselines/homepage.png \
    --threshold 0.1 \
    --assert 'diff_percentage <= 0.1' \
    --output ./diffs/homepage-diff.png
```

### Visual diff options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--baseline` | `str` | required | Path to baseline image |
| `--output` | `str` | stdout | Diff output path |
| `--threshold` | `float` | `0.1` | Pixel difference threshold (0-1) |
| `--full-page` | `flag` | off | Full page comparison |
| `--viewport` | `str` | `1920x1080` | Viewport size |
| `--assert` | `str` | None | Assertion expression |
| `--wait-for` | `str` | None | Wait for selector before screenshot |

### Visual diff output

```json
{
  "diff_percentage": 0.03,
  "pixels_changed": 1245,
  "total_pixels": 41472,
  "status": "PASS"
}
```

### Baseline management

- **Store baselines in git** — commit baseline images to the repo.
- **Update baselines intentionally** — re-generate after approved UI changes.
- **Use per-viewport baselines** — separate baselines for mobile and desktop.
- **Name baselines by page** — `baselines/homepage-desktop.png`, `baselines/homepage-mobile.png`.

## Docker Serve Mode

### Overview

Run wavexis in serve mode inside Docker to share a browser instance across CI jobs or team members.

### Docker Compose

```yaml
version: "3.8"
services:
  wavexis:
    image: ghcr.io/mathiaspaulenko/wavexis:latest
    ports:
      - "9222:9222"
    environment:
      - WAVEXIS_PORT=9222
      - WAVEXIS_RATE_LIMIT=10
      - WAVEXIS_MAX_SESSIONS=5
    volumes:
      - ./output:/app/output
    restart: unless-stopped
```

### Using serve mode

```bash
# Point wavexis at the serve instance
wavexis --serve http://localhost:9222 navigate https://example.com

# Run assertions against serve instance
wavexis --serve http://localhost:9222 cwv https://example.com \
    --mobile --throttle --assert 'lcp_ms <= 2500'
```

### Serve mode benefits

- **Shared browser pool** — reuse browser instances across jobs.
- **Faster CI** — no browser launch overhead per job.
- **Resource control** — limit concurrent sessions and rate limiting.
- **Team access** — shared instance for local development and CI.

## GitHub Actions Integration

### Basic workflow

```yaml
name: Wavexis Tests

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  wavexis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install wavexis
        run: pip install wavexis[cdp]

      - name: Install Chrome
        run: |
          wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
          sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
          sudo apt-get update && sudo apt-get install -y google-chrome-stable

      - name: Run assertions
        run: |
          wavexis navigate https://staging.example.com \
            --assert 'title == "Welcome"' \
            --assert 'text contains "Sign In"' \
            --output result.json

      - name: Run CWV gate
        run: |
          wavexis cwv https://staging.example.com \
            --mobile --throttle \
            --assert 'lcp_ms <= 2500' \
            --assert 'cls <= 0.1' \
            --assert 'inp_ms <= 200' \
            --output cwv.json

      - name: Run accessibility gate
        run: |
          wavexis axe https://staging.example.com \
            --tags wcag2a,wcag2aa \
            --impact-threshold serious \
            --assert \
            --output axe.json

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: wavexis-results
          path: |
            result.json
            cwv.json
            axe.json
```

### Visual regression workflow

```yaml
name: Visual Regression

on:
  pull_request:
    branches: [main]

jobs:
  visual:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install wavexis
        run: pip install wavexis[cdp]

      - name: Install Chrome
        run: |
          wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
          sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
          sudo apt-get update && sudo apt-get install -y google-chrome-stable

      - name: Visual diff
        run: |
          wavexis visual-diff https://staging.example.com \
            --baseline ./baselines/homepage.png \
            --threshold 0.1 \
            --assert 'diff_percentage <= 0.1' \
            --output ./diffs/homepage-diff.png

      - name: Upload diff
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: visual-diff
          path: ./diffs/
```

### Deploy gate workflow

```yaml
name: Deploy Gate

on:
  push:
    branches: [main]

jobs:
  deploy-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install wavexis
        run: pip install wavexis[cdp]

      - name: Install Chrome
        run: |
          wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
          sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
          sudo apt-get update && sudo apt-get install -y google-chrome-stable

      - name: Batch smoke tests
        run: |
          wavexis batch ./urls/production.txt \
            --assert 'status_code == 200' \
            --assert 'title !matches ".*Error.*"' \
            --output-dir ./smoke-results/

      - name: CWV deploy gate
        run: |
          wavexis cwv https://production.example.com \
            --mobile --throttle \
            --assert 'lcp_ms <= 2500' \
            --assert 'cls <= 0.1' \
            --assert 'inp_ms <= 200' \
            --output ./cwv-gate.json

      - name: Deploy
        if: success()
        run: echo "All gates passed — deploying..."
```

## Multi-Action YAML for CI

### CI assertion template

```yaml
actions:
  - navigate:
      url: https://staging.example.com
      wait_until: networkidle
  - assert:
      title: "== Welcome"
      url: "matches https://staging\\.example\\.com"
      text: "contains Sign In"
  - screenshot:
      full_page: true
      output: ./screenshots/staging.png
  - cwv:
      mobile: true
      throttle: true
      budget:
        LCP_ms: 2500
        CLS: 0.1
        INP_ms: 200
  - axe:
      tags:
        - wcag2a
        - wcag2aa
      impact_threshold: serious
      assert: true
      output: ./axe-results.json
```

## Best Practices

- **Use `--assert` for all CI gates** — exit codes drive pipeline decisions.
- **Save outputs as artifacts** — use `--output` and upload artifacts for debugging.
- **Use batch for smoke tests** — verify multiple pages after deploy.
- **Store baselines in git** — visual regression baselines should be version-controlled.
- **Set thresholds carefully** — too strict causes flaky CI; too loose misses regressions.
- **Use serve mode for large pipelines** — share browser instances across jobs.
- **Run CWV with `--throttle`** — simulate real-world conditions in CI.
- **Run axe with `--impact-threshold`** — focus on serious/critical issues in CI.
- **Use `--wait-for` for SPAs** — ensure dynamic content is loaded before assertions.
- **Set per-URL timeouts in batch** — prevent one slow page from blocking the pipeline.

## Common Pitfalls

- **Not handling exit code 2** — code 2 means error, not assertion failure; handle differently.
- **Baselines out of date** — update baselines after intentional UI changes.
- **Visual diff too strict** — `--threshold 0.01` causes flaky failures from anti-aliasing.
- **Not using `--throttle` for CWV** — lab data without throttle doesn't reflect real users.
- **Batch without `--delay`** — hammering a staging server can cause false failures.
- **Not uploading artifacts** — without outputs, CI failures are impossible to debug.
- **Serve mode without rate limiting** — concurrent jobs can overwhelm the browser pool.
- **Assertions on dynamic content** — use `--wait-for` before asserting on SPA content.

## References

- `references/ci-assertions.md` — Assertion patterns and exit codes
- `references/visual-diff.md` — Visual regression setup and baselines
- `assets/workflows/github-actions-wavexis.yml` — GitHub Actions workflow
- `assets/docker/docker-compose.yml` — Docker Compose for serve mode
- `assets/templates/ci-assertion.yml` — CI assertion YAML template

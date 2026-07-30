---
name: WaveXis Performance Audit
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Performance auditing with wavexis. Core Web Vitals measurement (LCP, CLS, INP), CPU traces, JS/CSS coverage, heap snapshots, Lighthouse audits, CI budgets."
tags: [core-web-vitals, performance, lighthouse, tracing]
trigger: When the user asks about performance auditing with wavexis, needs Core Web Vitals measurement, wants Lighthouse audits, needs CPU traces or JS/CSS coverage, or wants CI performance gates with budgets.
---

# WaveXis Performance Audit

## Description

Performance auditing with wavexis — measure Core Web Vitals (LCP, CLS, INP), capture CPU traces, analyze JS/CSS coverage, take heap snapshots, run Lighthouse audits, and enforce CI performance budgets.

## When to Invoke

- Measuring Core Web Vitals (LCP, CLS, INP) for a page
- Running Lighthouse audits (performance, accessibility, best practices, SEO)
- Capturing CPU performance traces
- Analyzing JS or CSS code coverage
- Taking heap snapshots for memory analysis
- Setting up CI performance gates with budgets
- Generating performance reports for CI/CD

## Prerequisites

- `pip install wavexis[cdp]`
- Chrome or Edge installed
- Basic familiarity with wavexis CLI (see `wavexis-cli-automation` skill)

## perf Command

The `perf` command provides subcommands for performance profiling.

### Metrics

Collect performance metrics from a page load:

```bash
wavexis perf metrics https://example.com
```

Output includes:
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Cumulative Layout Shift (CLS)
- Interaction to Next Paint (INP)
- Total Blocking Time (TBT)
- Time to Interactive (TTI)
- Speed Index
- Time to First Byte (TTFB)

### Trace

Capture a CPU performance trace:

```bash
wavexis perf trace https://example.com --output trace.json
```

### Profile

Capture a CPU profile:

```bash
wavexis perf profile https://example.com --output profile.json
```

### JS Coverage

Measure JavaScript code coverage:

```bash
wavexis perf coverage https://example.com --output js-coverage.json
```

Returns:
- URL of each JS file
- Total bytes
- Used bytes
- Unused bytes
- Usage percentage

### CSS Coverage

Measure CSS code coverage:

```bash
wavexis perf css-coverage https://example.com --output css-coverage.json
```

### Heap Snapshot

Take a heap snapshot for memory analysis:

```bash
wavexis perf heap-snapshot https://example.com --output heap.heapsnapshot
```

### perf options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--output` | `str` | stdout | Output file path |
| `--timeout` | `int` | `30000` | Page load timeout (ms) |
| `--wait-until` | `str` | `load` | Wait condition: `load`, `domcontentloaded`, `networkidle` |
| `--repeats` | `int` | `1` | Number of runs to average |
| `--mobile` | `flag` | off | Emulate mobile device |
| `--throttle` | `flag` | off | Apply CPU/network throttling |

## cwv Command

Measure Core Web Vitals with 0-100 scoring.

### Basic CWV measurement

```bash
wavexis cwv https://example.com
```

### CWV with mobile emulation

```bash
wavexis cwv https://example.com --mobile
```

### CWV with throttling

```bash
wavexis cwv https://example.com --throttle
```

### CWV with multiple runs

```bash
wavexis cwv https://example.com --repeats 5
```

### CWV output

```json
{
  "lcp": {
    "value": 2200,
    "unit": "ms",
    "rating": "needs-improvement",
    "score": 75
  },
  "cls": {
    "value": 0.05,
    "unit": "score",
    "rating": "good",
    "score": 100
  },
  "inp": {
    "value": 180,
    "unit": "ms",
    "rating": "good",
    "score": 92
  },
  "overall": {
    "score": 89,
    "rating": "needs-improvement"
  }
}
```

### Rating thresholds

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤ 2.5s | 2.5s - 4.0s | > 4.0s |
| CLS | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |
| INP | ≤ 200ms | 200ms - 500ms | > 500ms |

### CWV with budget

```bash
wavexis cwv https://example.com --budget budget.json
```

Exits with code 1 if any metric exceeds the budget.

## CWV Budgets

### Budget JSON format

```json
{
  "lcp_ms": 2500,
  "cls": 0.1,
  "inp_ms": 200,
  "fcp_ms": 1800,
  "tbt_ms": 200,
  "tti_ms": 3800,
  "speed_index_ms": 3400
}
```

### Budget with CI assert

```bash
wavexis cwv https://example.com \
    --budget budget.json \
    --assert
```

When `--assert` is used, the command exits with:
- **0** — all metrics within budget
- **1** — one or more metrics exceeded budget

### Budget keys

| Key | Unit | Description |
|-----|------|-------------|
| `lcp_ms` | ms | Largest Contentful Paint |
| `cls` | score | Cumulative Layout Shift |
| `inp_ms` | ms | Interaction to Next Paint |
| `fcp_ms` | ms | First Contentful Paint |
| `tbt_ms` | ms | Total Blocking Time |
| `tti_ms` | ms | Time to Interactive |
| `speed_index_ms` | ms | Speed Index |
| `ttfb_ms` | ms | Time to First Byte |

## lighthouse Command

Run Lighthouse audits directly from wavexis.

### Basic Lighthouse audit

```bash
wavexis lighthouse https://example.com
```

### Specific categories

```bash
wavexis lighthouse https://example.com \
    --categories performance,accessibility,best-practices,seo
```

### Mobile form factor

```bash
wavexis lighthouse https://example.com \
    --form-factor mobile \
    --throttle
```

### Lighthouse with output

```bash
wavexis lighthouse https://example.com \
    --output lighthouse-report.html \
    --format html
```

### Output formats

```bash
# HTML report
wavexis lighthouse https://example.com --format html --output report.html

# JSON report
wavexis lighthouse https://example.com --format json --output report.json

# Both
wavexis lighthouse https://example.com --format html,json --output report
```

### Lighthouse options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--categories` | `str` | all | Comma-separated categories |
| `--form-factor` | `str` | `mobile` | `mobile` or `desktop` |
| `--throttle` | `flag` | off | Apply CPU/network throttling |
| `--output` | `str` | stdout | Output file path |
| `--format` | `str` | `html` | `html`, `json`, or both |
| `--budget` | `str` | None | Performance budget JSON |

## Report Generation

### Combined performance report

```bash
wavexis perf metrics https://example.com --output metrics.json
wavexis cwv https://example.com --output cwv.json
wavexis lighthouse https://example.com --output lighthouse.html
```

### Multi-action YAML for full audit

```yaml
actions:
  - navigate:
      url: https://example.com
      wait_until: networkidle
  - cwv:
      budget:
        LCP_ms: 2500
        CLS: 0.1
        INP_ms: 200
  - lighthouse:
      categories:
        - performance
        - accessibility
      form_factor: mobile
  - perf:
      trace: true
      output: trace.json
  - screenshot:
      full_page: true
```

## CI Integration

### Performance gate in CI

```bash
# Run CWV with budget assertion
wavexis cwv https://staging.example.com \
    --budget ci-budget.json \
    --assert \
    --mobile \
    --throttle

# Exit code 0 = pass, 1 = fail
echo "Performance gate: $?"
```

### GitHub Actions integration

```yaml
- name: Performance audit
  run: |
    wavexis cwv https://staging.example.com \
        --budget ci-budget.json \
        --assert \
        --mobile \
        --throttle \
        --output cwv-results.json

- name: Upload results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: perf-results
    path: cwv-results.json
```

### Lighthouse CI gate

```bash
wavexis lighthouse https://staging.example.com \
    --categories performance \
    --form-factor mobile \
    --throttle \
    --budget lighthouse-budget.json \
    --assert
```

### Budget for Lighthouse

```json
{
  "performance": 80,
  "accessibility": 90,
  "best-practices": 85,
  "seo": 85
}
```

## Interpreting Results

### Core Web Vitals ratings

| Rating | Color | Meaning |
|--------|-------|---------|
| Good | Green | Meets Google thresholds |
| Needs Improvement | Orange | Close to thresholds, may affect UX |
| Poor | Red | Fails thresholds, likely affects UX |

### Lighthouse scores

| Score Range | Rating | Action |
|-------------|--------|--------|
| 90-100 | Good | Maintain |
| 50-89 | Needs Improvement | Optimize |
| 0-49 | Poor | Critical — fix immediately |

### Common performance issues

| Symptom | Likely Cause | Metric Affected |
|---------|-------------|-----------------|
| Slow first paint | Render-blocking resources | FCP, LCP |
| Large layout shifts | Images without dimensions | CLS |
| Slow interaction | Long JavaScript tasks | INP, TBT |
| Slow page load | Large JS bundles | TTI, Speed Index |
| High unused JS | Unoptimized bundles | JS Coverage |
| High unused CSS | Unused stylesheets | CSS Coverage |
| Memory leaks | Growing heap | Heap Snapshot |

## Best Practices

- **Use `--mobile` for CWV** — Google ranks on mobile-first.
- **Use `--throttle`** — simulate real-world network/CPU conditions.
- **Run multiple times** — `--repeats 5` gives stable averages.
- **Set budgets** — define `--budget` JSON for CI gates.
- **Use `--assert` in CI** — exit code 1 fails the build.
- **Save reports** — `--output` for artifacts and trend analysis.
- **Test staging, not production** — avoid skewing real-user data.
- **Check JS/CSS coverage** — high unused % means optimization opportunity.
- **Monitor trends** — compare results across builds.
- **Fix poor ratings first** — they have the highest UX impact.

## Common Pitfalls

- **No throttling** — results look good but don't reflect real users.
- **Single run** — CWV can vary; use `--repeats` for stability.
- **Testing localhost** — network latency is zero; use `--throttle`.
- **Ignoring INP** — INP replaced FID; it's now a Core Web Vital.
- **Budget too strict** — set realistic budgets based on current performance.
- **Not saving results** — without `--output`, results are lost.
- **Wrong form factor** — mobile and desktop scores differ significantly.
- **Ignoring coverage** — unused JS/CSS is a major performance bottleneck.

## References

- `references/cwv-thresholds.md` — Official Google CWV thresholds
- `references/perf-metrics-reference.md` — Performance metrics reference
- `references/lighthouse-scoring.md` — Lighthouse audit categories and scoring
- `assets/templates/perf-audit.yml` — Performance audit YAML template
- `assets/templates/cwv-budget.json` — CWV budget JSON template
- `assets/templates/ci-perf-gate.yml` — CI performance gate template
- [wavexis on GitHub](https://github.com/MathiasPaulenko/wavexis)
- [Core Web Vitals](https://web.dev/vitals/)
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/)

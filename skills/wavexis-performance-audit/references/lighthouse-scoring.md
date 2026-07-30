# Lighthouse Scoring — Categories and Scoring

> Guide to Lighthouse audit categories, scoring methodology, and how wavexis integrates with Lighthouse.

## Lighthouse Categories

| Category | Weight | Description |
|----------|--------|-------------|
| Performance | 40% | Page load speed and runtime performance |
| Accessibility | 25% | WCAG compliance and screen reader support |
| Best Practices | 20% | Web development best practices |
| SEO | 15% | Search engine optimization |

### Running specific categories

```bash
# All categories (default)
wavexis lighthouse https://example.com

# Performance only
wavexis lighthouse https://example.com --categories performance

# Multiple categories
wavexis lighthouse https://example.com --categories performance,accessibility,seo
```

## Performance Score Calculation

The performance score is a weighted average of individual audit scores:

| Audit | Weight | Description |
|-------|--------|-------------|
| LCP | 25% | Largest Contentful Paint |
| TBT | 30% | Total Blocking Time |
| CLS | 15% | Cumulative Layout Shift |
| Speed Index | 10% | How quickly content displays |
| FCP | 10% | First Contentful Paint |
| TTI | 10% | Time to Interactive |

### Score ranges

| Score | Rating | Color |
|-------|--------|-------|
| 90-100 | Good | Green |
| 50-89 | Needs Improvement | Orange |
| 0-49 | Poor | Red |

## Accessibility Audits

Lighthouse checks accessibility against WCAG criteria:

| Audit | Description |
|-------|-------------|
| Color contrast | Text contrast ratio ≥ 4.5:1 |
| Image alt text | All images have `alt` attributes |
| Label association | Form inputs have associated labels |
| Heading hierarchy | Headings are properly nested |
| ARIA validity | ARIA attributes are correctly used |
| Tab order | Tab order follows visual order |
| Touch targets | Touch targets are ≥ 24x24 CSS pixels |
| Language attribute | `<html lang>` is set |
| Document title | Page has a descriptive title |
| Meta viewport | Viewport meta tag is present |

## Best Practices Audits

| Audit | Description |
|-------|-------------|
| HTTPS | Page served over HTTPS |
| HTTP/2+ | Uses HTTP/2 or HTTP/3 |
| No console errors | No errors in console |
| No deprecated APIs | No deprecated web API usage |
| Image aspect ratio | Images have correct aspect ratios |
| No large layout shifts | CLS is within acceptable range |
| Efficient cache headers | Static assets have long cache TTLs |
| Compression | Text assets are compressed (gzip/brotli) |

## SEO Audits

| Audit | Description |
|-------|-------------|
| Meta description | Page has a meta description |
| Document title | Title is descriptive and unique |
| Link text | Links have descriptive text |
| Crawlable links | Links are crawlable (not JS-only) |
| robots.txt | robots.txt is valid |
| hreflang | hreflang tags are valid |
| Canonical | Canonical link is valid |
| Mobile-friendly | Page is mobile-friendly |
| Font size | Font sizes are ≥ 12px |
| Tap targets | Tap targets are adequately sized |

## Form Factors

### Mobile (default)

- CPU: 4x slowdown
- Network: 1.6 Mbps down / 750 Kbps up (Simulated 3G)
- Screen: 412x823 (Pixel 5)

```bash
wavexis lighthouse https://example.com --form-factor mobile --throttle
```

### Desktop

- CPU: 1x slowdown
- Network: 40 Mbps down / 10 Mbps up
- Screen: 1350x940

```bash
wavexis lighthouse https://example.com --form-factor desktop
```

## Lighthouse Budgets

### Score-based budget

```json
{
  "performance": 80,
  "accessibility": 90,
  "best-practices": 85,
  "seo": 85
}
```

```bash
wavexis lighthouse https://example.com \
    --budget lighthouse-budget.json \
    --assert
```

### Metric-based budget

```json
{
  "lcp_ms": 2500,
  "cls": 0.1,
  "tbt_ms": 200,
  "fcp_ms": 1800,
  "speed_index_ms": 3400,
  "tti_ms": 3800
}
```

## Lighthouse Output

### HTML report

```bash
wavexis lighthouse https://example.com --format html --output report.html
```

The HTML report includes:
- Overall scores per category
- Individual audit results
- Pass/fail/warning status
- Opportunities (estimated load time savings)
- Diagnostics (additional metrics)
- Passed audits

### JSON report

```bash
wavexis lighthouse https://example.com --format json --output report.json
```

The JSON report includes:
- `categories` — scores per category
- `audits` — individual audit results
- `configSettings` — run configuration
- `timing` — total audit time
- `lighthouseVersion` — Lighthouse version

### Reading JSON results

```python
import json

with open("report.json") as f:
    report = json.load(f)

# Category scores
for cat, data in report["categories"].items():
    print(f"{cat}: {data['score'] * 100:.0f}")

# Individual audits
for audit_id, audit in report["audits"].items():
    if audit["score"] is not None:
        status = "pass" if audit["score"] == 1 else "fail"
        print(f"  {audit_id}: {status} - {audit.get('displayValue', '')}")
```

## CI Integration

### GitHub Actions

```yaml
- name: Lighthouse audit
  run: |
    wavexis lighthouse https://staging.example.com \
        --categories performance,accessibility \
        --form-factor mobile \
        --throttle \
        --budget lighthouse-budget.json \
        --assert \
        --output lighthouse-report.html \
        --format html

- name: Upload report
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: lighthouse-report
    path: lighthouse-report.html
```

### Performance gate with Lighthouse

```bash
#!/bin/bash
set -e

# Run Lighthouse with budget
wavexis lighthouse https://staging.example.com \
    --categories performance \
    --form-factor mobile \
    --throttle \
    --budget perf-budget.json \
    --assert \
    --output report.html \
    --format html

echo "Lighthouse performance gate passed"
```

## Common Lighthouse Issues

| Issue | Audit | Fix |
|-------|-------|-----|
| Render-blocking resources | Performance | Defer or inline critical CSS/JS |
| Unused CSS | Performance | Remove or purge unused styles |
| Unused JavaScript | Performance | Code-split, tree-shake |
| Large images | Performance | Compress, use modern formats (WebP/AVIF) |
| Missing alt text | Accessibility | Add `alt` attributes to images |
| Low contrast | Accessibility | Increase contrast ratio |
| Missing meta description | SEO | Add `<meta name="description">` |
| No HTTPS | Best Practices | Enable HTTPS with TLS certificate |

## References

- [Lighthouse documentation](https://developer.chrome.com/docs/lighthouse/)
- [Lighthouse performance scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring)
- [Lighthouse audits](https://developer.chrome.com/docs/lighthouse/best-practices/performance)

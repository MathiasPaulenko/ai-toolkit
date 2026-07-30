# Core Web Vitals Thresholds — Official Google Ratings

> Official Google Core Web Vitals thresholds and scoring methodology.

## Core Web Vitals (2024)

Core Web Vitals are the subset of Web Vitals that apply to all web pages. They measure real-world user experience for loading, interactivity, and visual stability.

| Metric | Good | Needs Improvement | Poor | Unit |
|--------|------|-------------------|------|------|
| LCP | ≤ 2,500 | 2,500 - 4,000 | > 4,000 | ms |
| CLS | ≤ 0.1 | 0.1 - 0.25 | > 0.25 | score |
| INP | ≤ 200 | 200 - 500 | > 500 | ms |

## LCP — Largest Contentful Paint

Measures loading performance. Marks the point when the largest text block or image element renders.

### What counts as LCP

- `<img>` elements
- `<video>` poster images
- Background images (inline or CSS)
- Text blocks (paragraphs, headings, list items)
- Block-level elements with text

### Common LCP issues

| Issue | Fix |
|-------|-----|
| Slow server response | Optimize TTFB, use CDN |
| Render-blocking JS/CSS | Defer non-critical resources |
| Large image files | Compress, use WebP/AVIF, responsive images |
| No image dimensions | Add `width` and `height` attributes |
| Client-side rendering | Consider SSR or pre-rendering |
| Font loading | Use `font-display: swap` |

### LCP scoring in wavexis

| LCP (ms) | Score | Rating |
|-----------|-------|--------|
| ≤ 2,500 | 90-100 | Good |
| 2,500-4,000 | 50-89 | Needs Improvement |
| > 4,000 | 0-49 | Poor |

## CLS — Cumulative Layout Shift

Measures visual stability. Quantifies how much page content shifts during loading.

### What causes CLS

- Images without dimensions
- Ads or embeds without reserved space
- Dynamically injected content
- Web fonts causing FOIT/FOUT
- Animations that move elements

### CLS scoring in wavexis

| CLS | Score | Rating |
|-----|-------|--------|
| ≤ 0.1 | 90-100 | Good |
| 0.1-0.25 | 50-89 | Needs Improvement |
| > 0.25 | 0-49 | Poor |

### Fixing CLS

| Issue | Fix |
|-------|-----|
| Images without dimensions | Add `width` and `height` |
| Ads | Reserve space with CSS `min-height` |
| Dynamic content | Insert above existing content, not below |
| Fonts | Use `font-display: swap` or `size-adjust` |
| Animations | Use `transform` instead of `top/left` |

## INP — Interaction to Next Paint

Measures interactivity. Captures the delay between user input and the next paint.

### What INP measures

- Clicks
- Taps
- Key presses
- Drag interactions

### INP vs FID

INP replaced First Input Delay (FID) in March 2024:
- FID measured only the first interaction
- INP measures all interactions and reports the worst (or near-worst)
- INP captures the full interaction: input delay, processing time, presentation delay

### INP scoring in wavexis

| INP (ms) | Score | Rating |
|-----------|-------|--------|
| ≤ 200 | 90-100 | Good |
| 200-500 | 50-89 | Needs Improvement |
| > 500 | 0-49 | Poor |

### Fixing INP

| Issue | Fix |
|-------|-----|
| Long JavaScript tasks | Break into smaller chunks, use `scheduler.yield()` |
| Heavy event handlers | Debounce or throttle |
| Large JavaScript bundles | Code-split, lazy load |
| Third-party scripts | Load async, defer |
| Unoptimized rendering | Use `requestAnimationFrame` for visual updates |
| Excessive reflows | Batch DOM reads/writes |

## Other Web Vitals

### FCP — First Contentful Paint

| Rating | Threshold |
|--------|-----------|
| Good | ≤ 1,800 ms |
| Needs Improvement | 1,800 - 3,000 ms |
| Poor | > 3,000 ms |

### TTFB — Time to First Byte

| Rating | Threshold |
|--------|-----------|
| Good | ≤ 800 ms |
| Needs Improvement | 800 - 1,800 ms |
| Poor | > 1,800 ms |

### TBT — Total Blocking Time (lab only)

| Rating | Threshold |
|--------|-----------|
| Good | ≤ 200 ms |
| Needs Improvement | 200 - 600 ms |
| Poor | > 600 ms |

### Speed Index (lab only)

| Rating | Threshold |
|--------|-----------|
| Good | ≤ 3,400 ms |
| Needs Improvement | 3,400 - 5,800 ms |
| Poor | > 5,800 ms |

## Scoring Methodology

### Per-metric scoring

Each metric is scored 0-100 based on the thresholds:

```
Score = 100 - (penalty based on distance from "Good" threshold)
```

### Overall CWV score

The overall score is the lowest of the three Core Web Vitals scores:

```python
overall_score = min(lcp_score, cls_score, inp_score)
```

### Rating logic

```python
if overall_score >= 90:
    rating = "good"
elif overall_score >= 50:
    rating = "needs-improvement"
else:
    rating = "poor"
```

## Field Data vs Lab Data

| Aspect | Field Data | Lab Data |
|--------|-----------|---------|
| Source | Real Chrome users | Simulated in wavexis |
| Metrics | LCP, CLS, INP | All metrics |
| Environment | Real devices/networks | Configurable |
| Sample | 28-day window | Single run |
| Use case | Monitor real UX | Debug and optimize |

### wavexis uses lab data

wavexis generates lab data — simulated measurements under controlled conditions. For field data, use the Chrome UX Report (CrUX) API.

## Passing CWV Assessment

To pass the CWV assessment in Google Search:

1. All three metrics must be in the "Good" range
2. Measured on mobile (Google uses mobile-first indexing)
3. Based on 28-day field data (CrUX)
4. Applies to the origin or specific URLs

### wavexis simulation for CWV assessment

```bash
wavexis cwv https://example.com \
    --mobile \
    --throttle \
    --repeats 5 \
    --budget cwv-budget.json \
    --assert
```

## References

- [Core Web Vitals](https://web.dev/vitals/)
- [LCP](https://web.dev/articles/lcp)
- [CLS](https://web.dev/articles/cls)
- [INP](https://web.dev/articles/inp)
- [Web Vitals thresholds](https://web.dev/articles/vitals#metrics)

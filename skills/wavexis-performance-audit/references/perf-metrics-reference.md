# Performance Metrics Reference

> Complete reference of performance metrics available in wavexis `perf` command.

## Navigation Timing Metrics

| Metric | Description | How to improve |
|--------|-------------|----------------|
| TTFB | Time to First Byte — server response time | Use CDN, optimize server, caching |
| FCP | First Contentful Paint — first text/image rendered | Eliminate render-blocking resources |
| LCP | Largest Contentful Paint — largest element rendered | Optimize images, reduce server time |
| TTI | Time to Interactive — page is fully interactive | Reduce JS execution time |
| TBT | Total Blocking Time — sum of long task blocking periods | Break long tasks, code-split |

## Visual Stability

| Metric | Description | How to improve |
|--------|-------------|----------------|
| CLS | Cumulative Layout Shift — visual stability | Add image dimensions, reserve space |

## Interactivity

| Metric | Description | How to improve |
|--------|-------------|----------------|
| INP | Interaction to Next Paint — responsiveness | Break long tasks, optimize handlers |
| FID | First Input Delay — (deprecated, replaced by INP) | Same as INP |

## Speed Metrics

| Metric | Description | How to improve |
|--------|-------------|----------------|
| Speed Index | How quickly content is visually displayed | Optimize above-the-fold content |
| FMP | First Meaningful Paint — (deprecated) | Same as FCP/LCP |

## Network Metrics

| Metric | Description | How to improve |
|--------|-------------|----------------|
| DNS Lookup | DNS resolution time | Use DNS caching, faster DNS provider |
| TCP Connect | TCP connection time | Use HTTP/2 or HTTP/3, keep-alive |
| SSL Negotiation | TLS handshake time | Use modern TLS, session resumption |
| Request Time | Time to send request | Minimize redirects |
| Response Time | Time to receive first byte | Optimize server, use CDN |

## CPU Metrics

| Metric | Description | How to improve |
|--------|-------------|----------------|
| Script Duration | Total JS execution time | Code-split, tree-shake, lazy load |
| Task Duration | Total time in all tasks | Break long tasks |
| Long Tasks | Number of tasks > 50ms | Break into smaller chunks |
| Main Thread Work | Total main thread blocking | Offload to Web Workers |

## Memory Metrics

| Metric | Description | How to improve |
|--------|-------------|----------------|
| JS Heap Used | JavaScript heap memory used | Fix memory leaks, release references |
| JS Heap Total | Total JavaScript heap size | Monitor for growth |
| DOM Nodes | Number of DOM nodes | Simplify DOM, virtual scrolling |
| JS Event Listeners | Number of event listeners | Remove unused listeners |
| Layout Objects | Number of layout objects | Simplify CSS, reduce nesting |

## Coverage Metrics

### JS Coverage

| Field | Description |
|-------|-------------|
| URL | JavaScript file URL |
| Total bytes | Total size of the script |
| Used bytes | Bytes executed during page load |
| Unused bytes | Bytes not executed |
| Usage % | Used / Total * 100 |

### CSS Coverage

| Field | Description |
|-------|-------------|
| URL | CSS file URL |
| Total bytes | Total size of the stylesheet |
| Used bytes | Bytes matching rendered elements |
| Unused bytes | Bytes not matching any element |
| Usage % | Used / Total * 100 |

## Trace Events

CPU traces contain detailed event data:

| Event Type | Description |
|-----------|-------------|
| `ParseHTML` | HTML parsing |
| `ParseScript` | JavaScript parsing |
| `EvaluateScript` | JavaScript evaluation |
| `FunctionCall` | Function call |
| `GCEvent` | Garbage collection |
| `DOMEvent` | DOM event handling |
| `Layout` | Layout recalculation |
| `Paint` | Paint event |
| `CompositeLayers` | Layer compositing |
| `XHRReadyStateChange` | XHR state change |
| `ResourceReceive` | Resource received |
| `ResourceSend` | Resource sent |

## Metric Relationships

```
TTFB → FCP → LCP → TTI
                   ↗
           TBT → INP
```

- TTFB affects FCP (can't paint before first byte)
- FCP affects LCP (LCP is always ≥ FCP)
- TBT correlates with INP (blocking time delays interactions)
- Speed Index is independent but correlates with FCP/LCP

## Measurement Modes

### Lab data (wavexis)

- Controlled environment
- Simulated device and network
- Repeatable
- Good for debugging

### Field data (CrUX)

- Real user data
- 28-day aggregation
- Actual devices and networks
- Good for monitoring

## Throttling Profiles

| Profile | CPU | Network | Use case |
|---------|-----|---------|----------|
| No throttle | None | None | Development |
| Lighthouse mobile | 4x slowdown | 1.6 Mbps down / 750 Kbps up | Default Lighthouse |
| Slow 3G | None | 400 Kbps / 400 Kbps | Worst-case |
| Custom | Configurable | Configurable | Specific testing |

```bash
# Lighthouse default throttling
wavexis cwv https://example.com --mobile --throttle

# No throttling (dev mode)
wavexis cwv https://example.com
```

## Reading perf output

### metrics output (JSON)

```json
{
  "ttfb_ms": 120,
  "fcp_ms": 850,
  "lcp_ms": 2200,
  "cls": 0.05,
  "inp_ms": 180,
  "tbt_ms": 150,
  "tti_ms": 3200,
  "speed_index_ms": 2800
}
```

### coverage output (JSON)

```json
{
  "scripts": [
    {
      "url": "https://example.com/app.js",
      "total_bytes": 250000,
      "used_bytes": 80000,
      "unused_bytes": 170000,
      "usage_percent": 32
    }
  ],
  "stylesheets": [
    {
      "url": "https://example.com/styles.css",
      "total_bytes": 45000,
      "used_bytes": 12000,
      "unused_bytes": 33000,
      "usage_percent": 27
    }
  ]
}
```

## References

- [Web Performance Metrics](https://web.dev/articles/metrics)
- [Navigation Timing API](https://developer.mozilla.org/en-US/docs/Web/API/Performance_API/Navigation_timing)
- [Lighthouse Performance Scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring)

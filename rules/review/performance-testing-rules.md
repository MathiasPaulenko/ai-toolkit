---
name: Performance Testing Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Rules for designing, executing, and reporting performance tests. Covers SLA definition, environment parity, result analysis, and bottleneck identification.
tags: [performance, load-testing, sla, rules, qa]
role: performance-rules
type: rules
language: en
---

# Performance Testing Rules

## 1. SLA Definition

### Rule 1.1: Define Before Testing
- Response time, throughput, and error rate SLAs must be agreed with stakeholders before the first test run.
- SLAs must be realistic and based on production telemetry or business requirements.

```markdown
| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| p50 latency | < 200ms | 200-500ms | > 500ms |
| p95 latency | < 500ms | 500-1000ms | > 1000ms |
| p99 latency | < 1000ms | 1-3s | > 3s |
| Error rate | < 0.1% | 0.1-1% | > 1% |
| Throughput | > 1000 RPS | 500-1000 | < 500 |
```

### Rule 1.2: Test What Matters
- Focus on user-facing transactions (login, search, checkout).
- Do not micro-optimize endpoints that represent < 1% of traffic.

## 2. Environment Parity

### Rule 2.1: Mirror Production
- Hardware, network, database size, and cache state must match production as closely as possible.
- Document all deviations and their expected impact.

### Rule 2.2: No Cold Starts
- Warm up caches, connection pools, and JVM before measuring.
- Discard the first 5 minutes of results if not warmed up.

### Rule 2.3: Isolate the Test Environment
- No other tests, deployments, or batch jobs running concurrently.
- Monitoring must show only the load test traffic.

## 3. Test Design

### Rule 3.1: Realistic Load Profile
- Use production traffic patterns: ramp-up, peak, steady, ramp-down.
- Do not start with full peak load unless testing recovery behavior.

```
Ramp-up:   10 min to 10K users
Steady:    30 min at 10K users
Ramp-down: 5 min to 0
```

### Rule 3.2: Dynamic Data
- Use parameterized test data to avoid cache hits that don't reflect reality.
- Never load test with the same user or product ID repeatedly.

## 4. Execution

### Rule 4.1: Monitor Everything
- Collect application metrics (latency, errors, queue depths), infrastructure metrics (CPU, memory, I/O), and database metrics (slow queries, lock waits) simultaneously.

### Rule 4.2: Run Multiple Iterations
- Execute each scenario at least 3 times and report the median.
- Discard outliers caused by environment hiccups (document why).

### Rule 4.3: Fail Fast on Errors
- If error rate exceeds 5%, abort the test immediately.
- Continuing wastes time and may corrupt data or state.

## 5. Result Analysis

### Rule 5.1: Correlate Metrics
- Always correlate application latency with infrastructure metrics.
- A 500ms response time spike without CPU increase suggests DB or external API latency.

### Rule 5.2: Identify Root Cause, Not Symptom
- "Slow API" is a symptom. Root causes: missing index, serialization overhead, blocking I/O, GC pause.
- Use profiling tools (async-profiler, py-spy, YourKit) to pinpoint.

### Rule 5.3: Report Percentiles, Not Averages
- Average latency hides outliers and is meaningless for user experience.
- Always report p50, p95, p99, and max.

## 6. Bottleneck Remediation

### Rule 6.1: Fix One at a Time
- Change one variable per re-test.
- If you add an index and a cache simultaneously, you don't know which helped.

### Rule 6.2: Validate Fixes with Re-Test
- Re-run the same load profile after each fix.
- Compare before/after metrics side by side.

### Rule 6.3: Document Equivalent Mutations
- If a fix is an "equivalent mutation" (no semantic change, e.g., refactoring), note it to avoid re-testing.

## 7. Reporting

### Rule 7.1: Executive Summary First
- Lead with pass/fail status, critical findings, and recommended actions.
- Details go in appendices for engineers.

### Rule 7.2: Include Evidence
- Screenshots of dashboards, flame graphs, and query plans.
- Link to monitoring dashboards with time ranges.

### Rule 7.3: Actionable Recommendations
- Every finding must have a proposed fix with estimated impact.
- Prioritize by business risk, not technical complexity.

## Checklist

- [ ] SLAs defined and signed off
- [ ] Environment mirrors production (documented deviations)
- [ ] Load profile based on real traffic
- [ ] Monitoring active for all layers
- [ ] Results include p50/p95/p99, not averages
- [ ] Bottlenecks have root cause identified
- [ ] Re-test validates each fix
- [ ] Report has executive summary + evidence + actions

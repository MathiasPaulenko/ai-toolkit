---
name: Generate Observability Test Plan
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Verify that logs, metrics, traces, and alerts are correctly configured and actionable for production monitoring.
tags: [qa, observability, monitoring, logging, tracing, alerting]
role: qa-engineer
model: any
trigger: When the user asks for observability testing, monitoring validation, log verification, or tracing checks.
---

# Generate Observability Test Plan

Verify that the application is observable in production: logs are useful, metrics are accurate, traces are complete, and alerts are actionable.

## 1. Logging Tests

### Content Quality
- [ ] Every error includes: timestamp, service, trace_id, user_id, error_message, stack_trace
- [ ] No sensitive data in logs (passwords, tokens, SSN)
- [ ] Log levels used correctly (ERROR for failures, WARN for anomalies, INFO for milestones)
- [ ] Structured JSON logs (not plain text)

### Searchability
- [ ] Can filter by trace_id across all services
- [ ] Can search by user_id for support tickets
- [ ] Correlation ID propagates through async flows

```python
# Test log output
import json

def test_error_log_structure():
    with capture_logs() as logs:
        service.process_invalid_order()
    
    error_log = [l for l in logs if l['level'] == 'ERROR'][0]
    assert 'trace_id' in error_log
    assert 'user_id' in error_log
    assert 'error_type' in error_log
    assert 'stack_trace' in error_log
```

## 2. Metrics Tests

- [ ] Key business metrics exposed (`orders_created_total`, `payment_failures_total`)
- [ ] SLI metrics accurate (availability, latency, error rate)
- [ ] Metric labels are low cardinality (< 100 unique values)
- [ ] Counter increments are monotonic
- [ ] Histogram buckets cover expected range

## 3. Tracing Tests

- [ ] Every request has a trace ID
- [ ] Spans cover all service calls (DB, cache, external API)
- [ ] Parent-child relationships correct
- [ ] Errors marked on the correct span
- [ ] Trace sampling not dropping critical paths

## 4. Alert Tests

- [ ] Alert fires within 2 minutes of threshold breach
- [ ] Alert includes: what, where, when, impact, runbook link
- [ ] No alert fatigue (false positive rate < 5%)
- [ ] Severity appropriate (page for P0, ticket for P1)
- [ ] Runbook exists and is up to date

## 5. Dashboard Tests

- [ ] Dashboards load in < 5 seconds
- [ ] Key metrics visible without scrolling
- [ ] Drill-down from summary to detail works
- [ ] Time ranges selectable (1h, 24h, 7d)
- [ ] Annotations for deployments/releases

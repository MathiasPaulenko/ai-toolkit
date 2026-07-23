---
name: Performance Test Session
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Structured performance testing session: define SLAs, script scenarios, execute tests, analyze bottlenecks, and report findings with actionable recommendations."
tags: [workflow, performance, load-testing, sla, profiling]
role: performance-tester---

# Performance Test Session

Structured workflow for a performance testing engagement.

## Prerequisites

- [ ] Application deployed to performance environment
- [ ] Environment mirrors production (CPU, memory, DB size)
- [ ] Monitoring tools active (APM, logs, metrics)
- [ ] Baseline metrics from current system (if migrating)

## Phase 1: Define SLAs & Objectives

### Step 1: Identify Key Scenarios

| Priority | Scenario | Business Impact |
|----------|----------|----------------|
| P0 | Login | User entry point |
| P0 | Product search | Revenue-critical |
| P0 | Checkout | Conversion |
| P1 | Order history | Retention |
| P1 | Admin dashboard | Operations |

### Step 2: Define SLAs

```markdown
| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Response Time (p50) | < 200ms | 200-500ms | > 500ms |
| Response Time (p95) | < 500ms | 500-1000ms | > 1000ms |
| Response Time (p99) | < 1000ms | 1-3s | > 3s |
| Error Rate | < 0.1% | 0.1-1% | > 1% |
| Throughput | 1000 RPS | 500-1000 | < 500 |
| CPU Usage | < 70% | 70-85% | > 85% |
| Memory Usage | < 80% | 80-90% | > 90% |
```

### Step 3: Load Model

- **Concurrent users**: 10K (peak), 5K (normal)
- **Ramp-up**: 10 minutes to peak
- **Steady state**: 30 minutes
- **Ramp-down**: 5 minutes

## Phase 2: Script Scenarios

### Step 4: Choose Tool

| Tool | Best For | Script Format |
|------|----------|---------------|
| **k6** | Modern, developer-friendly | JavaScript |
| **JMeter** | Complex protocols, GUI | JMX / DSL |
| **Gatling** | Scala teams, high throughput | Scala / Kotlin |
| **Locust** | Python, distributed | Python |

### Step 5: Write Scripts

```javascript
// k6 script: checkout flow
import http from 'k6/http';
import { check, sleep, group } from 'k6';

export const options = {
  stages: [
    { duration: '10m', target: 10000 },  // Ramp-up
    { duration: '30m', target: 10000 },  // Steady
    { duration: '5m', target: 0 },       // Ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  group('Login', () => {
    const res = http.post(`${__ENV.BASE_URL}/auth/login`, {
      email: `user${__VU}@test.com`,
      password: 'testpass',
    });
    check(res, {
      'login status 200': (r) => r.status === 200,
      'login < 200ms': (r) => r.timings.duration < 200,
    });
  });

  sleep(1);

  group('Search', () => {
    const res = http.get(`${__ENV.BASE_URL}/products?q=laptop`);
    check(res, {
      'search status 200': (r) => r.status === 200,
      'search < 300ms': (r) => r.timings.duration < 300,
    });
  });
}
```

## Phase 3: Execute Tests

### Step 6: Pre-Flight Checks

```bash
# Verify environment
curl $BASE_URL/health

# Check monitoring is active
kubectl get pods -n monitoring

# Warm up caches (optional)
./warmup.sh
```

### Step 7: Run Load Test

```bash
# k6 cloud (managed)
k6 cloud run script.js

# k6 local with output
k6 run --out influxdb=http://influxdb:8086/k6 script.js

# JMeter headless
jmeter -n -t checkout.jmx -l results.jtl -e -o report/
```

### Step 8: Monitor During Test

- APM dashboard (Datadog, New Relic, Dynatrace)
- Infrastructure metrics (CPU, memory, disk, network)
- Database slow query log
- Error logs (ELK, Loki)

## Phase 4: Analyze Results

### Step 9: Gather Metrics

```markdown
| Metric | Result | SLA | Status |
|--------|--------|-----|--------|
| p50 response | 150ms | < 200ms | Pass |
| p95 response | 750ms | < 500ms | **Fail** |
| Error rate | 0.05% | < 0.1% | Pass |
| Throughput | 1200 RPS | > 1000 | Pass |
| CPU peak | 92% | < 85% | **Fail** |
```

### Step 10: Identify Bottlenecks

Common findings:
- **DB**: Missing index, N+1 queries, slow JOINs
- **API**: Synchronous calls, no caching, serialization overhead
- **Infra**: CPU throttling, memory pressure, GC pauses
- **Network**: Latency to external APIs, DNS resolution

## Phase 5: Report & Recommend

### Step 11: Performance Report

```markdown
## Performance Test Report

### Executive Summary
- **Date**: [Date]
- **Environment**: [URL]
- **Scenarios tested**: 5
- **Overall status**: 3/5 passed

### Critical Findings
1. **p95 checkout latency 750ms** (SLA: 500ms)
   - Root cause: Database missing index on `orders.user_id`
   - Fix: Add composite index `(user_id, created_at)`
   - Estimated impact: -300ms

2. **CPU peaked at 92%** (SLA: 85%)
   - Root cause: JSON serialization blocking event loop
   - Fix: Switch to streaming response + caching layer
   - Estimated impact: -20% CPU

### Recommendations
| Priority | Action | Owner | ETA |
|----------|--------|-------|-----|
| P0 | Add DB index | Backend | 2 days |
| P0 | Implement Redis cache | Backend | 1 week |
| P1 | Async external API calls | Backend | 2 weeks |
```

### Step 12: Re-Test After Fixes

- Re-run same load profile
- Compare before/after metrics
- Verify no regressions in other scenarios

## Verification Checklist

- [ ] SLAs defined and agreed with stakeholders
- [ ] Scripts cover all P0 scenarios
- [ ] Test executed without environment issues
- [ ] Monitoring captured full metrics
- [ ] Bottlenecks identified with evidence
- [ ] Report delivered with actionable fixes
- [ ] Re-test validates improvements

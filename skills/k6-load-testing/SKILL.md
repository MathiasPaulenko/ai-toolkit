---
name: k6 Load Testing
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Modern load testing with k6: JavaScript scripting, Grafana dashboards, cloud execution, thresholds, extensions, and CI/CD integration."
tags: [load-testing, k6, performance, grafana, javascript]
role: performance-tester
---

# k6 Load Testing

Invoke when user asks about k6, modern load testing, or JavaScript-based performance scripting.

## Core Principles

- **JavaScript syntax**: Familiar to frontend/backend teams.
- **Built-in metrics**: HTTP timing, custom trends, checks, thresholds.
- **Grafana ecosystem**: Native dashboards, cloud SaaS, InfluxDB output.

## Script Structure

```javascript
import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const failRate = new Rate('failed_requests');
const responseTime = new Trend('response_time');

export const options = {
  stages: [
    { duration: '5m', target: 100 },   // Ramp-up
    { duration: '10m', target: 100 }, // Steady
    { duration: '5m', target: 200 },  // Spike
    { duration: '5m', target: 0 },    // Ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
    failed_requests: ['rate<0.05'],
  },
};

export default function () {
  group('Login', () => {
    const res = http.post(`${__ENV.BASE_URL}/auth/login`, JSON.stringify({
      email: `user${__VU}@test.com`,
      password: 'password123',
    }), { headers: { 'Content-Type': 'application/json' } });

    const success = check(res, {
      'status is 200': (r) => r.status === 200,
      'token present': (r) => r.json('access_token') !== undefined,
    });

    failRate.add(!success);
    responseTime.add(res.timings.duration);
  });

  sleep(1);
}
```

## Execution Modes

```bash
# Local
cd k6 run script.js

# Cloud (Grafana k6 Cloud)
k6 cloud run script.js

# Docker
docker run -i grafana/k6 run --vus 10 --duration 30s - <script.js

# Output to InfluxDB
k6 run --out influxdb=http://localhost:8086/k6 script.js
```

## Scenarios (Advanced Load Profiles)

```javascript
export const options = {
  scenarios: {
    constant_load: {
      executor: 'constant-vus',
      vus: 50,
      duration: '10m',
    },
    ramping_load: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '5m', target: 100 },
        { duration: '10m', target: 100 },
        { duration: '5m', target: 0 },
      ],
    },
    per_vu_iterations: {
      executor: 'per-vu-iterations',
      vus: 100,
      iterations: 10,
      maxDuration: '1h',
    },
  },
};
```

## Checks vs Thresholds

| Feature | Purpose | When It Fails |
|---------|---------|---------------|
| **Check** | Validate response content | Logged, does not abort |
| **Threshold** | Enforce SLA | Aborts test if breached |

```javascript
// Check (validation)
check(res, {
  'status is 200': (r) => r.status === 200,
});

// Threshold (SLA enforcement)
thresholds: {
  http_req_duration: ['p(95)<500'], // Fail test if > 500ms
}
```

## Reusable Modules

```javascript
// lib/auth.js
import http from 'k6/http';

export function login(email, password) {
  const res = http.post(`${__ENV.BASE_URL}/auth/login`, JSON.stringify({
    email, password,
  }), { headers: { 'Content-Type': 'application/json' } });
  return res.json('access_token');
}
```

```javascript
// main script
import { login } from './lib/auth.js';

export default function () {
  const token = login(`user${__VU}@test.com`, 'password123');
  http.get(`${__ENV.BASE_URL}/orders`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}
```

## CI/CD Integration

```yaml
# .github/workflows/load-test.yml
name: Load Test
on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly Monday 2am

jobs:
  k6:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: grafana/k6-action@v0.3.1
        with:
          filename: tests/load.js
          flags: --out json=results.json
      - uses: actions/upload-artifact@v4
        with:
          name: k6-results
          path: results.json
```

## Extensions (xk6)

```bash
# Build k6 with extensions
go install go.k6.io/xk6/cmd/xk6@latest
xk6 build --with github.com/grafana/xk6-sql

# SQL extension usage
import sql from 'k6/x/sql';
const db = sql.open('postgres', 'postgres://user:pass@localhost/db');
```

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Hardcoded URLs | Use `__ENV.BASE_URL` |
| No sleep between requests | Add `sleep()` to simulate think time |
| Ignoring failed checks | Set thresholds to enforce SLAs |
| Single large script | Split into modules: auth, cart, checkout |
| Testing against prod directly | Use dedicated performance environment |

## Quick Reference

| Metric | Description |
|--------|-------------|
| `http_req_duration` | Total request time |
| `http_req_waiting` | Time to first byte |
| `http_req_connecting` | TCP connection time |
| `http_req_tls_handshaking` | TLS handshake time |
| `vus` | Current virtual users |
| `iterations` | Total iterations |

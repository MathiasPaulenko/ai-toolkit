---
name: Generate Load Test Script
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a ready-to-run load test script for APIs or web apps using k6, Locust, or JMeter. Includes scenarios, thresholds, and metrics collection.
tags: [qa, load-testing, k6, locust, performance, script]
role: qa-engineer
model: any
trigger: When the user asks for a load test script, k6 script, Locust script, or JMeter test plan.
---

# Generate Load Test Script

Generate a complete load test script based on application endpoints and expected traffic patterns.

## k6 Script (JavaScript)

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up
    { duration: '5m', target: 100 },   // Steady state
    { duration: '2m', target: 200 },   // Ramp up
    { duration: '5m', target: 200 },   // Steady state
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

const loginErrors = new Counter('login_errors');
const apiLatency = new Trend('api_latency');

export default function () {
  // Login
  const loginRes = http.post(`${__ENV.BASE_URL}/auth/login`, JSON.stringify({
    email: `user${__VU}@test.com`,
    password: 'testpass123',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(loginRes, {
    'login status 200': (r) => r.status === 200,
    'login has token': (r) => r.json('token') !== '',
  }) || loginErrors.add(1);

  const token = loginRes.json('token');

  // API call
  const start = Date.now();
  const res = http.get(`${__ENV.BASE_URL}/api/orders`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  apiLatency.add(Date.now() - start);

  check(res, {
    'orders status 200': (r) => r.status === 200,
    'orders response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(Math.random() * 3 + 2); // 2-5s think time
}
```

## Locust Script (Python)

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(2, 5)

    def on_start(self):
        self.client.post("/auth/login", json={
            "email": "test@test.com",
            "password": "password"
        })

    @task(3)
    def view_orders(self):
        self.client.get("/api/orders")

    @task(1)
    def create_order(self):
        self.client.post("/api/orders", json={
            "product_id": 123,
            "quantity": 1
        })
```

## Execution Commands

```bash
# k6
k6 run --env BASE_URL=https://api.example.com script.js

# Locust
locust -f locustfile.py --host https://api.example.com -u 100 -r 10
```

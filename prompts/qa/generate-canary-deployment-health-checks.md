---
name: Generate Canary Deployment Health Checks
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Define health checks and rollback criteria for canary deployments: error rates, latency, business metrics, and gradual traffic shifting."
tags: [qa, canary, deployment, monitoring, rollback, production]
role: qa-engineer
model: any
trigger: When the user asks for canary deployment, blue-green deployment, production health checks, or deployment verification.---

# Generate Canary Deployment Health Checks

Define health checks and rollback criteria for safe canary deployments.

## Canary Stages

| Stage | Traffic % | Duration | Exit Criteria |
|-------|-----------|----------|---------------|
| 1 | 1% | 10 min | No alerts, p95 < baseline + 10% |
| 2 | 5% | 15 min | Error rate < 0.1%, no new error types |
| 3 | 25% | 30 min | Business metrics stable (checkout rate) |
| 4 | 50% | 30 min | No customer complaints, support tickets stable |
| 5 | 100% | — | Monitor for 1 hour before closing rollback window |

## Health Check Categories

### 1. Technical Metrics
- HTTP 5xx rate < 0.1%
- p95 latency < baseline + 20%
- p99 latency < baseline + 50%
- CPU/memory usage within limits
- Database connection pool not exhausted
- Queue depth stable

### 2. Business Metrics
- Conversion rate change < ±2%
- Checkout completion rate stable
- Search result relevance stable
- User engagement metrics stable

### 3. Error Analysis
- No new error types (compare to baseline)
- Known error rates not increased
- No correlation between canary and errors

## Automated Rollback Triggers

```yaml
# Argo Rollouts example
analysis:
  templates:
    - templateName: success-rate
  args:
    - name: service-name
      value: my-service
  metrics:
    - name: success-rate
      interval: 5m
      successCondition: result[0] >= 0.99
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{service="my-service",status=~"2xx"}[5m]))
            /
            sum(rate(http_requests_total{service="my-service"}[5m]))
```

## Manual Verification Checklist

- [ ] Smoke tests pass on canary instances
- [ ] Key user journeys verified manually
- [ ] Feature flags behaving correctly
- [ ] No security alerts (WAF, IDS)
- [ ] Logging and tracing working

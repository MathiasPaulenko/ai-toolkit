---
name: Generate Canary Test Strategy
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Design a canary deployment test strategy with traffic splitting, health checks, rollback triggers, and observability. Covers feature flags, metrics-based gating, and automated rollback.
tags: [canary, deployment, testing, feature-flags, rollback]
role: qa-engineer
model: any
trigger: When the user asks about canary testing, canary deployment validation, progressive delivery, or feature flag testing.
---

# Generate Canary Test Strategy

Design testing for canary deployments with automated gating and rollback.

## Canary Phases

```
Phase 0: Baseline metrics (5 min)
Phase 1: 5% traffic → canary (10 min)
Phase 2: 25% traffic → canary (10 min)
Phase 3: 50% traffic → canary (10 min)
Phase 4: 100% traffic → canary (monitor 30 min)
Rollback: Any phase if gates fail
```

## Health Check Gates

### Automatic Gates

| Gate | Baseline | Canary | Action |
|------|----------|--------|--------|
| Error rate | < 0.1% | < 0.2% | Hold or rollback |
| p95 latency | < 200ms | < 250ms | Hold or rollback |
| CPU usage | < 70% | < 80% | Hold |
| Memory usage | < 80% | < 90% | Hold |
| Business metric | Baseline | ±5% | Rollback if < -10% |

### Manual Gates

- Security scan pass
- Compliance checklist complete
- On-call engineer availability
- Runbook updated for new features

## Feature Flag Integration

```python
# LaunchDarkly example
from ldclient import LDClient

ld_client = LDClient("sdk-key")

# Gradual rollout
if ld_client.variation("new-checkout-flow", user, False):
    return new_checkout()
else:
    return old_checkout()
```

```yaml
# flag-config.yaml
new-checkout-flow:
  default: false
  rules:
    - rollout:
        - variation: true
          weight: 5000   # 50%
        - variation: false
          weight: 5000
      start: 2024-01-15T09:00:00Z
```

## Automated Rollback

```yaml
# Argo Rollouts
template:
  spec:
    canary:
      steps:
        - setWeight: 5
        - pause: { duration: 10m }
        - analysis:
            templates:
              - templateName: error-rate
            args:
              - name: threshold
                value: "0.02"  # 2%
        - setWeight: 25
        - pause: { duration: 10m }
        - analysis:
            templates:
              - templateName: latency
            args:
              - name: threshold
                value: "0.25"  # 250ms p95
```

## Testing Checklist

- [ ] **Pre-canary**
  - [ ] Unit tests pass
  - [ ] Integration tests pass
  - [ ] Contract tests pass
  - [ ] Security scan clean

- [ ] **Canary validation**
  - [ ] Smoke tests on canary pods
  - [ ] Feature flag toggles correctly
  - [ ] Business metrics stable
  - [ ] No new error patterns in logs

- [ ] **Post-canary**
  - [ ] Full traffic for 30 min without alerts
  - [ ] Compare canary vs baseline metrics
  - [ ] Document any anomalies

## Observability Requirements

| Signal | Query Example |
|--------|---------------|
| Error rate | `rate(http_requests_total{status=~"5.."}[5m])` |
| Latency | `histogram_quantile(0.95, rate(http_request_duration_bucket[5m]))` |
| Business | `sum(checkout_success) / sum(checkout_attempts)` |
| Infra | `container_cpu_usage_seconds_total / container_spec_cpu_quota` |

## Rollback Decision Tree

```
Gate fails?
  ├─ Error rate > threshold?
  │   └─ Rollback immediately
  ├─ Latency > threshold?
  │   └─ Hold, investigate
  │      └─ If not resolved in 5 min → Rollback
  ├─ Business metric down > 10%?
  │   └─ Rollback immediately
  └─ Infra metric high?
      └─ Scale canary horizontally
         └─ If scaling fails → Rollback
```

## Output

Provide:
1. Traffic split schedule with durations
2. Gate definitions (automatic + manual)
3. Rollback triggers and decision tree
4. Observability queries for monitoring
5. Feature flag configuration example
6. Testing checklist per phase

---
name: Generate Chaos Engineering Tests
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Design chaos engineering experiments to test system resilience. Inject failures, validate circuit breakers, measure recovery time, and document blast radius.
tags: [chaos-engineering, resilience, fault-injection, reliability, gremlin]
role: qa-engineer
model: any
trigger: When the user asks about chaos engineering, fault injection, system resilience testing, or Gremlin experiments.
---

# Generate Chaos Engineering Tests

Design chaos experiments to validate system resilience.

## Experiment Design Framework (Chaos Monkey → Litmus → Gremlin)

### Step 1: Steady State Hypothesis

Define what "normal" looks like before introducing failure.

```markdown
| Metric | Steady State | Measurement |
|--------|--------------|-------------|
| p95 latency | < 200ms | APM dashboard |
| Error rate | < 0.1% | Monitoring |
| Checkout success | > 99% | Business metric |
| CPU | < 70% | Infrastructure |
```

### Step 2: Select Attack Type

| Attack | Tool | What It Tests |
|--------|------|---------------|
| **CPU stress** | stress-ng, Gremlin | Auto-scaling, throttling |
| **Memory exhaustion** | Gremlin, Chaos Mesh | OOM handling, graceful degradation |
| **Network latency** | tc, Toxiproxy | Timeout handling, retries |
| **Packet loss** | tc, Pumba | Resilience of TCP connections |
| **Disk fill** | dd, Gremlin | Log rotation, cleanup |
| **Process kill** | kill, Chaos Mesh | Recovery, leader election |
| **Dependency failure** | WireMock, Toxiproxy | Circuit breakers, fallbacks |
| **Zone/region outage** | AWS AZ blackout | Multi-region failover |

### Step 3: Blast Radius & Abort Conditions

```markdown
**Scope**: Single pod in staging namespace
**Duration**: 5 minutes
**Abort if**:
- Error rate > 5%
- p99 latency > 3s
- Checkout success < 95%
- Manual stop signal
```

## Gremlin Example

```python
# gremlin_experiment.py
import requests
import time

def run_experiment():
    # 1. Verify steady state
    baseline_latency = measure_latency()
    assert baseline_latency < 200

    # 2. Inject CPU attack (Gremlin API)
    gremlin.attack(
        target_type="container",
        target_selection="random",
        attack_type="cpu",
        intensity=80,  # 80% CPU
        duration=300,  # 5 minutes
        blast_radius={"namespace": "staging"}
    )

    # 3. Monitor during attack
    for i in range(30):  # 30 x 10s = 5 min
        time.sleep(10)
        current_latency = measure_latency()
        error_rate = measure_errors()

        if error_rate > 0.05:
            gremlin.halt()
            raise ExperimentFailed("Error rate exceeded 5%")

    # 4. Verify recovery
    time.sleep(60)
    recovery_latency = measure_latency()
    assert recovery_latency < baseline_latency * 1.5
```

## Kubernetes + Chaos Mesh

```yaml
# cpu-stress.yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: StressChaos
metadata:
  name: cpu-stress
  namespace: chaos-testing
spec:
  mode: one
  selector:
    namespaces:
      - staging
  stressors:
    cpu:
      workers: 2
      load: 80
  duration: 5m
```

```bash
kubectl apply -f cpu-stress.yaml
# Monitor
checkly status --watch
# Cleanup
kubectl delete -f cpu-stress.yaml
```

## Circuit Breaker Validation

```python
# Test circuit breaker trips under failure
import requests

def test_circuit_breaker():
    # Simulate downstream failure
    toxiproxy.add_latency("payment-service", latency=5000)

    # Requests should fail fast, not wait 5s
    start = time.time()
    response = requests.post("/checkout")
    elapsed = time.time() - start

    assert elapsed < 1.0  # Circuit breaker opens
    assert response.status_code == 503

    # Verify fallback
    assert response.json()["fallback"] == "Queue for later processing"
```

## Game Day Runbook

```markdown
## Game Day: Payment Service Degradation

### Participants
- SRE Lead
- On-call Engineer
- Product Owner

### Timeline
| Time | Action |
|------|--------|
| T+0  | Announce start in #incidents |
| T+1  | Inject 300ms latency to payment-service |
| T+2  | Monitor checkout success rate |
| T+5  | If success > 98%, increase latency to 1000ms |
| T+10 | If circuit breaker opens, verify fallback |
| T+15 | Restore service, verify recovery |
| T+20 | Post-mortem in #incidents |

### Success Criteria
- [ ] No manual intervention required for auto-scaling
- [ ] Fallback activated within 30s of failure
- [ ] Full recovery within 2 minutes
```

## Output

Provide:
1. Steady state hypothesis with metrics
2. Experiment design (attack type, scope, duration)
3. Abort conditions and rollback plan
4. Monitoring queries/dashboard links
5. Game day runbook if applicable

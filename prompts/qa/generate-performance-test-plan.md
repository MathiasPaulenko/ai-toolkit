---
name: Generate Performance Test Plan
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Create a performance test plan with load, stress, spike, and endurance scenarios. Includes metrics, thresholds, and tooling recommendations.
tags: [qa, performance, load-testing, jmeter, k6, stress-test]
role: qa-engineer
model: any
trigger: When the user asks for performance tests, load testing plan, or stress testing strategy.
---

# Generate Performance Test Plan

Given application characteristics and business requirements, generate a comprehensive performance test plan.

## Test Types

| Type | Purpose | Duration | Load Pattern |
|------|---------|----------|--------------|
| Load | Verify expected user load | 30-60 min | Steady state |
| Stress | Find breaking point | 15-30 min | Ramp to failure |
| Spike | Sudden traffic surge | 5-10 min | Instant peak |
| Endurance | Memory leaks / degradation | 8-24 hours | Steady state |
| Soak | Long-term stability | 72+ hours | Low steady |

## Key Metrics

- **Response Time**: p50, p95, p99 thresholds
- **Throughput**: Requests/sec, Transactions/sec
- **Error Rate**: % of 5xx / timeout responses
- **Resource Utilization**: CPU, Memory, Disk I/O, Network
- **Apdex Score**: User satisfaction index

## Output Components

### 1. Test Scenarios
```
Scenario: Checkout Flow
- Concurrent users: 1000
- Ramp-up: 5 min
- Duration: 30 min
- Think time: 3-7 seconds (randomized)
```

### 2. SLA Thresholds
```
p50 response time < 200ms
p95 response time < 800ms
p99 response time < 2000ms
Error rate < 0.1%
CPU usage < 80%
```

### 3. Tooling Configuration
- JMeter / k6 / Gatling test scripts
- Grafana dashboards for monitoring
- Prometheus alerts for SLA breaches

### 4. Infrastructure Requirements
- Load generator specs (CPU, memory, network)
- Isolated test environment
- Production-like data volume

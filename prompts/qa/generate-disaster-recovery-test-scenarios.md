---
name: Generate Disaster Recovery Test Scenarios
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Define disaster recovery test scenarios: backup restoration, failover, data corruption handling, and RTO/RPO validation."
tags: [qa, disaster-recovery, backup, failover, rto, rpo, resilience]
role: qa-engineer
model: any
trigger: When the user asks for disaster recovery testing, backup validation, failover testing, or business continuity tests.---

# Generate Disaster Recovery Test Scenarios

Define test scenarios to validate disaster recovery capabilities and business continuity.

## RTO / RPO Definitions

| Metric | Definition | Target |
|--------|-----------|--------|
| **RTO** | Recovery Time Objective | < 1 hour |
| **RPO** | Recovery Point Objective | < 15 min data loss |

## Test Scenarios

### 1. Database Failure
- [ ] Primary DB fails → automatic failover to replica (< 30s)
- [ ] Promote replica to primary
- [ ] Application reconnects without manual intervention
- [ ] No data loss during failover
- [ ] Read replicas catch up after recovery

### 2. Region Failure
- [ ] Entire region unavailable → traffic routed to secondary region
- [ ] DNS TTL short enough for quick switch
- [ ] Data replication lag acceptable (< RPO)
- [ ] State/session management works cross-region

### 3. Backup Restoration
- [ ] Full backup restores successfully
- [ ] Point-in-time recovery works (to specific transaction)
- [ ] Restoration time < RTO
- [ ] Data integrity verified after restore (checksums)
- [ ] Application functions correctly on restored data

### 4. Data Corruption
- [ ] Detect corrupted records via checksums
- [ ] Isolate corruption to prevent spread
- [ ] Restore corrupted data from backup
- [ ] Notify affected users

### 5. Dependency Failure
- [ ] External API down → circuit breaker opens
- [ ] Degraded mode still functional (cached data, queued requests)
- [ ] Queue doesn't overflow during extended outage
- [ ] Recovery after dependency restored

## Execution Schedule

| Scenario | Frequency | Environment |
|----------|-----------|-------------|
| DB failover | Monthly | Staging |
| Region failover | Quarterly | Production-like |
| Backup restore | Weekly | Isolated env |
| Full DR drill | Annually | Production |

## Validation Criteria

```markdown
## DR Test: [Scenario] [Date]

### Results
- RTO Achieved: 45 min (Target: < 60 min) ✅
- RPO Achieved: 5 min data loss (Target: < 15 min) ✅
- Data Integrity: 100% checksum match ✅

### Issues Found
- [ ] DNS propagation took 8 min (should be < 5)

### Action Items
- [ ] Reduce DNS TTL from 300s to 60s
```

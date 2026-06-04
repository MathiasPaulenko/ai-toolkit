---
name: QA Release Gate
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Quality gate process before releasing to production. Covers automated checks, manual validation, risk assessment, and go/no-go decision with sign-offs.
tags: [workflow, release, quality-gate, qa, production]
role: qa-lead
---

# QA Release Gate

Quality gate process before any release to production.

## Prerequisites

- [ ] Release candidate deployed to staging
- [ ] All code merged to release branch
- [ ] Release notes drafted
- [ ] Rollback plan documented

## Gate 1: Automated Checks

### Step 1: CI Pipeline Pass

```markdown
| Check | Required | Status |
|-------|----------|--------|
| Unit tests | > 80% coverage, all pass | Pass / Fail |
| Integration tests | All pass | Pass / Fail |
| Lint / formatting | No new violations | Pass / Fail |
| Security scan | No critical/high findings | Pass / Fail |
| Dependency audit | No known CVEs | Pass / Fail |
| Contract tests | All pass | Pass / Fail |
```

### Step 2: Performance Baseline

```markdown
| Metric | Baseline | Current | Status |
|--------|----------|---------|--------|
| p95 latency | < 200ms | ___ | Pass / Fail |
| Error rate | < 0.1% | ___ | Pass / Fail |
| CPU peak | < 70% | ___ | Pass / Fail |
| Memory peak | < 80% | ___ | Pass / Fail |
```

## Gate 2: Manual Validation

### Smoke Test Checklist

```markdown
- [ ] Homepage loads
- [ ] Login / logout works
- [ ] Core user journey (e.g., checkout) complete
- [ ] Critical API endpoints respond correctly
- [ ] Mobile responsive on iPhone + Android
- [ ] Cross-browser: Chrome, Firefox, Safari
```

### Regression Spot Checks

```markdown
- [ ] Feature X (new in this release) — tested by QA
- [ ] Feature Y (adjacent to changes) — tested by QA
- [ ] Integration Z (touched by changes) — tested by QA
```

## Gate 3: Risk Assessment

### Risk Matrix

```markdown
| Risk | Probability | Impact | Score | Mitigation |
|------|-------------|--------|-------|------------|
| Database migration fails | Low | High | 6 | Backup taken, rollback script tested |
| New auth flow breaks | Medium | High | 8 | Feature flag enabled, canary deploy |
| Third-party API down | Low | Medium | 3 | Cached responses, fallback mock |
```

### Go/No-Go Decision

```markdown
**Release Gate Decision**

Date: [Date]
Version: [Version]

| Criterion | Status | Notes |
|-----------|--------|-------|
| Automated checks | Pass / Fail | |
| Manual validation | Pass / Fail | |
| Risk assessment | Acceptable / High | |
| Rollback plan | Ready / Not Ready | |
| On-call coverage | Available / Not Available | |

**Decision**: Go / No-Go

**Sign-offs**:
- [ ] QA Lead: ___
- [ ] Dev Lead: ___
- [ ] Product Owner: ___
- [ ] SRE (if infra changes): ___
```

## Gate 4: Deployment & Monitoring

### Deployment Steps

```markdown
1. Deploy to canary (5% traffic)
2. Monitor for 30 minutes
3. If healthy, deploy to 50%
4. Monitor for 30 minutes
5. If healthy, deploy to 100%
6. Monitor for 1 hour
```

### Monitoring Checklist

```markdown
- [ ] Error rate dashboard
- [ ] Latency percentiles
- [ ] Business metrics (conversions, signups)
- [ ] Infrastructure (CPU, memory, disk)
- [ ] Alert channels active (#alerts Slack)
```

## Rollback Trigger

```markdown
Rollback immediately if:
- Error rate > 1% for 5 minutes
- p95 latency > 500ms for 10 minutes
- Business metric drops > 10%
- Customer complaints spike in support
- On-call engineer requests rollback
```

## Verification Checklist

- [ ] All automated gates passed
- [ ] Manual smoke tests passed
- [ ] Risk assessment completed
- [ ] Sign-offs obtained from all leads
- [ ] Canary deployment successful
- [ ] Monitoring active for 1 hour post-deploy
- [ ] Rollback plan tested and ready

---
name: Generate QA Metrics Dashboard
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Define key QA metrics and dashboard layout for tracking test coverage, defect density, automation ROI, and release quality over time.
tags: [qa, metrics, kpi, dashboard, reporting, dora]
role: qa-engineer
model: any
trigger: When the user asks for QA metrics, quality KPIs, test dashboard, or DORA metrics for QA.
---

# Generate QA Metrics Dashboard

Define key QA metrics and a dashboard layout for tracking quality over time.

## Leading Indicators (Predictive)

| Metric | Formula | Target | Why It Matters |
|--------|---------|--------|----------------|
| Defect Density | Bugs / story point | < 0.5 | Quality of development |
| Test Coverage | Covered lines / total lines | > 80% | Confidence in changes |
| Code Review Time | Hours from PR to merge | < 4h | Bottleneck detection |
| Build Failure Rate | Failed builds / total builds | < 5% | Stability |

## Lagging Indicators (Outcome)

| Metric | Formula | Target | Why It Matters |
|--------|---------|--------|----------------|
| Escape Rate | Production bugs / total bugs | < 10% | QA effectiveness |
| MTTR | Mean time to recovery | < 1 hour | Operational resilience |
| Customer Found Bugs | Bugs reported by users / sprint | Trending down | User perception |
| Release Frequency | Releases per week | > 2 | Agility |

## DORA Metrics for QA

| Metric | QA Contribution |
|--------|-----------------|
| **Deployment Frequency** | Fast, reliable tests enable frequent deploys |
| **Lead Time for Changes** | Automated testing reduces validation time |
| **Change Failure Rate** | Good tests catch issues before production |
| **MTTR** | Monitoring + tests help identify and fix faster |

## Dashboard Layout

```
┌─────────────────────────────────────────────┐
│  Sprint Quality Score: 8.2/10               │
├──────────────┬──────────────┬───────────────┤
│  Coverage    │  Defects     │  Automation   │
│  78% ↑       │  12 ↓        │  65% ↑        │
├──────────────┴──────────────┴───────────────┤
│  Escape Rate Trend (last 6 sprints)        │
│  ████████████████████░░░░                   │
├──────────────┬──────────────┬───────────────┤
│  Top Risks   │  Flaky Tests │  Manual Effort│
│  3 open      │  2 (1%)      │  40h → 25h    │
└──────────────┴──────────────┴───────────────┘
```

## Metric Definitions

```markdown
### Defect Density
Bugs found per story point delivered. Lower is better.
**Calculation**: `Total bugs / Total story points`

### Automation Coverage
% of testable features covered by automated tests.
**Calculation**: `Automated test cases / Total test cases`

### Test Execution Time
Time to run full regression suite. Lower enables faster feedback.
**Target**: < 30 minutes for PR gate

### Cost of Quality
Prevention + appraisal costs vs. failure costs.
**Goal**: Shift left — invest more in prevention.
```

## Alerts

- Defect density increases > 20% sprint-over-sprint
- Escape rate exceeds 15% for 2 consecutive sprints
- Build failure rate > 10%
- Critical bugs open > 48 hours

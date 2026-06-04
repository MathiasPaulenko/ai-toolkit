---
name: Generate QA Risk Analysis
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Build a risk-based testing matrix. Identify business, technical, and operational risks; assess probability and impact; prioritize test coverage accordingly.
tags: [risk-analysis, qa, prioritization, matrix, testing-strategy]
role: qa-lead
model: any
trigger: When the user asks for risk-based testing, QA risk analysis, test prioritization, or risk matrix for testing.
---

# Generate QA Risk Analysis

Build a risk-based testing matrix to prioritize coverage.

## Risk Categories

| Category | Examples |
|----------|----------|
| **Business** | Revenue impact, compliance, customer churn |
| **Technical** | Complex code, new tech, integrations, legacy |
| **Operational** | Deployment risk, rollback difficulty, monitoring gaps |
| **Security** | Authentication, authorization, data exposure |
| **Performance** | Load limits, scalability, SLA violations |

## Risk Assessment Matrix

```
Impact
High |   3   |   6   |   9   |
Med  |   2   |   4   |   6   |
Low  |   1   |   2   |   3   |
     Low     Med     High
           Probability
```

**Score ≥ 6**: Must test thoroughly (automated + manual + exploratory)
**Score 4-5**: Should test (automated + spot checks)
**Score ≤ 3**: May test (smoke test or defer)

## Template

```markdown
## Risk Analysis: [Feature/System]

### Risk Register

| ID | Risk | Category | Probability | Impact | Score | Mitigation (Tests) |
|----|------|----------|-------------|--------|-------|-------------------|
| R1 | Payment failure on checkout | Business | High | High | 9 | E2E + load + rollback test |
| R2 | Auth bypass on mobile app | Security | Med | High | 6 | Penetration + boundary tests |
| R3 | Search timeout with 1M+ docs | Performance | Med | Med | 4 | Load + profiling |
| R4 | CSV import corrupts data | Business | Low | High | 4 | Integration + validation tests |

### Coverage Plan

**Priority 1 (Score ≥ 6)**
- Full regression suite
- Automated E2E tests
- Performance/load validation
- Manual exploratory session

**Priority 2 (Score 4-5)**
- Smoke tests
- API contract tests
- Spot-check manual tests

**Priority 3 (Score ≤ 3)**
- Unit tests only
- Defer to next sprint if needed

### Execution Strategy

1. **Sprint Start**: Identify risks from JIRA/stories
2. **Daily Standup**: Update risk status (new blockers?)
3. **Test Planning**: Allocate effort by priority tier
4. **Retrospective**: Review which risks materialized

## Output

Provide:
1. Completed risk register (5-10 items)
2. Risk matrix visualization
3. Coverage allocation by priority
4. Recommended test types per risk
5. Monitoring/alerting suggestions

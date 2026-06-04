---
name: Generate Test Summary Report
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a professional test summary report with execution metrics, defect statistics, risk assessment, and recommendations.
tags: [qa, reporting, test-summary, metrics, stakeholder]
role: qa-engineer
model: any
trigger: When the user asks for a test report, test summary, QA report, or release quality assessment.
---

# Generate Test Summary Report

Generate a comprehensive test summary report for stakeholders, release management, or sprint retrospectives.

## Report Sections

### 1. Executive Summary

```markdown
## Release Quality: [Version]

**Verdict:** ✅ Ready for Production / ⚠️ Conditional Release / ❌ Not Ready

**Key Metrics:**
- Test Cases Executed: 245 / 250 (98%)
- Pass Rate: 92% (226 passed)
- Critical Defects Open: 1 (P0)
- Automation Coverage: 78%
```

### 2. Test Execution Breakdown

| Category | Total | Passed | Failed | Skipped | Blocked |
|----------|-------|--------|--------|---------|---------|
| Smoke | 15 | 15 | 0 | 0 | 0 |
| Functional | 120 | 112 | 5 | 3 | 0 |
| Regression | 80 | 74 | 4 | 2 | 0 |
| E2E | 30 | 25 | 3 | 1 | 1 |
| Performance | 10 | 8 | 2 | 0 | 0 |

### 3. Defect Summary

| Severity | Open | Closed | Deferred | Total |
|----------|------|--------|----------|-------|
| Critical | 1 | 3 | 0 | 4 |
| High | 2 | 8 | 1 | 11 |
| Medium | 5 | 15 | 3 | 23 |
| Low | 3 | 7 | 5 | 15 |

### 4. Risk Assessment

| Risk | Impact | Mitigation | Owner |
|------|--------|------------|-------|
| Payment flow untested on Safari | High | Manual validation tomorrow | QA Lead |
| 2 flaky E2E tests | Medium | Under investigation | Dev Team |

### 5. Recommendations

1. **Block release** until P0 payment bug is fixed
2. Increase E2E test stability (target: < 2% flakiness)
3. Add contract tests for new microservice integration
4. Schedule accessibility audit for next sprint

## Sprint-Level Report

```markdown
## Sprint [N] QA Report

### What was tested
- Feature A: user profile redesign
- Feature B: SSO integration

### Test effort
- Planned: 80 hours
- Actual: 94 hours (+17% due to environment issues)

### Quality trends
- Defect density: 0.8 / story point (improving vs 1.2 last sprint)
- Automation stability: 96% (up from 91%)
```

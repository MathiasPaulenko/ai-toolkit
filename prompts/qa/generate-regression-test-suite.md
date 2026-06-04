---
name: Generate Regression Test Suite
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a regression test suite to verify that recent changes did not break existing functionality. Covers smoke, sanity, and full regression selection.
tags: [qa, regression, smoke-test, sanity, critical-path]
role: qa-engineer
model: any
trigger: When the user asks for regression tests, smoke tests, sanity checks, or post-deployment verification.
---

# Generate Regression Test Suite

Generate a regression test suite based on code changes, risk analysis, and application criticality.

## Test Selection Strategy

### 1. Smoke Tests (5-10 min)
Core functionality that must work for the app to be usable:
- Application launches
- Login / authentication
- Main navigation flows
- Critical business transactions

### 2. Sanity Tests (15-30 min)
Verify the specific area changed:
- Direct features modified in the release
- Integration points with modified modules
- API contracts affected by changes

### 3. Full Regression (2-8 hours)
Comprehensive coverage:
- All critical paths
- Integration between all modules
- Edge cases previously found in production
- Cross-browser / cross-device matrix

## Risk-Based Prioritization

| Risk Factor | Weight | Selection Criteria |
|-------------|--------|-------------------|
| Code churn | High | Areas with >20% changed lines |
| Bug density | High | Modules with most historical bugs |
| Business impact | Critical | Payment, auth, data export |
| Complexity | High | Multi-service integrations |
| New features | Medium | Recently added, less battle-tested |

## Output Format

```markdown
## Regression Suite: Release v2.4.0

### Smoke (Must pass before proceeding)
- [ ] TC-S01: Login with valid credentials
- [ ] TC-S02: Access main dashboard
- [ ] TC-S03: Create basic record
- [ ] TC-S04: Logout

### Sanity (Changed areas)
- [ ] TC-N01: New payment method (Stripe)
- [ ] TC-N02: Updated user profile flow
- [ ] TC-N03: Invoice PDF generation

### Full Regression
- [ ] TC-R01-R50: [Full test list]
```

## Automation Approach

- Tag tests: `@smoke`, `@sanity`, `@regression`
- CI pipeline: smoke → sanity → regression
- Parallel execution for regression suite
- Retry flaky tests up to 3 times
- Report: passed / failed / skipped / blocked

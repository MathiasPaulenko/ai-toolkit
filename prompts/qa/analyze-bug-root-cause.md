---
name: Analyze Bug Root Cause
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Analyze a bug report to identify probable root causes, reproduce steps, affected areas, and suggest fix verification tests.
tags: [qa, bug-analysis, root-cause, debugging, defect-management]
role: qa-engineer
model: any
trigger: When the user asks to analyze a bug, find root cause, or investigate a defect.
---

# Analyze Bug Root Cause

Given a bug report with environment, steps, and symptoms, perform a structured root cause analysis.

## Analysis Framework

### 1. Bug Triage
- **Severity**: Critical / High / Medium / Low
- **Priority**: Blocker / Must-fix / Should-fix / Cosmetic
- **Component**: Frontend / Backend / Database / Integration / Infrastructure
- **Regression?**: Did this work before? Last known good version?

### 2. Reproduction Assessment
- Can the bug be reproduced consistently?
- Minimum reproduction steps
- Environment-specific (browser, OS, data state)
- Race condition indicators

### 3. Root Cause Hypotheses
| Hypothesis | Likelihood | Evidence | Verification |
|------------|------------|----------|------------|
| Missing null check | High | Stack trace shows NPE at line 42 | Unit test with null input |
| Race condition | Medium | Intermittent failures | Add logging, run 100x |
| DB migration issue | Low | Only on staging | Compare schema versions |

### 4. Affected Areas
- Direct impact: Feature X unusable
- Side effects: Feature Y may also be broken
- Data integrity: Corrupted records possible
- Performance: Slower response times

### 5. Suggested Fix Verification
- Unit test that fails before fix, passes after
- Integration test covering the scenario
- Regression test for related functionality
- Data validation for existing corrupted records

## Output Format

```markdown
## Bug Analysis: [Title]

### Triage
- Severity: High
- Component: Backend/API
- Regression: Yes (worked in v1.2.0)

### Root Cause
[Detailed explanation with code references if available]

### Fix Verification Tests
- [ ] TC-001: [Description]
- [ ] TC-002: [Description]

### Regression Risk Areas
- [ ] Area 1
- [ ] Area 2
```

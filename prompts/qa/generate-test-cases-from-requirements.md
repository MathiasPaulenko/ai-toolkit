---
name: Generate Test Cases from Requirements
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate comprehensive test cases from functional requirements, user stories, or acceptance criteria. Covers positive, negative, boundary, and edge cases.
tags: [qa, test-design, test-cases, requirements, functional-testing]
role: qa-engineer
model: any
trigger: When the user asks to create test cases from requirements, user stories, or acceptance criteria.
---

# Generate Test Cases from Requirements

Given a set of functional requirements, user stories, or acceptance criteria, generate a comprehensive test suite with the following coverage:

## Coverage Criteria

- **Positive / Happy Path**: Standard valid inputs and expected outcomes
- **Negative / Error Path**: Invalid inputs, missing data, unauthorized access
- **Boundary Value Analysis**: Min, min+1, nominal, max-1, max
- **Edge Cases**: Null, empty, special characters, extremely large data
- **Cross-Browser / Cross-Device** (if UI involved)
- **Accessibility** (WCAG 2.1 AA compliance checks)

## Output Format

For each requirement, provide:

```markdown
| ID | Requirement | Test Scenario | Preconditions | Steps | Expected Result | Priority | Type |
|----|-------------|---------------|---------------|-------|-----------------|----------|------|
| TC-001 | User can login with valid credentials | Happy path login | Account exists | 1. Enter email 2. Enter password 3. Click Login | Dashboard loads | High | Positive |
| TC-002 | User cannot login with invalid password | Invalid password | Account exists | 1. Enter email 2. Enter wrong password 3. Click Login | Error message "Invalid credentials" | High | Negative |
```

## Instructions

1. Map each acceptance criterion to at least one test case
2. Include data variations (valid/invalid/boundary)
3. Flag requirements that are ambiguous or untestable
4. Suggest missing requirements based on common patterns
5. Prioritize: P0 (blocker), P1 (critical), P2 (major), P3 (minor)

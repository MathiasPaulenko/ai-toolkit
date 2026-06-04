---
name: Validate User Story Testability
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Review user stories for testability issues: missing acceptance criteria, ambiguous requirements, untestable statements, and suggest improvements.
tags: [qa, user-stories, acceptance-criteria, testability, requirements]
role: qa-engineer
model: any
trigger: When the user asks to review user stories, check acceptance criteria, or validate testability of requirements.
---

# Validate User Story Testability

Review user stories and acceptance criteria for testability issues before development starts.

## INVEST Check

| Criterion | Question | Common Issues |
|-----------|----------|---------------|
| **I**ndependent | Can this be tested alone? | Depends on another unfinished story |
| **N**egotiable | Is the scope clear enough to test? | Vague "improve performance" |
| **V**aluable | Can we verify the business value? | No measurable outcome |
| **E**stimable | Can QA estimate test effort? | Unknown technical approach |
| **S**mall | Can this be tested in < 2 weeks? | Epic disguised as story |
| **T**estable | Can we write test cases now? | No acceptance criteria |

## Acceptance Criteria Quality

### Good Example
```
Given a user with role "admin"
When they access /api/users
Then they receive a 200 response with all users
And response time is < 200ms
```

### Issues to Flag

| Issue | Example | Fix |
|-------|---------|-----|
| Ambiguous | "Fast loading" | "Page loads in < 2s on 3G" |
| Unmeasurable | "User-friendly" | "Error message is < 100 chars" |
| Missing boundary | "Accept valid email" | Define valid format (RFC 5322) |
| No error case | "User can login" | Also "Invalid password shows error" |
| UI-only focus | "Button is green" | "Button meets WCAG contrast 3:1" |

## Output Format

```markdown
## Testability Review: [Story ID]

### Score: 7/10

### Issues
| # | Severity | Issue | Suggestion |
|---|----------|-------|------------|
| 1 | High | No error acceptance criteria | Add: "Invalid email returns 422 with message" |
| 2 | Medium | "Fast" is undefined | Change to: "< 500ms p95" |

### Questions for Product Owner
- What should happen if the email already exists?
- Is there a rate limit on resend attempts?

### Estimated Test Cases: 12
- Positive: 4
- Negative: 5
- Boundary: 3
```

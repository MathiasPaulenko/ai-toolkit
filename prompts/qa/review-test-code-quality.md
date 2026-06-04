---
name: Review Test Code Quality
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Review test code for quality issues: flakiness, poor assertions, over-mocking, test interdependence, and maintainability problems.
tags: [qa, test-review, code-quality, flakiness, assertions, mocking]
role: qa-engineer
model: any
trigger: When the user asks to review test code, check test quality, or identify flaky tests.
---

# Review Test Code Quality

Review test code for common quality issues that lead to flakiness, false confidence, or maintenance burden.

## Review Checklist

### Assertions
- [ ] Assertions are specific (exact value, not `is not None`)
- [ ] Error messages explain what failed
- [ ] No tautological assertions (`assertTrue(True)`)
- [ ] Multiple assertions only when testing one concept
- [ ] `assertAll` / soft assertions for grouped checks

### Mocking
- [ ] External dependencies mocked (DB, API, filesystem)
- [ ] Mocks verify behavior, not implementation internals
- [ ] No mocking the unit under test
- [ ] `spy` used instead of `mock` when partial behavior needed
- [ ] Factory methods used instead of raw `mock()`

### Independence
- [ ] No shared mutable state between tests
- [ ] No dependence on execution order
- [ ] Cleanup in teardown/fixtures
- [ ] Parallel-safe (`pytest -n auto` passes)

### Readability
- [ ] Test name describes behavior, not method name
- [ ] Arrange-Act-Assert structure visible
- [ ] No logic in tests (no if/for/switch)
- [ ] Magic values extracted to constants/fixtures

### Anti-Patterns to Flag

| Pattern | Problem | Fix |
|---------|---------|-----|
| `time.sleep()` | Flaky, slow | Explicit wait, synchronization |
| `random` in tests | Non-deterministic | Fixed seed or parameterize |
| Hardcoded IDs | Brittle | Generate IDs dynamically |
| `print` instead of assert | Manual verification | Add assertions |
| Commented-out tests | Rot | Delete or fix |
| `catch (Exception e)` | Swallows failures | Catch specific exceptions |
| Test everything via UI | Slow, brittle | Test logic at unit level |

## Output Format

```markdown
## Test Review: [File/PR]

### Issues Found
| Line | Severity | Issue | Suggestion |
|------|----------|-------|------------|
| 42 | High | `time.sleep(2)` | Use WebDriverWait explicit wait |
| 55 | Medium | Assertion too vague | Assert exact response code |

### Score
- Assertions: 7/10
- Independence: 9/10
- Readability: 6/10
- **Overall: 7.3/10**
```

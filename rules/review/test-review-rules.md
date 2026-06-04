---
name: Test Review Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Rules for reviewing test code. Covers coverage thresholds, assertion quality, mock usage, test independence, and anti-patterns.
tags: [testing, review, quality, coverage, assertions, mocks]
role: test-review-checklist
type: rules
language: en
---

# Test Review Rules

Use these rules when reviewing test code. A test suite is only as good as its weakest test.

## 1. Coverage Thresholds

- [ ] Business logic: **≥ 80%** line coverage
- [ ] Critical paths: **≥ 90%** line coverage
- [ ] Error handling paths: **≥ 60%** branch coverage
- [ ] Infrastructure/CRUD code: **≥ 50%** or covered by integration tests
- [ ] No untested public methods

## 2. Assertion Quality

- [ ] Assertions are **specific** (assert exact value, not just `not None`).
- [ ] Error messages include context (expected vs actual).
- [ ] Multiple assertions in one test only when testing one concept.
- [ ] Use `assertAll` / `soft assertions` for grouped validations.
- [ ] Avoid tautological assertions (`assertTrue(True)`).

```python
# Good
assert response.status_code == 201
assert response.json()["email"] == "test@example.com"

# Bad
assert response is not None
assert True
```

## 3. Mock Usage

- [ ] External dependencies (DB, API, filesystem) are mocked or isolated.
- [ ] Mocks verify behavior, not implementation details.
- [ ] `verify()` / `assert_called_with()` used appropriately.
- [ ] No mocking of the unit under test.
- [ ] `spy` used instead of `mock` when partial behavior needed.

```python
# Good — verify contract, not internals
mock_email_service.send_welcome.assert_called_once_with("test@example.com")

# Bad — asserting internal method calls
user_service._hash_password.assert_called_once()
```

## 4. Test Independence

- [ ] Tests do not depend on execution order.
- [ ] Tests clean up after themselves (fixtures, transactions).
- [ ] No shared mutable state between tests.
- [ ] Each test has its own data setup.
- [ ] Parallel execution safe (`pytest -n auto` passes).

## 5. Test Data

- [ ] Use factories/fixtures, not hardcoded data.
- [ ] Edge cases covered: empty, max length, special characters, null.
- [ ] Boundary values tested (0, 1, max-1, max, max+1).
- [ ] Realistic data mimics production (not `test1`, `test2`).

## 6. Test Naming

- [ ] Name describes behavior, not method being tested.
- [ ] Format: `test_{scenario}_{expected_result}` or `should_{expected}_when_{condition}`.

```python
# Good
def test_user_login_fails_with_invalid_password():

def should_return_404_when_user_does_not_exist():

# Bad
def test_login():
def test_user():
```

## 7. Test Structure

- [ ] Arrange-Act-Assert (AAA) structure visible.
- [ ] No logic in tests (no if/for/switch).
- [ ] One concept per test (single reason to fail).
- [ ] Setup extracted to fixtures/helpers.

```python
# Good
@pytest.fixture
def active_user():
    return UserFactory(is_active=True)

def test_deactivate_user_sets_inactive(active_user):
    # Arrange
    service = UserService()
    
    # Act
    service.deactivate(active_user.id)
    
    # Assert
    assert active_user.is_active is False
```

## 8. Anti-Patterns to Reject

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| `Thread.sleep` in tests | Flaky, slow | Use explicit waits or synchronization |
| `System.out.println` | Noise, manual verification | Replace with assertions |
| Commented-out tests | Rot, confusion | Delete or fix |
| Tests without assertions | False positives | Add meaningful assertions |
| Mocking value objects | Over-mocking | Use real objects |
| Testing private methods | Brittle | Test public behavior |
| `expected = Exception.class` without message check | Catches wrong exception | Verify exception message/type |
| Database state leaking | Intermittent failures | Use transactions or cleanup |

## 9. Integration Test Rules

- [ ] Use TestContainers for real dependencies (DB, Kafka, Redis).
- [ ] Test happy path and at least one error path per endpoint.
- [ ] Verify response schema matches contract (OpenAPI).
- [ ] Reset state between tests (clean tables, reset mocks).

## 10. E2E Test Rules

- [ ] Cover critical user journeys only (not everything).
- [ ] Use Page Object Model for UI selectors.
- [ ] Run against staging, not production.
- [ ] Idempotent (can rerun without manual cleanup).
- [ ] Screenshots/videos on failure.

## Review Decision

| Result | Criteria |
|--------|----------|
| **Approve** | All rules satisfied, coverage thresholds met |
| **Request Changes** | Missing tests, low coverage, flaky tests, poor assertions |
| **Block** | Tests do not cover the change, or test code has security risks |

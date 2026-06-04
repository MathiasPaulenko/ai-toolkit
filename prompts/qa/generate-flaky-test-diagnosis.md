---
name: Generate Flaky Test Diagnosis
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Diagnose and fix flaky tests by analyzing timing issues, async races, test isolation, environment dependencies, and non-deterministic data.
tags: [qa, flaky-tests, debugging, timing, async, stability]
role: qa-engineer
model: any
trigger: When the user asks about flaky tests, intermittent failures, test stability, or non-deterministic test behavior.
---

# Generate Flaky Test Diagnosis

Diagnose and fix flaky tests systematically.

## Diagnostic Framework

### 1. Reproduction
- [ ] Run test in isolation 100 times: `pytest --count=100`
- [ ] Run full suite 10 times (isolation vs. interaction)
- [ ] Run on different machines/CI agents
- [ ] Run with random seed variations

### 2. Root Cause Categories

| Category | Symptom | Fix |
|----------|---------|-----|
| **Timing** | Fails only on slow CI | Explicit waits, not `sleep` |
| **Async** | Race between operations | `await`, callbacks, polling |
| **Isolation** | Passes alone, fails in suite | Reset state, unique IDs |
| **Order** | Depends on execution order | Independent setup/teardown |
| **Data** | Non-deterministic DB state | Transaction rollback, factories |
| **External** | Depends on API/service | Mock or stub consistently |
| **Time** | Fails near midnight, month-end | Freeze time (time-machine) |

### 3. Common Fixes

#### Timing Issues (UI Tests)
```python
# Bad
import time
time.sleep(2)

# Good
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.ID, "submit")))
```

#### Async Race Conditions
```python
# Bad
async_operation()
assert result == expected  # May not be ready

# Good
await async_operation()
# Or poll
for _ in range(10):
    if check_result(): break
    time.sleep(0.1)
```

#### Test Isolation
```python
# Bad: shared counter
COUNTER += 1

# Good: fixture with cleanup
@pytest.fixture
def unique_user():
    user = create_user(email=f"test_{uuid4()}@example.com")
    yield user
    delete_user(user.id)
```

#### Time-Dependent Tests
```python
from freezegun import freeze_time

@freeze_time("2024-06-01")
def test_monthly_report():
    assert generate_report().month == 6
```

## Prevention Checklist

- [ ] All tests run in random order (`pytest-randomly`)
- [ ] No `time.sleep()` in tests
- [ ] Unique identifiers for all created resources
- [ ] Database transactions roll back after each test
- [ ] External services mocked consistently
- [ ] CI runs tests 3 times to catch flakiness early
- [ ] Flaky test quarantine process (skip + ticket)

## Quarantine Process

1. Identify flaky test (fails > 5% of runs)
2. Mark with `@pytest.mark.skip(reason="FLAKY-123")`
3. Create ticket FLAKY-123
4. Fix within 1 sprint
5. Re-enable and monitor for 1 week

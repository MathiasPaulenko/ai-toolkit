---
name: Test Automation Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Rules for writing maintainable, reliable, and fast test automation. Covers Page Object Model, stable selectors, waits, assertions, and CI/CD integration.
tags: [test-automation, e2e, qa, review, selectors]
role: qa-automation-rules
type: rules
language: en
---

# Test Automation Rules

## 1. Page Object Model (POM)

### Rule 1.1: Encapsulate Selectors
- All locators must live in Page Object classes, never in tests.
- Page Objects expose methods that describe user actions, not DOM queries.

```python
# Good
login_page.login("user", "pass")

# Bad
page.find_element("#username").send_keys("user")
page.find_element("#password").send_keys("pass")
page.find_element("#submit").click()
```

### Rule 1.2: Single Responsibility per Page Object
- One Page Object per page or major component.
- Sub-components (modals, navbars) get their own Page Objects.

## 2. Selectors

### Rule 2.1: Prefer Semantic Locators
Priority order:
1. `data-testid` (stable, dev-controlled)
2. Accessible attributes: `role`, `label`, `placeholder`, `alt`
3. Text content (if static and not i18n)
4. CSS class or ID (if contractually stable)
5. XPath or complex CSS (last resort, document why)

```python
# Good
page.get_by_role("button", name="Submit")
page.get_by_test_id("checkout-form")

# Bad
page.find_element(".btn-primary:nth-child(3)")
page.find_element("//div[@class='wrapper']/span[2]")
```

### Rule 2.2: No Dynamic Indices
- Never use `nth-child`, `eq()`, or array indices in selectors.
- If order matters, add stable identifiers to the DOM.

## 3. Waits & Synchronization

### Rule 3.1: Explicit Waits Only
- Never use `sleep()` or implicit waits.
- Use framework-native waits for conditions: visibility, clickability, text present.

```python
# Good
wait.until(EC.element_to_be_clickable((By.ID, "submit")))

# Bad
import time
time.sleep(3)
```

### Rule 3.2: Wait for State, Not Time
- Wait for the condition that indicates the action is safe, not an arbitrary duration.

```python
# Good
wait.until(EC.presence_of_element_located((By.ID, "results")))

# Bad
wait(5)  # Maybe results are already there
```

## 4. Test Data

### Rule 4.1: Generate or Isolate Test Data
- Each test must create or use isolated data.
- Never share mutable state between tests.

```python
# Good
@pytest.fixture
def new_user():
    return create_user(email=f"test-{uuid4()}@example.com")

# Bad
TEST_USER = User.objects.get(id=1)  # Shared state
```

### Rule 4.2: Clean Up After Tests
- Delete created data in teardown or use transactional fixtures.
- Leave environment in known state for next test.

## 5. Assertions

### Rule 5.1: One Concept per Test
- Each test verifies one behavior or user journey step.
- Avoid mega-tests that assert 10 different things.

### Rule 5.2: Assert on User-Visible Outcomes
- Prefer assertions on UI state, URL, or API response over internal implementation.

```python
# Good
assert page.url == "/dashboard"
assert page.get_by_text("Welcome, Alice").is_visible()

# Bad
assert db.query("SELECT role FROM users WHERE id=1") == "admin"
```

## 6. CI/CD Integration

### Rule 6.1: Fast Feedback Loop
- Smoke tests must run in under 5 minutes.
- Full suite should not exceed 30 minutes.
- Parallelize by file or by browser.

### Rule 6.2: Fail Fast
- `--maxfail=3` or equivalent to abort on repeated failures.
- Prevents wasting CI minutes when environment is broken.

### Rule 6.3: Artifact Retention
- Screenshot, video, and trace artifacts must be uploaded on failure.
- Retain for 7-14 days, not indefinitely.

## 7. Maintainability

### Rule 7.1: No Hardcoded URLs
- Use environment variables or config files for base URLs.
- Same test must run against local, staging, and production.

### Rule 7.2: No Hardcoded Credentials
- Use secrets management or test-specific accounts.
- Never commit passwords or API keys.

### Rule 7.3: Document Flaky Tests
- If a test is temporarily flaky, annotate with `@flaky` and ticket number.
- Fix within one sprint; do not accumulate skipped tests.

## 8. Performance

### Rule 8.1: Limit Browser Instances
- Reuse browser context or session where isolation allows.
- Login once per worker, not once per test.

### Rule 8.2: Headless in CI
- Run headless in CI unless debugging a specific failure.
- Local development can use headed mode for visibility.

## Checklist

- [ ] Page Objects used for all major pages
- [ ] Selectors use `data-testid` or accessible attributes
- [ ] No `sleep()` calls in test code
- [ ] Test data isolated per test
- [ ] Assertions on user-visible outcomes
- [ ] CI runs under 30 minutes with artifacts
- [ ] No hardcoded URLs or credentials

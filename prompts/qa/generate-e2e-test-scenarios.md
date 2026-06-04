---
name: Generate E2E Test Scenarios
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate end-to-end test scenarios for critical user journeys. Covers login, checkout, onboarding, and multi-step workflows with Page Object Model structure.
tags: [qa, e2e, playwright, cypress, selenium, user-journey]
role: qa-engineer
model: any
trigger: When the user asks for E2E tests, user journey tests, or critical path testing.
---

# Generate E2E Test Scenarios

Given a user story or feature description, generate complete E2E test scenarios using Page Object Model (POM) pattern.

## Coverage

- Critical user journeys (login → dashboard → action → logout)
- Error recovery paths
- Form submissions with validation
- File uploads/downloads
- Search and filter workflows
- Payment/checkout flows
- Multi-role interactions (admin vs customer)

## Output Structure

```
tests/e2e/
  pages/
    login_page.py
    dashboard_page.py
  fixtures/
    users.py
  scenarios/
    test_login_flow.py
    test_checkout_flow.py
```

## Example (Playwright + Python)

```python
# tests/e2e/pages/login_page.py
from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator("[data-testid='email']")
        self.password_input = page.locator("[data-testid='password']")
        self.submit_button = page.locator("[data-testid='login-btn']")
        self.error_message = page.locator("[data-testid='error']")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

# tests/e2e/scenarios/test_login_flow.py
from pages.login_page import LoginPage

def test_successful_login(page):
    login = LoginPage(page)
    page.goto("/login")
    login.login("alice@example.com", "password123")
    assert page.url.endswith("/dashboard")

def test_invalid_credentials_shows_error(page):
    login = LoginPage(page)
    page.goto("/login")
    login.login("alice@example.com", "wrongpass")
    assert login.error_message.is_visible()
```

## Best Practices Enforced

- Use `data-testid` attributes for selectors (no CSS class dependency)
- Independent tests (no shared mutable state)
- Screenshots on failure
- Video recording for flaky tests
- Parallel execution safe

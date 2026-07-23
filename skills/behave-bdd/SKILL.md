---
name: behave-bdd
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Production-grade skill for BDD testing with Python Behave (v1.3.0+). Covers Gherkin, step implementations, environment hooks, fixtures, tags, data tables, scenario outlines, formatters, and CI/CD integration.
tags: [behave, bdd, python, testing, gherkin, e2e, cucumber]
trigger: When the user asks to create, update, fix, or explain Behave BDD tests, feature files, step definitions, environment.py, fixtures, tags, or any BDD-related workflow in Python.
min_version: 1.3.0
---

# Behave BDD Skill

## Description

This skill provides comprehensive guidance for Behavior-Driven Development (BDD) using the Python `behave` framework (version 1.3.0 and above). It covers everything from writing Gherkin feature files to production-grade step implementations, environment hooks, fixtures, tag expressions, data tables, scenario outlines, custom formatters, and CI/CD integration.

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Gherkin Feature Files](#2-gherkin-feature-files)
3. [Step Implementations](#3-step-implementations)
4. [Environment Hooks](#4-environment-hooks)
5. [Page Object Model](#5-page-object-model)
6. [Fixtures](#6-fixtures)
7. [Tags and Tag Expressions](#7-tags-and-tag-expressions)
8. [The Context Object](#8-the-context-object)
9. [Formatters and Reporters](#9-formatters-and-reporters)
10. [Configuration and CLI](#10-configuration-and-cli)
11. [Logging and Output Capture](#11-logging-and-output-capture)
12. [Debugging](#12-debugging)
13. [CI/CD Integration](#13-cicd-integration)
14. [Best Practices Checklist](#14-best-practices-checklist)
15. [Common Pitfalls](#15-common-pitfalls)
16. [References](#16-references)

## When to Invoke

- Creating or refactoring BDD tests for a Python project
- Writing Gherkin feature files with proper syntax and best practices
- Implementing Python step definitions with parameters, type conversion, shared state, and step composition (`execute_steps`)
- Configuring `environment.py` hooks for setup/teardown (browsers, DB, APIs)
- Using **Page Object Model (POM)** to decouple UI selectors from step definitions
- Using fixtures for reusable test components and resource management
- Applying tags and tag expressions to control test execution
- Working with data tables, scenario outlines, and backgrounds
- Generating reports (JSON, JUnit XML) and integrating with CI/CD
- Debugging failing behave tests or interpreting behave output

---

## 1. Project Setup

### Directory Layout

```
project/
  features/
    __init__.py          # Optional: makes features a package
    environment.py       # Setup / teardown hooks
    fixtures.py          # Reusable fixtures (optional)
    *.feature            # Gherkin feature files
    steps/
      __init__.py        # Optional
      *_steps.py         # Step definition modules
  behave.ini             # Configuration file (optional but recommended)
  setup.cfg              # Alternative config location
```

### Installation

```bash
pip install "behave>=1.3.0"

# Optional: for colored output and parse expressions
pip install behave[formatters] behave[parse]

# For web testing (Selenium example)
pip install selenium webdriver-manager
```

### behave.ini

```ini
[behave]
format = pretty
tags = ~@wip
stdout_capture = true
stderr_capture = true
log_capture = true
logging_level = INFO
colors = true
```

### setup.cfg (alternative config)

```ini
[behave]
format = pretty
tags = not @wip
paths = features/
stdout_capture = true
stderr_capture = true
```

### Project Template

See `references/project-template/` for a ready-to-copy bootstrap structure with `behave.ini`, `environment.py`, `steps/__init__.py`, and an example feature.

---

## 2. Gherkin Feature Files

### Basic Structure

```gherkin
Feature: User Authentication
  As a registered user
  I want to log into the application
  So that I can access my personal dashboard

  Background:
    Given the database has been seeded with default users

  @smoke @critical
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter "user@test.com" as email
    And I enter "password123" as password
    And I click the login button
    Then I should be redirected to the dashboard
    And the welcome message should contain "Hello, User"

  @regression
  Scenario: Login fails with invalid credentials
    Given I am on the login page
    When I enter "wrong@test.com" as email
    And I enter "wrongpass" as password
    And I click the login button
    Then I should see an error message "Invalid credentials"
    And the login form should still be visible
```

### Scenario Outline with Examples

```gherkin
  @data-driven
  Scenario Outline: Login with various user roles
    Given I am on the login page
    When I enter "<email>" as email
    And I enter "<password>" as password
    And I click the login button
    Then I should be redirected to "<expected_page>"
    And my role should be "<role>"

    Examples: Valid users
      | email          | password | expected_page | role  |
      | admin@test.com | admin123 | /admin        | admin |
      | user@test.com  | user123  | /dashboard    | user  |

    Examples: Invalid users
      | email        | password | expected_page | role |
      | bad@test.com | wrong    | /login        | none |
```

### Data Tables

```gherkin
  Scenario: Add multiple items to cart
    Given I have the following products in inventory:
      | sku   | name      | price | stock |
      | A1001 | Mouse     | 25.00 | 100   |
      | A1002 | Keyboard  | 75.00 | 50    |
      | A1003 | Monitor   | 299.99| 20    |
    When I add the following items to my cart:
      | sku   | qty |
      | A1001 | 2   |
      | A1002 | 1   |
    Then my cart total should be 125.00
    And the inventory should be updated:
      | sku   | remaining |
      | A1001 | 98        |
      | A1002 | 49        |
```

### Tags

```gherkin
  @slow @integration @db-required
  Scenario: Process large batch order
```

### Doc Strings (Multiline Text)

```gherkin
  Scenario: Submit contact form
    Given I am on the contact page
    When I fill in the message with:
      """
      Dear Support,
      I am experiencing issues with my account.
      Please contact me as soon as possible.
      Regards,
      John Doe
      """
    And I submit the form
    Then I should see a confirmation "Message sent successfully"
```

---

## 3. Step Implementations

### Decorators

```python
from behave import given, when, then, step
from behave.api.async_step import async_run_until_complete  # For async steps

@given('I am on the login page')
def step_on_login_page(context):
    context.browser.get(f"{context.base_url}/login")

@when('I enter "{text}" as email')
def step_enter_email(context, text):
    context.browser.find_element(context.by.ID, 'email').send_keys(text)

@then('I should be redirected to the dashboard')
def step_redirected_to_dashboard(context):
    assert '/dashboard' in context.browser.current_url
```

### Step Parameters with Parse

```python
from parse import with_pattern
from behave import register_type

@with_pattern(r'\d+[,.]?\d*')
def parse_number(text):
    return float(text.replace(',', ''))

register_type(Number=parse_number)

@when('I add {amount:Number} items to cart')
def step_add_items(context, amount):
    context.cart.add_items(int(amount))
```

### Step Parameters with Regular Expressions

```python
from behave import use_step_matcher

use_step_matcher('re')

@when(r'I wait (?P<seconds>\d+) seconds?')
def step_wait(context, seconds):
    import time
    time.sleep(int(seconds))

# Switch back to default parse matcher
use_step_matcher('parse')
```

### Step Parameters with Cucumber Expressions (cfparse)

```python
from cfparse import parameter_cfparse

use_step_matcher('cfparse')

@when('I have {count:d} items in my cart')
def step_count_items(context, count):
    assert context.cart.count() == count
```

### Shared / Common Steps

```python
# features/steps/common_steps.py
from behave import given, when, then

@given('the database has been seeded with default users')
def step_seed_database(context):
    context.db.seed_users()
```

### Step Composition with `execute_steps()`

Call existing steps from within another step to avoid duplication:

```python
@given('I am logged in as an admin')
def step_logged_in_as_admin(context):
    context.execute_steps('''
        Given I am on the login page
        When I enter "admin@test.com" as email
        And I enter "admin123" as password
        And I click the login button
    ''')
    assert context.browser.current_url.endswith('/admin')
```

Use sparingly â€” prefer helper functions for shared logic. `execute_steps` is best for reusing **Given** sequences in integration/E2E tests.

### `@capture` Decorator (per-step capture control)

Disable stdout/stderr capture for a single step without toggling global config:

```python
from behave import capture

@when('I run a shell command and need immediate output')
@capture(False)
def step_shell_command(context):
    import subprocess
    result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
    print(result.stdout)  # Printed immediately, not buffered
```

### Assert Helpers with Hamcrest / AssertPy

Use expressive matchers for readable failure messages:

```python
# pip install PyHamcrest
from hamcrest import assert_that, equal_to, contains_string, has_length

@then('the cart should contain {count:d} items')
def step_cart_count(context, count):
    assert_that(context.cart.count(), equal_to(count))

@then('the page title should contain "{text}"')
def step_title_contains(context, text):
    assert_that(context.browser.title, contains_string(text))

# Or with assertpy (pip install assertpy)
from assertpy import assert_that as assertpy_that

@then('the response list should have {count:d} elements')
def step_list_count(context, count):
    assertpy_that(context.response).is_length(count)
```

### Accessing Data Tables

```python
@when('I add the following items to my cart')
def step_add_multiple_items(context):
    for row in context.table:
        sku = row['sku']
        qty = int(row['qty'])
        context.cart.add(sku, qty)

@then('the inventory should be updated')
def step_inventory_updated(context):
    for row in context.table:
        sku = row['sku']
        expected = int(row['remaining'])
        actual = context.inventory.stock(sku)
        assert actual == expected, f"Expected {expected} for {sku}, got {actual}"
```

### Doc Strings

```python
@when('I fill in the message with')
def step_fill_message(context):
    message = context.text  # multiline string from Doc String
    context.browser.find_element('id', 'message').send_keys(message)
```

### Async Steps (behave 1.2.6+)

```python
from behave.api.async_step import async_run_until_complete
import asyncio

@when('I async fetch user data')
@async_run_until_complete
async def step_async_fetch(context):
    context.user_data = await context.api.get_user()
```

---

## 4. Environment Hooks (environment.py)

### Full Hook Reference

```python
# features/environment.py
import os

# -- HOOKS ORDER: before_all -> before_feature -> before_scenario -> before_step
#                  after_step -> after_scenario -> after_feature -> after_all

def before_all(context):
    """Runs once before any feature is executed."""
    context.base_url = os.environ.get('BASE_URL', 'http://localhost:8000')
    context.test_outputs_dir = 'test_outputs'
    os.makedirs(context.test_outputs_dir, exist_ok=True)

def after_all(context):
    """Runs once after all features have completed."""
    if hasattr(context, 'db'):
        context.db.close()

def before_feature(context, feature):
    """Runs before each feature."""
    context.feature_tags = feature.tags

def after_feature(context, feature):
    """Runs after each feature."""
    pass

def before_scenario(context, scenario):
    """Runs before each scenario."""
    # Web driver example
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    options = Options()
    options.add_argument('--headless')
    context.browser = webdriver.Chrome(options=options)
    context.by = By  # Store for step usage
    context.browser.implicitly_wait(10)

def after_scenario(context, scenario):
    """Runs after each scenario."""
    # Screenshot on failure
    if scenario.status == 'failed':
        screenshot_path = f"{context.test_outputs_dir}/{scenario.name.replace(' ', '_')}.png"
        context.browser.save_screenshot(screenshot_path)
    context.browser.quit()

def before_step(context, step):
    """Runs before each step."""
    pass

def after_step(context, step):
    """Runs after each step."""
    pass

def before_tag(context, tag):
    """Runs before a scenario/feature with the given tag."""
    if tag == 'db-required':
        context.db = DatabaseConnection()

def after_tag(context, tag):
    """Runs after a scenario/feature with the given tag."""
    if tag == 'db-required':
        context.db.rollback()
        context.db.close()
```

---

## 5. Page Object Model (POM)

When testing web applications with Selenium, **never** put CSS selectors or XPath inside step definitions. Decouple UI locators from BDD steps using the Page Object Model.

### Directory Layout

```
features/
  pages/
    __init__.py
    base_page.py
    login_page.py
    dashboard_page.py
  steps/
    login_steps.py
```

### BasePage

```python
# features/pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, base_url=''):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def find(self, locator):
        return self.driver.find_element(*locator)

    def wait_for(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def open(self, path):
        self.driver.get(self.base_url + path)
```

### LoginPage

```python
# features/pages/login_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, 'email')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.error')

    def open(self):
        super().open('/login')
        return self

    def enter_email(self, email):
        self.find(self.EMAIL_INPUT).send_keys(email)
        return self

    def enter_password(self, password):
        self.find(self.PASSWORD_INPUT).send_keys(password)
        return self

    def click_login(self):
        self.find(self.LOGIN_BUTTON).click()
        return self

    def get_error_message(self):
        return self.wait_for(self.ERROR_MESSAGE).text
```

### Steps Using POM

```python
# features/steps/login_steps.py
from behave import given, when, then
from features.pages.login_page import LoginPage

@given('I am on the login page')
def step_on_login_page(context):
    context.login_page = LoginPage(context.browser, context.base_url)
    context.login_page.open()

@when('I enter "{email}" as email')
def step_enter_email(context, email):
    context.login_page.enter_email(email)

@when('I enter "{password}" as password')
def step_enter_password(context, password):
    context.login_page.enter_password(password)

@when('I click the login button')
def step_click_login(context):
    context.login_page.click_login()

@then('I should see an error message "{msg}"')
def step_see_error(context, msg):
    actual = context.login_page.get_error_message()
    assert msg in actual, f"Expected '{msg}' in error message, got '{actual}'"
```

### POM Best Practices

- **One class per page/screen**, not per feature.
- **Locators are constants** (`UPPER_CASE`) at the top of the page class.
- **Fluent interface** (`return self`) allows chaining in complex scenarios.
- **Waits belong in Page classes**, not in steps.
- **Assertions belong in steps**, not in pages.

---

## 6. Fixtures

### Defining Fixtures (behave 1.2.6+)

```python
# features/fixtures.py
from behave import fixture
import tempfile
import shutil

@fixture
def temp_directory(context):
    """Provides a temporary directory for the scenario."""
    path = tempfile.mkdtemp()
    context.temp_dir = path
    yield path
    shutil.rmtree(path)

@fixture
def database_transaction(context):
    """Wraps each scenario in a DB transaction and rolls back."""
    connection = context.db_connection
    transaction = connection.begin()
    yield connection
    transaction.rollback()
```

### Using Fixtures in environment.py

```python
from behave import use_fixture
from features.fixtures import temp_directory, database_transaction

def before_scenario(context, scenario):
    use_fixture(temp_directory, context)
    if 'db' in scenario.tags:
        use_fixture(database_transaction, context)
```

### Using Fixtures in Steps

```python
from behave import use_fixture
from features.fixtures import temp_directory

@given('I have a temporary workspace')
def step_temp_workspace(context):
    use_fixture(temp_directory, context)
```

### Named Fixtures

```python
from behave import fixture

@fixture(name='fresh_db')
def database_fixture(context):
    """Provides an isolated DB per scenario."""
    db = create_isolated_db()
    context.db = db
    yield db
    db.destroy()

# Usage
use_fixture('fresh_db', context)
```

---

## 7. Tags and Tag Expressions

### Tag Syntax in Gherkin

```gherkin
@wip @slow @integration
Feature: Heavy processing
```

### Running with Tags

```bash
# Single tag
behave --tags=@smoke

# Multiple tags (AND)
behave --tags=@smoke --tags=@critical

# Tag expressions v2 (behave 1.3.0+)
behave --tags="@smoke and not @wip"
behave --tags="(@fast or @smoke) and not @slow"
behave --tags="@integration and @db-required"

# Using behave.ini
[behave]
tags = not @wip
```

### Tag Expression Reference (v2)

| Expression | Meaning |
|-----------|---------|
| `@a and @b` | Both tags present |
| `@a or @b` | At least one tag present |
| `not @a` | Tag not present |
| `(@a or @b) and not @c` | Grouped logic |

---

## 8. The Context Object

### Context Attributes and Behaviors

```python
# context is shared across all steps in a scenario
# It is reset for each scenario (fresh instance)

# Setting attributes (any step)
context.user_id = 123
context.config      # behave configuration
context.feature     # current Feature object
context.scenario    # current Scenario object
context.tags        # combined tags of feature + scenario
context.failed      # True if any step failed
context.aborted     # True if scenario was aborted
context.table       # DataTable from last step (if any)
context.text        # DocString from last step (if any)
```

### `context.config.userdata` and `--define`

Pass runtime values from CLI into steps without hardcoding:

```bash
behave -D browser=firefox -D headless=true
```

```python
# In environment.py or steps
browser = context.config.userdata.get('browser', 'chrome')
headless = context.config.userdata.get('headless', 'false').lower() == 'true'
```

Useful for CI matrix builds (different browsers, endpoints, environments).

### Custom Context Class (Advanced)

```python
# features/environment.py
from behave.runner import Context

class CustomContext(Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_data = {}

# In behave.ini or CLI: --runner-class=features.environment:CustomContext
```

---

## 9. Formatters and Reporters

### Built-in Formatters

```bash
behave --format=pretty        # Default, human-readable
behave --format=json          # JSON output
behave --format=junit         # JUnit XML for CI/CD
behave --format=rerun         # Outputs failed scenarios for rerun
```

### Output to File

```bash
behave --format=json --outfile=reports/behave.json
behave --format=junit --outfile=reports/junit.xml
```

For the full formatter list, JSON report schema, and a custom formatter template, see `references/api-reference.md` and `references/formatter-template.py`.

---

## 10. Configuration and CLI

### Common CLI Commands

```bash
behave features/                        # Run all features
behave --tags=@smoke                    # Filter by tags
behave --dry-run                        # Validate without executing
behave --stop                           # Fail fast
behave --steps-catalog                  # List available steps
behave -D browser=firefox               # Pass userdata
```

### behave.ini Example

```ini
[behave]
format = pretty
tags = not @wip
stdout_capture = true
stderr_capture = true
log_capture = true
logging_level = INFO
colors = true
```

For the full CLI reference with all flags and a complete behave.ini, see `references/api-reference.md`.

---

## 10. Logging and Output Capture

### Controlling Capture

```python
# In step, disable capture temporarily to debug
import logging

logger = logging.getLogger(__name__)

@when('I debug this step')
def step_debug(context):
    logger.info("This is captured and shown on failure")
    print("This is also captured by default")
    
    # To bypass capture and print immediately:
    context.config.stdout_capture = False
    print("IMMEDIATE OUTPUT")
    context.config.stdout_capture = True
```

### behave.ini Logging Options

```ini
[behave]
log_capture = true
logging_level = DEBUG
logging_format = %(asctime)s %(levelname)s %(name)s %(message)s
log_date_format = %Y-%m-%d %H:%M:%S
```

---

## 11. Debugging

### Debug-on-Error

```bash
behave --stop --verbose
```

### Interactive Debugger (pdb/ipdb)

```python
import ipdb

@when('something complicated happens')
def step_complicated(context):
    result = complex_operation()
    if not result:
        ipdb.set_trace()  # Break here in test run
```

### Using behave --dry-run

```bash
# Validates Gherkin syntax and step matching without executing
behave --dry-run --verbose
```

---

## 12. CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/behave.yml
name: BDD Tests

on: [push, pull_request]

jobs:
  behave:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: behave --format=json --outfile=reports/behave.json
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: behave-reports
          path: reports/
```

### Makefile Target

```makefile
.PHONY: bdd bdd-smoke bdd-report

bdd:
	behave features/

bdd-smoke:
	behave --tags=@smoke features/

bdd-report:
	mkdir -p reports
	behave --format=json --outfile=reports/behave.json
	behave --format=junit --junit-directory=reports/
```

---

## 13. Best Practices Checklist

- [ ] Feature files are written in business language, not technical implementation
- [ ] Each scenario is independent (no state leakage between scenarios)
- [ ] Background is used only for truly common preconditions
- [ ] Step definitions are reusable and not duplicated
- [ ] **Page Object Model** decouples UI selectors from step definitions
- [ ] Type converters are registered for domain-specific types
- [ ] `environment.py` handles all setup/teardown; no external state in steps
- [ ] Tags are used to categorize by speed, layer (unit, integration, e2e), and scope
- [ ] Fixtures are used for complex resource management (DB, browsers, temp files)
- [ ] Screenshots / logs are captured on failure for debugging
- [ ] CI pipeline runs behave with `--stop` to fail fast and reports in JSON/JUnit
- [ ] `behave.ini` is committed; local overrides use `.behaverc` or env vars
- [ ] Scenario Outlines use meaningful `Examples` names
- [ ] Data tables have headers; steps iterate cleanly over rows
- [ ] Doc strings are used for large text input (emails, JSON, XML)
- [ ] Async steps use `@async_run_until_complete` for async/await code
- [ ] Hamcrest / AssertPy matchers provide clear failure messages
- [ ] `execute_steps` composes common **Given** sequences sparingly
- [ ] `context.config.userdata` parametrizes tests for CI matrix builds
- [ ] `--steps-catalog` is checked before adding duplicate step definitions

---

## 14. Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| `Step undefined` | Missing step definition or typo | Check spelling; use `behave --dry-run` and `behave --steps-catalog` |
| `Ambiguous step` | Two step definitions match same text | Use more specific regex or parse patterns |
| Scenario state leaks | Mutable default args or class-level state | Reset state in `before_scenario`; use fixtures |
| Slow tests | Browser started/stopped per step | Move browser lifecycle to `before_scenario`/`after_scenario` |
| Tags not filtering | Wrong tag expression syntax | Use v2 syntax with quotes: `--tags="@a and not @b"` |
| Missing context attr | Attribute set in wrong hook scope | Check hook execution order |
| Capture hides prints | stdout_capture enabled | Use `--no-capture` or logger |
| Selectors in steps | Hardcoded XPath/CSS in step definitions | Use **Page Object Model**; locators belong in page classes |
| Duplicated Given logic | Copy-paste across scenarios | Extract helper or use `execute_steps` for shared sequences |
| Brittle assertions | Raw `assert` without context | Use Hamcrest/AssertPy for descriptive failure messages |

---

## 15. References

- [Behave Documentation](https://behave.readthedocs.io/)
- [Gherkin Reference](https://cucumber.io/docs/gherkin/)
- [BDD Best Practices](https://cucumber.io/docs/bdd/)
- Related skills: `appium-skill`, `playwright-best-practices`, `selenium-automation`

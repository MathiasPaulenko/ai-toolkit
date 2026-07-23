---
name: robot-framework
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Production-grade skill for Robot Framework keyword-driven testing. Covers project structure, keywords, variables, libraries (Selenium, Requests, Database), resources, setup/teardown, tags, CLI execution, and CI/CD integration.
tags: [robot-framework, testing, keyword-driven, automation, qa, selenium]
trigger: When the user asks to create, refactor, fix, or explain Robot Framework tests, keywords, variables, resources, libraries, or project structure.
---

# Robot Framework Skill

## Description

Comprehensive skill for Robot Framework, the leading keyword-driven test automation framework in Python. Covers project structure, custom and built-in keywords, variable scopes, resource and variable files, library integration (Selenium, Requests, Database), setup/teardown patterns, tag-based execution, command-line options, and CI/CD integration.

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Test Case Syntax](#2-test-case-syntax)
3. [Keywords](#3-keywords)
4. [Variables](#4-variables)
5. [Libraries](#5-libraries)
6. [Resource & Variable Files](#6-resource--variable-files)
7. [Setup & Teardown](#7-setup--teardown)
8. [Tags](#8-tags)
9. [Execution & CLI](#9-execution--cli)
10. [CI/CD Integration](#10-cicd-integration)
11. [Best Practices Checklist](#11-best-practices-checklist)
12. [Common Pitfalls](#12-common-pitfalls)
13. [References](#13-references)

## When to Invoke

- Creating or refactoring a Robot Framework test suite
- Writing keyword-driven tests for web, API, or database validation
- Structuring a Robot Framework project with resources and libraries
- Implementing custom keywords in Python or Robot syntax
- Managing variables across different scopes (test, suite, global)
- Integrating SeleniumLibrary, RequestsLibrary, or DatabaseLibrary
- Configuring setup/teardown at test, suite, or global level
- Using tags to organize and filter test execution
- Running tests via CLI with custom options and listeners
- Integrating Robot Framework into Jenkins, GitHub Actions, or GitLab CI

---

## 1. Project Setup

### Directory Layout

```
robot-project/
  tests/
    api/
      login_api.robot
      users_api.robot
    ui/
      login_ui.robot
      checkout_ui.robot
  resources/
    keywords/
      common.robot
      api_keywords.robot
      ui_keywords.robot
    pages/
      login_page.robot
      home_page.robot
    variables/
      global_variables.py
      test_data.yaml
    locators/
      login_locators.yaml
  libraries/
    CustomLibrary.py
  config/
    environments.yaml
  results/
  requirements.txt
  run.sh
```

### requirements.txt

```
robotframework>=6.1.0
robotframework-seleniumlibrary>=6.1.0
robotframework-requests>=0.9.5
robotframework-databaselibrary>=1.3.0
robotframework-pabot>=2.15.0
```

### Installation

```bash
pip install -r requirements.txt
```

---

## 2. Test Case Syntax

### Basic Structure

```robot
*** Settings ***
Documentation    Test suite for user login functionality
Resource         ../resources/keywords/common.robot
Test Setup       Open Browser To Login Page
Test Teardown    Close Browser

*** Test Cases ***
Valid Login
    [Documentation]    Verify that a valid user can log in successfully
    [Tags]    smoke    regression    api
    Input Username    ${VALID_USER}
    Input Password    ${VALID_PASSWORD}
    Click Login Button
    Welcome Page Should Be Open

Invalid Login With Wrong Password
    [Documentation]    Verify login fails with incorrect password
    [Tags]    regression    negative
    Input Username    ${VALID_USER}
    Input Password    wrongpassword
    Click Login Button
    Error Message Should Be Visible    Invalid credentials
```

### BDD-Style Syntax

```robot
*** Test Cases ***
User Can Add Item To Cart
    Given User Is Logged In
    When User Adds Product "Headphones" To Cart
    Then Cart Should Contain "Headphones"
    And Cart Total Should Be "$99.99"
```

---

## 3. Keywords

### Built-in Keywords

```robot
*** Test Cases ***
Built-in Examples
    ${result} =    Evaluate    2 + 2
    Should Be Equal As Numbers    ${result}    4

    ${list} =    Create List    apple    banana    cherry
    Should Contain    ${list}    banana

    ${dict} =    Create Dictionary    name=John    age=30
    Dictionary Should Contain Key    ${dict}    name

    Run Keyword If    ${result} > 3    Log    Result is greater than 3
    Run Keyword Unless    ${result} == 4    Fail    Unexpected result

    Wait Until Keyword Succeeds    5x    1s    Check Element Is Visible    id:submit
```

### User-Defined Keywords (Robot Syntax)

```robot
*** Keywords ***
Input Username
    [Arguments]    ${username}
    [Documentation]    Enters the given username into the username field
    Wait Until Element Is Visible    ${LOGIN.USERNAME_FIELD}
    Input Text    ${LOGIN.USERNAME_FIELD}    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    ${LOGIN.PASSWORD_FIELD}    ${password}

Click Login Button
    Click Button    ${LOGIN.SUBMIT_BUTTON}

Welcome Page Should Be Open
    Location Should Be    ${WELCOME_URL}
    Page Should Contain    Welcome

Login With Credentials
    [Arguments]    ${username}    ${password}
    Input Username    ${username}
    Input Password    ${password}
    Click Login Button
```

### Custom Keywords in Python

```python
# libraries/CustomLibrary.py
from robot.api.deco import keyword
import hashlib


class CustomLibrary:
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.session = None

    @keyword("Generate MD5 Hash")
    def generate_md5(self, text: str) -> str:
        """Generate MD5 hash of the given text."""
        return hashlib.md5(text.encode()).hexdigest()

    @keyword("Format Currency")
    def format_currency(self, amount: float, symbol: str = "$") -> str:
        """Format amount as currency string."""
        return f"{symbol}{amount:,.2f}"

    @keyword("Validate Email Format")
    def validate_email(self, email: str) -> bool:
        """Check if email format is valid."""
        import re
        pattern = r"^[^@]+@[^@]+\.[^@]+$"
        return bool(re.match(pattern, email))
```

### Keyword Arguments

```robot
*** Keywords ***
Create User Via API
    [Arguments]    ${name}    ${email}    ${role}=user    ${status}=active
    ${payload} =    Create Dictionary
    ...    name=${name}
    ...    email=${email}
    ...    role=${role}
    ...    status=${status}
    ${response} =    POST On Session    api    /users    json=${payload}
    Should Be Equal As Strings    ${response.status_code}    201
    RETURN    ${response.json()['id']}
```

### Keyword Teardown

```robot
*** Keywords ***
Create Temporary File
    [Arguments]    ${content}
    [Teardown]    Remove File    ${path}
    ${path} =    Join Path    ${TEMPDIR}    temp.txt
    Create File    ${path}    ${content}
    RETURN    ${path}
```

---

## 4. Variables

### Variable Scopes

| Prefix | Scope | Example |
|--------|-------|---------|
| `${VAR}` | Global / Test case | `${VALID_USER}` |
| `@{LIST}` | List variable | `@{USERS}` |
| `&{DICT}` | Dictionary variable | `&{CREDENTIALS}` |
| `$${VAR}` | Environment variable | `$${PATH}` |
| `%{VAR}` | Operating system variable | `%{HOME}` |

### Scalar Variables

```robot
*** Variables ***
${URL}              https://api.example.com
${BROWSER}          chrome
${TIMEOUT}          10
${VALID_USER}       testuser@example.com
${VALID_PASSWORD}   TestPassword123!
```

### List Variables

```robot
*** Variables ***
@{BROWSERS}         chrome    firefox    edge
@{HTTP_METHODS}     GET       POST       PUT       DELETE
```

```robot
*** Test Cases ***
Test All Browsers
    FOR    ${browser}    IN    @{BROWSERS}
        Open Browser    ${URL}    ${browser}
        Log In With Valid Credentials
        Close Browser
    END
```

### Dictionary Variables

```robot
*** Variables ***
&{VALID_CREDENTIALS}    username=testuser    password=TestPass123
&{HEADERS}                Content-Type=application/json    Accept=application/json
```

```robot
*** Test Cases ***
Login With Dictionary Credentials
    Input Text    ${LOGIN.USERNAME}    ${VALID_CREDENTIALS}[username]
    Input Text    ${LOGIN.PASSWORD}    ${VALID_CREDENTIALS}[password]
```

### Variable Files (Python)

```python
# variables/global_variables.py
import os

URL = os.environ.get("BASE_URL", "https://staging.example.com")
BROWSER = os.environ.get("BROWSER", "chrome")
TIMEOUT = int(os.environ.get("TIMEOUT", "10"))

VALID_USER = os.environ.get("TEST_USER", "testuser@example.com")
VALID_PASSWORD = os.environ.get("TEST_PASSWORD", "TestPassword123!")
```

```robot
*** Settings ***
Variables    ../variables/global_variables.py
```

### Variable Files (YAML)

```yaml
# variables/test_data.yaml
users:
  admin:
    username: admin@example.com
    password: AdminPass123
    role: administrator
  editor:
    username: editor@example.com
    password: EditorPass456
    role: editor
```

```robot
*** Settings ***
Variables    ../variables/test_data.yaml

*** Test Cases ***
Login As Admin
    Log In    ${users}[admin][username]    ${users}[admin][password]
```

---

## 5. Libraries

### SeleniumLibrary (UI Testing)

```robot
*** Settings ***
Library    SeleniumLibrary    timeout=10    implicit_wait=2

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    0.5s
    Go To    ${URL}/login
    Title Should Be    Login

Wait And Click Element
    [Arguments]    ${locator}
    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    Click Element    ${locator}

Capture Screenshot On Failure
    [Arguments]    ${filename}
    Capture Page Screenshot    ${filename}
```

### RequestsLibrary (API Testing)

```robot
*** Settings ***
Library    RequestsLibrary

*** Keywords ***
Create API Session
    Create Session    api    ${URL}    headers=${HEADERS}
    ${token} =    Get Auth Token
    Set To Dictionary    ${HEADERS}    Authorization=Bearer ${token}

Get Auth Token
    ${payload} =    Create Dictionary    username=${VALID_USER}    password=${VALID_PASSWORD}
    ${response} =    POST On Session    api    /auth/login    json=${payload}
    Should Be Equal As Strings    ${response.status_code}    200
    RETURN    ${response.json()['token']}

Get User By ID
    [Arguments]    ${user_id}
    ${response} =    GET On Session    api    /users/${user_id}
    Should Be Equal As Strings    ${response.status_code}    200
    RETURN    ${response.json()}
```

### DatabaseLibrary (Database Testing)

```robot
*** Settings ***
Library    DatabaseLibrary

*** Keywords ***
Connect To Test Database
    Connect To Database
    ...    pymysql
    ...    ${DB_NAME}
    ...    ${DB_USER}
    ...    ${DB_PASSWORD}
    ...    ${DB_HOST}
    ...    ${DB_PORT}

Verify User Exists In Database
    [Arguments]    ${email}
    ${result} =    Query    SELECT id FROM users WHERE email = '${email}'
    Should Not Be Empty    ${result}
```

### Built-in Libraries Summary

| Library | Purpose |
|---------|---------|
| `BuiltIn` | Core keywords (log, evaluate, run keyword if, etc.) |
| `Collections` | List/dictionary operations |
| `DateTime` | Date and time manipulation |
| `OperatingSystem` | File system, environment variables |
| `Process` | Run external processes |
| `Screenshot` | Take screenshots |
| `String` | String manipulation |
| `XML` | XML parsing and validation |

---

## 6. Resource & Variable Files

### Resource File Structure

```robot
# resources/keywords/common.robot
*** Settings ***
Documentation    Common keywords used across test suites
Library          SeleniumLibrary
Library          RequestsLibrary
Variables        ../variables/global_variables.py

*** Keywords ***
Log In With Valid Credentials
    Input Text    ${LOGIN.USERNAME}    ${VALID_USER}
    Input Text    ${LOGIN.PASSWORD}    ${VALID_PASSWORD}
    Click Button    ${LOGIN.SUBMIT}
    Welcome Page Should Be Open

Log In
    [Arguments]    ${username}    ${password}
    Input Text    ${LOGIN.USERNAME}    ${username}
    Input Text    ${LOGIN.PASSWORD}    ${password}
    Click Button    ${LOGIN.SUBMIT}

Log Out
    Click Element    ${NAV.LOGOUT}
    Page Should Contain    You have been logged out
```

### Page Object Pattern

```robot
# resources/pages/login_page.robot
*** Variables ***
${LOGIN.URL}              /login
${LOGIN.USERNAME}         id:username
${LOGIN.PASSWORD}         id:password
${LOGIN.SUBMIT}           id:submit-button
${LOGIN.ERROR}            css:.error-message
${LOGIN.SUCCESS}          css:.success-message

*** Keywords ***
Open Login Page
    Go To    ${BASE_URL}${LOGIN.URL}
    Wait Until Element Is Visible    ${LOGIN.USERNAME}

Input Username
    [Arguments]    ${username}
    Input Text    ${LOGIN.USERNAME}    ${username}

Input Password
    [Arguments]    ${password}
    Input Text    ${LOGIN.PASSWORD}    ${password}

Submit Login Form
    Click Button    ${LOGIN.SUBMIT}

Error Message Should Be Visible
    [Arguments]    ${expected_message}
    Wait Until Element Is Visible    ${LOGIN.ERROR}
    Element Should Contain    ${LOGIN.ERROR}    ${expected_message}
```

### Importing Resources

```robot
*** Settings ***
Resource    ../resources/keywords/common.robot
Resource    ../resources/pages/login_page.robot
Resource    ../resources/pages/home_page.robot
Variables   ../variables/global_variables.py
Variables   ../variables/test_data.yaml
```

---

## 7. Setup & Teardown

### Levels

```robot
*** Settings ***
# Suite-level: runs once per suite file
Suite Setup       Connect To Test Database
Suite Teardown    Disconnect From Database

# Test-level: runs before/after each test case
Test Setup        Open Browser To Login Page
Test Teardown     Close Browser

# Task-level (in RPA): runs before/after each task
Task Setup        Log In As Admin
Task Teardown     Log Out
```

### Named Setup/Teardown

```robot
*** Keywords ***
Prepare Test Environment
    Connect To Database
    Clean Test Data
    Seed Test Users

Clean Up Test Environment
    Rollback Transactions
    Disconnect From Database

*** Settings ***
Suite Setup       Run Keywords    Prepare Test Environment    AND    Log    Suite setup complete
Suite Teardown    Run Keywords    Clean Up Test Environment    AND    Log    Suite teardown complete
```

### Conditional Teardown

```robot
*** Test Cases ***
Create Order Test
    [Setup]    Log In As Admin
    [Teardown]    Run Keyword If Test Failed    Cancel Order    ${ORDER_ID}
    ${ORDER_ID} =    Create Order
    Verify Order Exists    ${ORDER_ID}
```

---

## 8. Tags

### Tag Syntax

```robot
*** Test Cases ***
Valid Login
    [Tags]    smoke    regression    critical    ui
    ...       jira:PROJ-123
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Welcome Page Should Be Open
```

### Tagging at Suite Level

```robot
*** Settings ***
Default Tags    regression    api
Force Tags      sprint-42
```

### Tag Patterns in CLI

```bash
# Include only smoke tests
robot --include smoke tests/

# Exclude slow tests
robot --exclude slow tests/

# Include smoke AND critical
robot --include smokeANDcritical tests/

# Include smoke OR critical
robot --include smokeORcritical tests/

# Exclude wip AND debug
robot --exclude wipORdebug tests/

# Combine include and exclude
robot --include regression --exclude slow tests/

# Tag patterns with wildcards
robot --include sprint* tests/
```

### Tagging via Python Listener

```python
# listeners/TagListener.py
from robot.api import SuiteVisitor


class TagListener(SuiteVisitor):
    def start_suite(self, suite):
        for test in suite.tests:
            if "api" in suite.name.lower():
                test.tags.add("api-suite")
```

---

## 9. Execution & CLI

### Basic Execution

```bash
# Run all tests in directory
robot tests/

# Run specific test file
robot tests/ui/login.robot

# Run specific test case
robot --test "Valid Login" tests/ui/login.robot

# Run multiple test suites
robot tests/ui/ tests/api/
```

### Output Options

```bash
# Custom output directory
robot --outputdir results/ tests/

# Custom report names
robot --output results/output.xml --report results/report.html --log results/log.html tests/

# Generate only XML (for CI)
robot --output results/output.xml --report NONE --log NONE tests/

# Set log level
robot --loglevel DEBUG tests/
```

### Variable Overrides

```bash
# Override variables from CLI
robot --variable BROWSER:firefox --variable URL:https://staging.example.com tests/

# Variable file
robot --variablefile variables/staging.py tests/

# Multiple variable files
robot --variablefile variables/common.py --variablefile variables/staging.py tests/
```

### Parallel Execution (pabot)

```bash
# Run tests in parallel across 4 processes
pabot --processes 4 tests/

# Parallel with custom output
pabot --processes 4 --outputdir results/ tests/

# Parallel by suite
pabot --processes 4 --pabotlib tests/
```

### Dry Run

```bash
# Validate syntax without executing keywords
robot --dryrun tests/
```

### Listeners

```bash
# Custom listener for custom reporting
robot --listener listeners.AllureListener tests/
```

---

## 10. CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/robot-tests.yml
name: Robot Framework Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      selenium:
        image: selenium/standalone-chrome
        ports:
          - 4444:4444

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run Robot Framework tests
        run: |
          robot \
            --variable BROWSER:headlesschrome \
            --variable SELENIUM_URL:http://localhost:4444/wd/hub \
            --outputdir results/ \
            --exclude wip \
            tests/

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: robot-results
          path: results/
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh '''
                    robot \
                        --variable ENV:staging \
                        --outputdir results/ \
                        --exclude not_ready \
                        tests/
                '''
            }
        }
    }
    post {
        always {
            robot outputPath: 'results/'
        }
    }
}
```

### GitLab CI

```yaml
stages:
  - test

robot-tests:
  stage: test
  image: python:3.11
  services:
    - selenium/standalone-chrome
  script:
    - pip install -r requirements.txt
    - robot --outputdir results/ --exclude wip tests/
  artifacts:
    when: always
    paths:
      - results/
    reports:
      junit: results/output.xml
```

---

## 11. Best Practices Checklist

- [ ] Use **Page Object pattern**: locators in dedicated `.robot` files, logic in keyword files
- [ ] Keep test cases **short and focused**: one assertion per test
- [ ] Use **BDD naming**: `Given/When/Then` in test case names
- [ ] Extract reusable keywords to **resource files**
- [ ] Use **variables** for all dynamic data (URLs, credentials, timeouts)
- [ ] Store **sensitive data** in environment variables, never in repo
- [ ] Use **tag expressions** to organize by layer (`ui`, `api`, `db`) and priority (`smoke`, `regression`)
- [ ] Implement **setup/teardown** at the lowest possible scope
- [ ] Use `Wait Until Keyword Succeeds` for flaky operations
- [ ] Add `[Documentation]` to every test case and keyword
- [ ] Use `[Arguments]` typing for keyword parameters
- [ ] Return values from keywords using `RETURN` (or `Return From Keyword` in older versions)
- [ ] Use `Run Keyword And Ignore Error` for non-critical steps
- [ ] Implement custom Python libraries for complex logic
- [ ] Use `pabot` for parallel execution in CI
- [ ] Generate **JUnit-compatible output** for CI integration
- [ ] Keep locators in YAML or dedicated files, not inline in keywords
- [ ] Use `Set Selenium Speed` only for debugging, not in CI
- [ ] Implement `Listener` for custom reporting (Allure, TestRail, etc.)
- [ ] Version control `.robot` files; exclude `results/` directory

---

## 12. Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| `Variable not found` | Wrong scope or missing import | Check `*** Variables ***` section or resource import |
| `Keyword not found` | Missing `Resource` or `Library` import | Verify `*** Settings ***` imports |
| `Element not found` | Timing issue or wrong locator | Use `Wait Until Element Is Visible` with explicit timeout |
| `Suite setup failed` | Previous test left dirty state | Implement robust suite teardown |
| Slow test execution | `Sleep` or implicit waits | Replace `Sleep` with explicit waits |
| Duplicate keywords | Same name in multiple resources | Use resource namespacing or unique names |
| Hardcoded credentials | Values in `.robot` files | Move to environment variables or encrypted files |
| Brittle locators | XPath with dynamic IDs | Use `data-testid` attributes or CSS classes |
| Missing teardown on failure | Teardown not running after exception | Use `Run Keyword If Test Failed` in teardown |
| Parallel execution conflicts | Shared state between processes | Use `pabotlib` or isolate test data per process |
| Log pollution | Too many screenshots | Capture only on failure or for specific steps |
| `FOR` loop scope issues | Variables leaking between iterations | Use `END` and localize loop variables |

---

## 13. References

- [Robot Framework User Guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html)
- [SeleniumLibrary Documentation](https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html)
- [RequestsLibrary Documentation](https://marketsquare.github.io/robotframework-requests/)
- [DatabaseLibrary Documentation](https://github.com/franz-see/Robotframework-Database-Library)
- [Robot Framework Built-in Keywords](https://robotframework.org/robotframework/latest/libraries/BuiltIn.html)
- [pabot â€” Parallel Executor](https://pabot.org/)
- [Robot Framework Listener Interface](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-interface)
- Related skills: `selenium-automation`, `behave-bdd`, `playwright-best-practices`, `postman`

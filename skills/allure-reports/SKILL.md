---
name: Allure Reports
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Production-grade skill for generating rich test reports with Allure. Covers pytest, Behave, JUnit, annotations, attachments, steps, CI/CD integration, and custom categories.
tags: [allure, reporting, pytest, behave, junit, testing, ci-cd]
trigger: When the user asks to set up, configure, generate, or customize Allure reports for tests, or integrate Allure with pytest, Behave, JUnit, Cypress, or CI/CD pipelines.
---

# Allure Reports Skill

## Description

Comprehensive skill for generating rich, interactive test reports with Allure. Covers integration with Python (pytest, Behave), Java (JUnit), annotations for metadata, step-by-step traceability, attachments (screenshots, logs, files), custom categories, and CI/CD integration (Jenkins, GitHub Actions).

## Table of Contents

1. [Overview](#1-overview)
2. [Installation & Setup](#2-installation--setup)
3. [Pytest Integration](#3-pytest-integration)
4. [Behave Integration](#4-behave-integration)
5. [JUnit Integration](#5-junit-integration)
6. [Annotations & Metadata](#6-annotations--metadata)
7. [Steps & Nested Steps](#7-steps--nested-steps)
8. [Attachments](#8-attachments)
9. [Report Generation](#9-report-generation)
10. [CI/CD Integration](#10-cicd-integration)
11. [Custom Categories](#11-custom-categories)
12. [Best Practices Checklist](#12-best-practices-checklist)
13. [Common Pitfalls](#13-common-pitfalls)
14. [References](#14-references)

## When to Invoke

- Setting up Allure reporting for a test suite (pytest, Behave, JUnit, Cypress)
- Annotating tests with features, stories, severity, and labels
- Adding screenshots, logs, or files to test reports
- Implementing step-by-step traceability in test methods
- Configuring custom defect categories in Allure
- Integrating Allure into Jenkins, GitLab CI, or GitHub Actions
- Generating and serving Allure reports locally or in CI
- Troubleshooting missing attachments or empty reports

---

## 1. Overview

Allure is a flexible, lightweight multi-language test report tool. It produces interactive HTML reports with:

- Test cases grouped by suite, feature, and story
- Step-by-step execution trace
- Attachments (screenshots, logs, network captures)
- Severity levels, tags, and links to issues/PRs
- Trends and history across builds
- Custom defect categories (e.g., "Product Defect" vs "Test Defect")

### Supported Frameworks

| Language | Framework | Adapter |
|----------|-----------|---------|
| Python | pytest | `allure-pytest` |
| Python | Behave | `allure-behave` |
| Java | JUnit 4 | `allure-junit4` |
| Java | JUnit 5 | `allure-junit5` |
| JavaScript | Cypress | `@shelex/cypress-allure-plugin` |

---

## 2. Installation & Setup

### Python (pytest)

```bash
pip install allure-pytest
```

### Python (Behave)

```bash
pip install allure-behave
```

### Java (Maven)

```xml
<dependency>
    <groupId>io.qameta.allure</groupId>
    <artifactId>allure-junit5</artifactId>
    <version>2.25.0</version>
    <scope>test</scope>
</dependency>
```

### Allure Command-Line Tool

```bash
# macOS
brew install allure

# Windows (Scoop)
scoop install allure

# Linux
wget https://github.com/allure-framework/allure2/releases/download/2.25.0/allure-2.25.0.tgz
tar -xzf allure-2.25.0.tgz
sudo mv allure-2.25.0 /opt/allure
sudo ln -s /opt/allure/bin/allure /usr/local/bin/allure
```

### Verify Installation

```bash
allure --version
```

---

## 3. Pytest Integration

### pytest.ini

```ini
[pytest]
addopts = --alluredir=reports/allure-results
```

### Basic Test with Annotations

```python
import allure
import pytest


@allure.feature("User Management")
@allure.story("Create User")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify user creation with valid data")
@allure.description("This test validates that a new user can be created via the API.")
def test_create_user(api_client):
    with allure.step("Send POST request to /users"):
        response = api_client.post("/users", json={"name": "John", "email": "john@test.com"})

    with allure.step("Verify response status is 201"):
        assert response.status_code == 201

    with allure.step("Verify response contains user ID"):
        assert "id" in response.json()
```

### Fixtures with Allure Steps

```python
@pytest.fixture
def authenticated_client():
    with allure.step("Authenticate test user"):
        client = ApiClient()
        client.login("testuser", "password123")
    yield client
    with allure.step("Logout and cleanup"):
        client.logout()
```

### Dynamic Titles and Descriptions

```python
@allure.title("Dynamic title: {param1} + {param2}")
@pytest.mark.parametrize("param1,param2", [(1, 2), (3, 4)])
def test_dynamic_title(param1, param2):
    allure.dynamic.title(f"Custom title for {param1} and {param2}")
    allure.dynamic.description("This description was set at runtime.")
    assert param1 + param2 > 0
```

### Labels and Links

```python
@allure.label("owner", "qa-team")
@allure.label("layer", "api")
@allure.link("https://jira.example.com/PROJ-123", name="JIRA-123")
@allure.issue("https://bugzilla.example.com/456", name="BUG-456")
def test_with_metadata():
    pass
```

---

## 4. Behave Integration

### behave.ini

```ini
[behave]
format=allure_behave.formatter:AllureFormatter
outfiles=reports/allure-results
```

### Feature File with Tags

```gherkin
@allure.feature.user_management
@allure.story.create_user
Feature: User Management

  @allure.severity.critical
  @allure.label.owner:qa_team
  Scenario: Create a new user
    Given the API is available
    When I send a POST request to /users with valid data
    Then the response status should be 201
    And the response should contain a user ID
```

### Environment Hooks with Allure

```python
# features/environment.py
import allure
from allure_commons.types import AttachmentType


def before_scenario(context, scenario):
    allure.dynamic.feature("User Management")
    allure.dynamic.story(scenario.name)


def after_step(context, step):
    if step.status == "failed":
        if hasattr(context, "browser"):
            screenshot = context.browser.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=AttachmentType.PNG
            )
```

### Attachments in Steps

```python
# features/steps/api_steps.py
import allure
from allure_commons.types import AttachmentType
import json


@when('I send a POST request to {endpoint} with valid data')
def step_send_post(context, endpoint):
    payload = {"name": "Test User", "email": "test@example.com"}

    allure.attach(
        json.dumps(payload, indent=2),
        name="Request Payload",
        attachment_type=AttachmentType.JSON
    )

    context.response = context.client.post(endpoint, json=payload)

    allure.attach(
        json.dumps(context.response.json(), indent=2),
        name="Response Body",
        attachment_type=AttachmentType.JSON
    )
```

---

## 5. JUnit Integration

### JUnit 5 Example

```java
import io.qameta.allure.*;
import org.junit.jupiter.api.Test;

@Feature("User Management")
@Story("Create User")
@Severity(SeverityLevel.CRITICAL)
@Owner("qa-team")
@Link(name = "JIRA-123", url = "https://jira.example.com/PROJ-123")
public class UserTest {

    @Step("Send POST request to /users")
    public Response createUser(String name, String email) {
        return apiClient.post("/users", Map.of("name", name, "email", email));
    }

    @Test
    @Title("Verify user creation with valid data")
    @Description("This test validates that a new user can be created.")
    public void testCreateUser() {
        Response response = createUser("John", "john@test.com");
        Assertions.assertEquals(201, response.getStatusCode());
    }

    @Attachment(value = "Request Payload", type = "application/json")
    public byte[] attachRequestPayload(String payload) {
        return payload.getBytes();
    }
}
```

---

## 6. Annotations & Metadata

### Severity Levels

| Level | Use Case |
|-------|----------|
| `BLOCKER` | Critical functionality broken; blocks release |
| `CRITICAL` | Core feature failure |
| `NORMAL` | Standard test |
| `MINOR` | Edge case or cosmetic issue |
| `TRIVIAL` | Documentation or typo check |

### Python Decorators

```python
@allure.feature("Feature Name")
@allure.story("Story Name")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Custom test title")
@allure.description("Detailed description")
@allure.description_html("<b>HTML</b> description")
@allure.tag("regression", "smoke")
@allure.label("owner", "qa-team")
@allure.label("layer", "ui")
@allure.link("https://docs.example.com", name="Documentation")
@allure.issue("https://jira.example.com/PROJ-456", name="PROJ-456")
@allure.testcase("https://testrail.example.com/C123", name="TestRail C123")
```

### Dynamic Annotations (Runtime)

```python
def test_dynamic_metadata():
    allure.dynamic.feature("Dynamic Feature")
    allure.dynamic.story("Dynamic Story")
    allure.dynamic.title("Dynamic Title")
    allure.dynamic.description("Set at runtime based on conditions.")
    allure.dynamic.label("owner", "dynamic-owner")
```

---

## 7. Steps & Nested Steps

### Python (pytest)

```python
import allure


def test_with_steps():
    with allure.step("Step 1: Prepare test data"):
        user = {"name": "Alice", "email": "alice@example.com"}

    with allure.step("Step 2: Execute API call"):
        with allure.step("Step 2.1: Send request"):
            response = api.post("/users", json=user)

        with allure.step("Step 2.2: Verify response"):
            assert response.status_code == 201

    with allure.step("Step 3: Verify database state"):
        db_user = db.query(User).filter_by(email="alice@example.com").first()
        assert db_user is not None
```

### Decorator Style (Python)

```python
@allure.step("Create user with name={name} and email={email}")
def create_user(name: str, email: str):
    return api.post("/users", json={"name": name, "email": email})


def test_using_step_function():
    response = create_user("Bob", "bob@example.com")
    assert response.status_code == 201
```

### Java (JUnit)

```java
@Step("Verify user exists in database: {email}")
public void verifyUserInDatabase(String email) {
    User user = userRepository.findByEmail(email);
    assertNotNull(user);
}
```

---

## 8. Attachments

### Python Attachments

```python
import allure
from allure_commons.types import AttachmentType
import json


def test_with_attachments(browser):
    # Screenshot
    allure.attach(
        browser.get_screenshot_as_png(),
        name="Homepage Screenshot",
        attachment_type=AttachmentType.PNG
    )

    # JSON payload
    allure.attach(
        json.dumps({"user": "test", "role": "admin"}, indent=2),
        name="Request Body",
        attachment_type=AttachmentType.JSON
    )

    # Log file
    allure.attach.file(
        "/var/log/app.log",
        name="Application Log",
        attachment_type=AttachmentType.TEXT
    )

    # Plain text
    allure.attach(
        "This is a plain text attachment",
        name="Notes",
        attachment_type=AttachmentType.TEXT
    )
```

### Attachment Types

| Type | Constant |
|------|----------|
| PNG image | `AttachmentType.PNG` |
| JPEG image | `AttachmentType.JPG` |
| JSON | `AttachmentType.JSON` |
| XML | `AttachmentType.XML` |
| HTML | `AttachmentType.HTML` |
| Plain text | `AttachmentType.TEXT` |
| CSV | `AttachmentType.CSV` |
| URI | `AttachmentType.URI` |

### Java Attachments

```java
@Attachment(value = "Screenshot", type = "image/png")
public byte[] takeScreenshot() {
    return ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
}

@Attachment(value = "Page Source", type = "text/html")
public String attachPageSource() {
    return driver.getPageSource();
}
```

---

## 9. Report Generation

### Generate Results

```bash
# pytest
pytest --alluredir=reports/allure-results

# Behave
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results

# JUnit (Maven)
mvn clean test allure:report
```

### Serve Report (Local Development)

```bash
allure serve reports/allure-results
```

### Generate Static HTML

```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

### Report Structure

```
reports/
  allure-results/       # Raw JSON data (commit to CI artifacts)
  allure-report/        # Generated HTML (do not commit)
```

---

## 10. CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/tests.yml
name: Tests with Allure

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install allure-pytest

      - name: Run tests
        run: pytest --alluredir=reports/allure-results

      - name: Generate Allure Report
        if: always()
        run: |
          allure generate reports/allure-results -o reports/allure-report --clean

      - name: Upload Report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-report
          path: reports/allure-report
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pytest --alluredir=reports/allure-results'
            }
        }
    }
    post {
        always {
            allure([
                includeProperties: false,
                jdk: '',
                properties: [],
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'reports/allure-results']]
            ])
        }
    }
}
```

### GitLab CI

```yaml
stages:
  - test
  - report

test:
  stage: test
  script:
    - pytest --alluredir=allure-results
  artifacts:
    when: always
    paths:
      - allure-results/

allure:
  stage: report
  image: frankescobar/allure-docker-service
  script:
    - allure generate allure-results -o allure-report --clean
  artifacts:
    paths:
      - allure-report/
```

---

## 11. Custom Categories

Allure categorizes failures by default into "Product defects" and "Test defects". You can customize this.

### categories.json

Place this in `allure-results/` before report generation:

```json
[
  {
    "name": "Infrastructure Issues",
    "matchedStatuses": ["broken"],
    "messageRegex": ".*Connection refused.*"
  },
  {
    "name": "Known Flaky Tests",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*TimeoutException.*"
  },
  {
    "name": "Validation Errors",
    "matchedStatuses": ["failed"],
    "traceRegex": ".*AssertionError.*"
  }
]
```

### Environment Properties

```properties
# environment.properties
Browser=Chrome 120
OS=Ubuntu 22.04
Test.Environment=Staging
API.Version=v2.1
```

### Executor Info

```json
{
  "name": "jenkins",
  "type": "jenkins",
  "url": "http://jenkins.example.com",
  "buildOrder": 42,
  "buildName": "build #42",
  "buildUrl": "http://jenkins.example.com/job/42",
  "reportUrl": "http://jenkins.example.com/job/42/allure",
  "reportName": "Allure Report"
}
```

---

## 12. Best Practices Checklist

- [ ] Every test has a `@feature` and `@story` annotation
- [ ] Severity is assigned based on business impact (`BLOCKER` > `CRITICAL` > `NORMAL`)
- [ ] Steps describe **actions**, not assertions (`"Click login"` not `"Verify login works"`)
- [ ] Attach screenshots on UI test failures
- [ ] Attach request/response bodies for API test failures
- [ ] Attach logs when a test breaks (not just fails)
- [ ] Use dynamic annotations for parameterized tests
- [ ] Link tests to JIRA/Trello/TestRail tickets
- [ ] Label tests by layer (`ui`, `api`, `unit`) for filtering
- [ ] Use `@allure.title()` for human-readable test names
- [ ] Keep `allure-results/` as CI artifacts for history
- [ ] Generate reports with `--clean` to avoid stale data
- [ ] Add `environment.properties` for context (browser, OS, API version)
- [ ] Use `categories.json` to group failures by root cause
- [ ] Do not commit generated HTML reports to version control
- [ ] Use nested steps for complex workflows (login → navigate → perform action)
- [ ] Set `allure.description` or `allure.description_html` for complex test logic

---

## 13. Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| Empty report | No `allure-results` data or wrong path | Check `--alluredir` path matches `allure serve` path |
| Missing screenshots | Attachment after test failure | Add screenshot in `after_step` or `on_exception` hook |
| Duplicate test names | Same `@title` across parameterized tests | Use dynamic title with parameter values |
| Broken links in report | Relative paths or missing `categories.json` | Use absolute URLs in `@link` and provide `categories.json` |
| Report not showing history | Missing `allure-results` from previous runs | Persist `allure-results` between CI builds |
| Steps not visible | Missing `with allure.step()` or wrong import | Ensure `import allure` and use context manager |
| Large report size | Too many screenshots/videos | Compress images or attach only on failure |
| Attachments not opening | Wrong `attachment_type` | Use correct `AttachmentType` constant |
| CI report not generated | `allure` CLI not installed | Install CLI tool in CI image or use Docker |
| Flaky test categories missing | No `categories.json` in results | Copy `categories.json` before report generation |

---

## 14. References

- [Allure Framework](https://docs.qameta.io/allure/)
- [Allure pytest](https://docs.qameta.io/allure-report/frameworks/python/pytest/)
- [Allure Behave](https://docs.qameta.io/allure-report/frameworks/python/behave/)
- [Allure JUnit 5](https://docs.qameta.io/allure-report/frameworks/java/junit5/)
- [Allure Cypress](https://docs.qameta.io/allure-report/frameworks/js/cypress/)
- [Allure CLI](https://docs.qameta.io/allure/#_installing_a_commandline)
- Related skills: `behave-bdd`, `python-testing-patterns`, `java-junit`, `playwright-best-practices`, `cypress-author`

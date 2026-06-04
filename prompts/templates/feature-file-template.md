---
name: Feature File Template
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Parametrizable Gherkin feature file template with Background, Scenario Outline, Examples, Data Tables, and Doc Strings. Ready to copy and adapt.
tags: [gherkin, bdd, template, feature-file, behave, cucumber]
role: bdd-writer
model: any
trigger: When the user asks for a Gherkin feature file template or a BDD test template.
---

# Feature File Template

Use this template as a starting point for Gherkin feature files. Copy, fill in the placeholders, and adapt to your domain.

## Basic Feature

```gherkin
Feature: {{Feature Name}}
  As a {{user role}}
  I want to {{action}}
  So that {{benefit}}

  Background:
    Given {{precondition 1}}
    And {{precondition 2}}

  @{{tag1}} @{{tag2}}
  Scenario: {{scenario name}}
    Given {{context}}
    When {{action}}
    Then {{expected outcome}}
    And {{additional assertion}}
```

## Scenario Outline (Data-Driven)

```gherkin
Feature: {{Feature Name}}
  As a {{user role}}
  I want to {{action}}
  So that {{benefit}}

  Background:
    Given the system is initialized

  @regression @smoke
  Scenario Outline: {{scenario name with <parameter>}}
    Given a user with role "<role>"
    When they attempt to access "<resource>"
    Then the access should be "<result>"

    Examples:
      | role       | resource      | result     |
      | admin      | /dashboard    | granted    |
      | editor     | /dashboard    | granted    |
      | viewer     | /dashboard    | denied     |
      | admin      | /settings     | granted    |
      | editor     | /settings     | denied     |
      | viewer     | /settings     | denied     |
```

## With Data Table

```gherkin
Feature: {{Feature Name}}

  Scenario: {{scenario name}}
    Given the following products exist:
      | name        | price | category  |
      | Headphones  | 99.99 | Electronics|
      | Coffee Mug  | 12.50 | Kitchen   |
      | Notebook    | 5.00  | Stationery |
    When I apply a "<discount>" discount to "<product>"
    Then the final price should be "<final_price>"
```

## With Doc String

```gherkin
Feature: {{Feature Name}}

  Scenario: {{scenario name}}
    Given the following email template:
      """
      Dear {{name}},

      Your order #{{order_id}} has been shipped.
      Expected delivery: {{delivery_date}}.

      Thank you for your business.
      """
    When the system sends the email to "{{email}}"
    Then the email body should contain "{{expected_content}}"
```

## Tags Convention

```gherkin
@feature-level-tag
Feature: {{Feature Name}}

  @smoke @critical
  Scenario: Critical path test
    ...

  @regression @negative
  Scenario: Error handling test
    ...

  @wip @manual
  Scenario: Work in progress
    ...
```

## Background + Multiple Scenarios

```gherkin
Feature: User Authentication
  As a registered user
  I want to log in and out
  So that I can access my account securely

  Background:
    Given the login page is displayed
    And the following users exist:
      | username | password    | status   |
      | alice    | Password123 | active   |
      | bob      | Password456 | inactive |

  @smoke @login
  Scenario: Successful login with valid credentials
    When I enter "alice" as username
    And I enter "Password123" as password
    And I click the login button
    Then I should be redirected to the dashboard
    And my username should be displayed in the header

  @regression @negative
  Scenario: Login fails with invalid password
    When I enter "alice" as username
    And I enter "wrongpassword" as password
    And I click the login button
    Then I should see the error message "Invalid credentials"
    And I should remain on the login page

  @regression @negative
  Scenario: Login fails for inactive user
    When I enter "bob" as username
    And I enter "Password456" as password
    And I click the login button
    Then I should see the error message "Account is inactive"

  @regression @security
  Scenario: Login fails with empty credentials
    When I leave the username field empty
    And I leave the password field empty
    And I click the login button
    Then I should see validation errors for both fields
```

## Variables Reference

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{Feature Name}}` | Descriptive feature title | `User Authentication` |
| `{{user role}}` | Actor in the story | `registered user` |
| `{{action}}` | What the user wants to do | `log in and out` |
| `{{benefit}}` | Business value | `access my account securely` |
| `{{scenario name}}` | Concrete test scenario | `Successful login` |
| `{{tag1}}` | Execution filter tag | `smoke`, `regression` |
| `{{parameter}}` | Scenario Outline variable | `role`, `resource` |

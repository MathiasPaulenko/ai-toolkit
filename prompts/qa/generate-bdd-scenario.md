---
name: Generate BDD Scenario
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Convert user stories and requirements into Gherkin BDD scenarios with Given-When-Then structure, edge cases, and scenario outlines.
tags: [bdd, gherkin, testing, requirements, scenarios]
role: qa-engineer
model: any
trigger: When the user asks to write BDD scenarios, convert requirements to Gherkin, or create Given-When-Then tests.
---

# Generate BDD Scenario

Convert requirements into Gherkin BDD scenarios.

## Input

- User story or requirement text
- Acceptance criteria (if available)
- Business rules and constraints
- Edge cases to consider

## Output Format

```gherkin
Feature: [Feature Name]
  As a [role]
  I want [goal]
  So that [benefit]

  Background:
    Given [common precondition]
    And [another common precondition]

  Scenario: [Happy path description]
    Given [precondition]
    And [precondition]
    When [action]
    And [action]
    Then [expected result]
    And [expected result]

  Scenario: [Alternative path]
    Given [precondition]
    When [different action]
    Then [expected result]

  Scenario: [Error path]
    Given [precondition]
    When [invalid action]
    Then [error result]
    And [error detail]

  Scenario Outline: [Parameterized scenario]
    Given [precondition with <variable>]
    When [action]
    Then [expected result with <variable>]

    Examples:
      | variable | expected |
      | value1   | result1  |
      | value2   | result2  |
```

## Rules

- One scenario = one behavior (single When)
- Background only for shared preconditions
- Scenario Outline for data-driven cases (3+ examples)
- Use declarative language, not imperative UI steps
- Tag scenarios: `@smoke`, `@regression`, `@negative`, `@wip`

## Example Input

"As a customer, I want to apply a discount code at checkout so I can get reduced prices. The code must be valid, not expired, and not already used."

## Example Output

```gherkin
Feature: Discount Code Application
  As a customer
  I want to apply a discount code at checkout
  So that I can get reduced prices on my order

  Background:
    Given I have items in my cart totaling $100

  @smoke
  Scenario: Valid discount code reduces total
    Given I have a valid discount code "SAVE20" for 20% off
    When I apply the discount code at checkout
    Then the order total should be $80
    And a success message should be displayed

  @negative
  Scenario: Expired discount code is rejected
    Given I have an expired discount code "OLD2023"
    When I apply the discount code at checkout
    Then the order total should remain $100
    And an error "Code expired" should be displayed

  @negative
  Scenario: Already used discount code is rejected
    Given I have a discount code "SAVE20" that I already used
    When I apply the discount code at checkout
    Then the order total should remain $100
    And an error "Code already used" should be displayed

  Scenario Outline: Invalid code formats are rejected
    When I apply the discount code "<code>"
    Then the order total should remain $100
    And an error "Invalid code" should be displayed

    Examples:
      | code    |
      |         |
      | ABC     |
      | !!!     |
```

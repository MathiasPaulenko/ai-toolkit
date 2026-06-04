---
name: Karate API Testing
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "API testing with Karate DSL: REST, GraphQL, gRPC, mocking, parallel execution, CI/CD integration, and data-driven tests."
tags: [api-testing, karate, bdd, rest, graphql]
role: api-tester
---

# Karate API Testing

Invoke when user asks about Karate DSL, API testing with Karate, or BDD-style API automation.

## Core Principles

- **DSL first**: Tests are readable by non-developers.
- **Zero Java required**: JSON/YAML-like syntax, no compilation needed.
- **Built-in**: assertions, JSON/XML parsing, parallel execution, mocking.

## Feature File Structure

```gherkin
Feature: User API

  Background:
    * url 'https://api.example.com'
    * def token = call read('classpath:auth.js')
    * header Authorization = 'Bearer ' + token

  Scenario: Create and retrieve user
    Given path 'users'
    And request { name: 'Alice', email: 'alice@test.com' }
    When method post
    Then status 201
    And match response ==
      """
      {
        id: '#number',
        name: 'Alice',
        email: 'alice@test.com',
        createdAt: '#ignore'
      }
      """
    And def userId = response.id

    Given path 'users', userId
    When method get
    Then status 200
    And match response.name == 'Alice'
```

## Key Syntax Patterns

### Match Operators

```gherkin
Then match response.name == 'Alice'          # Exact
Then match response.id == '#number'          # Type check
Then match response.tags == '#[]'            # Array
Then match response.tags == '#[2] #'         # Array of 2+ items
Then match response.status == '#present'     # Non-null
Then match response.meta == '#notpresent'    # Absent
```

### Dynamic Data

```gherkin
# JavaScript function
* def generateEmail =
  """
  function() {
    var uuid = java.util.UUID.randomUUID().toString();
    return 'test-' + uuid + '@example.com';
  }
  """
* def email = generateEmail()
```

### Data-Driven Tests

```gherkin
Scenario Outline: Login with <scenario>
  Given path 'auth/login'
  And request { email: '<email>', password: '<password>' }
  When method post
  Then status <status>

  Examples:
    | scenario | email             | password | status |
    | valid    | alice@test.com    | correct  | 200    |
    | wrong_pw | alice@test.com    | wrong    | 401    |
    | missing  |                   |          | 400    |
```

## Reusable Helpers

```gherkin
# karate-config.js
function fn() {
  var env = karate.env || 'dev';
  var config = {
    baseUrl: 'https://api-' + env + '.example.com',
    timeout: 30000,
  };

  if (env === 'prod') {
    config.token = karate.read('classpath:secrets/prod-token.txt');
  }

  return config;
}
```

```gherkin
# common.feature
@ignore
Feature: Common Steps

  Scenario: Authenticate
    Given path 'auth/token'
    And request { client_id: '#(clientId)', client_secret: '#(clientSecret)' }
    When method post
    Then status 200
    And def accessToken = response.access_token
```

## GraphQL Testing

```gherkin
Feature: GraphQL Users

  Scenario: Query users
    Given path 'graphql'
    And request
      """
      {
        query: "{ users(limit: 5) { id name } }"
      }
      """
    When method post
    Then status 200
    And match $.data.users == '#[_ > 0]'
```

## Mocking with Karate Netty

```bash
# Start mock server
java -jar karate.jar -m mock.feature -p 8080
```

```gherkin
# mock.feature
Feature: Mock API

  Scenario: pathMatches('/users') && methodIs('get')
    * def response = read('classpath:fixtures/users.json')
    * def status = 200
```

## CI/CD Integration

```xml
<!-- pom.xml -->
<plugin>
  <groupId>com.intuit.karate</groupId>
  <artifactId>karate-maven-plugin</artifactId>
  <version>1.5.0</version>
  <executions>
    <execution>
      <goals><goal>test</goal></goals>
    </execution>
  </executions>
</plugin>
```

```bash
# Run all
mvn test -Dtest=KarateTest

# Run tagged
mvn test -Dkarate.options="--tags @smoke"
```

## Reporting

- Karate HTML report: `target/karate-reports/karate-summary.html`
- Cucumber JSON: add `cucumber-report` dependency
- Allure: add `allure-cucumber` adapter

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Inline large payloads | Use `read('classpath:json/user.json')` |
| Hardcoded IDs | Generate UUIDs or use fixtures |
| One mega-feature | Split by domain: `users.feature`, `orders.feature` |
| Ignoring response structure | Use `#present` / `#notpresent` selectively |

## Example: End-to-End Flow

```gherkin
Feature: Order Flow

  Background:
    * url baseUrl
    * call read('classpath:auth.feature')

  Scenario: Place order end-to-end
    # Create product
    Given path 'products'
    And request { name: 'Widget', price: 19.99 }
    When method post
    Then status 201
    And def productId = response.id

    # Add to cart
    Given path 'cart'
    And request { productId: '#(productId)', qty: 2 }
    When method post
    Then status 200

    # Checkout
    Given path 'orders'
    And request { items: [{ productId: '#(productId)', qty: 2 }], payment: 'card' }
    When method post
    Then status 201
    And match response.total == 39.98
    And match response.status == 'confirmed'
```

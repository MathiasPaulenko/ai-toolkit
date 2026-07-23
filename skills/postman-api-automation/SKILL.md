---
name: postman-api-automation
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "API testing and automation with Postman/Newman: collections, environments, pre/post scripts, CI/CD reporting, and data-driven testing."
tags: [api-testing, postman, newman, automation, rest]
role: qa-engineer
model: any
trigger: When the user asks about Postman, Newman, API testing, collection automation, or API test CI/CD integration.
---

# Postman API Automation

Professional API testing with Postman and Newman.

## 1. Collection Structure

```
Collection: E-Commerce API
â”œâ”€â”€ 1. Auth
â”‚   â”œâ”€â”€ POST /auth/login
â”‚   â””â”€â”€ POST /auth/refresh
â”œâ”€â”€ 2. Products
â”‚   â”œâ”€â”€ GET /products
â”‚   â”œâ”€â”€ GET /products/:id
â”‚   â””â”€â”€ POST /products
â”œâ”€â”€ 3. Cart
â”‚   â”œâ”€â”€ POST /cart/items
â”‚   â”œâ”€â”€ PUT /cart/items/:id
â”‚   â””â”€â”€ DELETE /cart/items/:id
â”œâ”€â”€ 4. Orders
â”‚   â”œâ”€â”€ POST /orders
â”‚   â””â”€â”€ GET /orders/:id
â””â”€â”€ 5. Checkout
    â””â”€â”€ POST /checkout
```

## 2. Request Best Practices

### Naming Convention
`[METHOD] /path â€” expected behavior`  
Example: `GET /products/404 â€” returns 404 for unknown product`

### Folder Organization
- Group by resource/domain
- Auth folder first (dependency for others)
- Use folders for workflow sequences

### Variables Hierarchy
| Scope | Example | Use |
|-------|---------|-----|
| Global | `{{baseUrl}}` | Shared across all collections |
| Collection | `{{authToken}}` | Set in pre-request, used everywhere |
| Environment | `{{apiVersion}}` | Switch between dev/staging/prod |
| Data | `{{email}}` | Data-driven from CSV/JSON |
| Local | `responseJson` | Within single request script |

## 3. Pre-request & Tests Scripts

```javascript
// Pre-request: Setup auth
const token = pm.environment.get("authToken");
pm.request.headers.add({
  key: "Authorization",
  value: `Bearer ${token}`
});

// Pre-request: Dynamic data
pm.environment.set("randomEmail",
  `test-${Date.now()}@example.com`);

// Tests: Status & structure
pm.test("Status is 201", () => {
  pm.response.to.have.status(201);
});

pm.test("Response has correct schema", () => {
  const json = pm.response.json();
  pm.expect(json).to.have.property("id");
  pm.expect(json).to.have.property("createdAt");
  pm.expect(json.price).to.be.a("number");
  pm.expect(json.price).to.be.greaterThan(0);
});

// Tests: Chain requests
pm.test("Store order ID for next request", () => {
  const order = pm.response.json();
  pm.collectionVariables.set("orderId", order.id);
});

// Tests: Performance SLA
pm.test("Response time < 500ms", () => {
  pm.expect(pm.response.responseTime).to.be.below(500);
});
```

## 4. Newman CLI

```bash
# Run collection
newman run collection.json -e environment.json

# Run with reporters
newman run collection.json \
  -e env.json \
  --reporters cli,json,html \
  --reporter-json-export results.json \
  --reporter-html-export report.html

# Data-driven with CSV
newman run collection.json -d test-data.csv --iteration-count 100

# CI-friendly (no colors, exit code)
newman run collection.json --color off --bail
```

## 5. Data-Driven Testing

```csv
email,password,expectedStatus
valid@example.com,Password123,200
invalid@example.com,wrong,401
,bad,400
```

```javascript
// In request test
pm.test("Status matches expected", () => {
  const expected = parseInt(pm.iterationData.get("expectedStatus"));
  pm.response.to.have.status(expected);
});
```

## 6. CI/CD Integration

```yaml
# .github/workflows/api-tests.yml
name: API Tests
on: [push, pull_request]
jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm install -g newman newman-reporter-htmlextra
      - run: |
          newman run postman/collection.json \
            -e postman/env.ci.json \
            --reporters cli,junit,htmlextra \
            --reporter-junit-export results.xml
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: api-test-report
          path: newman/
```

## 7. OpenAPI Sync

```bash
# Generate collection from OpenAPI spec
postman openapi-to-collection openapi.yaml \
  --output collection.json \
  --base-url {{baseUrl}}

# Or with openapi-to-postman
npx @apideck/portman -i openapi.yaml -o collection.json
```

## 8. Monitors (Postman Cloud)

- Schedule collections to run every X minutes
- Integrate with Slack/PagerDuty for failures
- Track response times over time
- Run from multiple regions

## 9. Advanced Patterns

### Mock Servers
```bash
# Create mock from collection for parallel dev
postman mock create --collection-id 12345 --name "payment-mock"
```

### Contract Testing
```javascript
// Verify response matches OpenAPI schema
const schema = pm.collectionVariables.get("openapiSchema");
const response = pm.response.json();
pm.test("Matches OpenAPI schema", () => {
  pm.expect(tv4.validate(response, JSON.parse(schema))).to.be.true;
});
```

## 10. Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| Hardcoded URLs | Use `{{baseUrl}}` environment variable |
| No assertions | Every request must have at least 2 tests |
| Tests in pre-request | Tests belong in Tests tab |
| No cleanup after create | DELETE resource in folder-level teardown |
| Copy-paste auth | Use collection-level pre-request |
| No environment separation | Use environments, never hardcode prod |

## 11. Related Resources

- Skills: `flask-api`, `behave-bdd`
- Prompts: `generate-api-test-suite`, `generate-api-contract-test`
- Agents: `test-architect`

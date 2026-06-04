---
name: Setup E2E Automation
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Bootstrap end-to-end automation from zero: choose framework, configure project, write first tests, integrate with CI/CD, and establish maintenance practices.
tags: [workflow, e2e, automation, playwright, cypress, selenium]
role: qa-automation-engineer
---

# Setup E2E Automation

Bootstrap an E2E automation suite from scratch.

## Prerequisites

- [ ] Target application URL and environment access
- [ ] Test data requirements identified
- [ ] CI/CD pipeline exists (or will be created)
- [ ] Framework decision made (see Step 1)

## Phase 1: Framework Selection

### Decision Matrix

| Criteria | Playwright | Cypress | Selenium |
|----------|-----------|---------|----------|
| Speed | Fast | Fast | Medium |
| Cross-browser | Chromium, Firefox, WebKit | Chromium, Firefox, WebKit | All |
| Mobile | Emulated | Limited | Appium bridge |
| API mocking | Native | `cy.intercept` | Limited |
| CI reliability | Excellent | Good | Requires grid |
| Team skill | TypeScript-friendly | JavaScript-focused | Multi-language |

### Recommendation
- **Greenfield web app** → Playwright
- **Existing Cypress team** → Cypress
- **Mobile + web** → Selenium + Appium
- **Component testing** → Playwright CT or Cypress CT

## Phase 2: Project Bootstrap

### Step 1: Initialize Project

```bash
# Playwright
npm init -y
npm install -D @playwright/test
npx playwright install

# Cypress
npm install -D cypress
npx cypress open  # Scaffold files

# Selenium (Java)
mvn archetype:generate -DgroupId=com.example \
  -DartifactId=e2e-tests -DarchetypeArtifactId=maven-archetype-quickstart
```

### Step 2: Directory Structure

```
e2e/
├── tests/
│   ├── auth/
│   │   └── login.spec.ts
│   ├── checkout/
│   │   └── purchase.spec.ts
│   └── fixtures/
│       └── users.json
├── pages/
│   ├── LoginPage.ts
│   └── CheckoutPage.ts
├── utils/
│   ├── test-helpers.ts
│   └── selectors.ts
├── playwright.config.ts   # or cypress.config.js
└── .env.ci
```

### Step 3: Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html'], ['junit', { outputFile: 'results.xml' }]],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
  ],
});
```

## Phase 3: First Tests

### Step 4: Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.getByLabel('Email').fill(email);
    await this.page.getByLabel('Password').fill(password);
    await this.page.getByRole('button', { name: 'Sign in' }).click();
  }

  async expectLoggedIn() {
    await expect(this.page).toHaveURL('/dashboard');
  }
}
```

### Step 5: Write Smoke Tests

```typescript
// tests/smoke.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('Smoke Tests', () => {
  test('homepage loads', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/My App/);
  });

  test('user can log in', async ({ page }) => {
    const login = new LoginPage(page);
    await login.goto();
    await login.login('user@test.com', 'password');
    await login.expectLoggedIn();
  });
});
```

### Step 6: Run Locally

```bash
# Playwright
npx playwright test --headed --workers=1

# Cypress
npx cypress open    # Interactive
npx cypress run     # Headless
```

## Phase 4: CI/CD Integration

### Step 7: GitHub Actions

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

### Step 8: Slack Notifications

```yaml
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {"text": "E2E tests failed on ${{ github.ref }}"}
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Phase 5: Maintenance Practices

### Step 9: Selector Strategy

| Priority | Strategy | Example |
|----------|----------|---------|
| 1 | `getByRole` | `getByRole('button', { name: 'Submit' })` |
| 2 | `getByTestId` | `getByTestId('checkout-form')` |
| 3 | `getByLabel` | `getByLabel('Email address')` |
| 4 | `getByText` | `getByText('Welcome')` |
| Avoid | CSS/XPath | `.btn-primary`, `//div[3]` |

### Step 10: Flakiness Prevention

- [ ] No `waitForTimeout` — use auto-wait
- [ ] Mock external APIs in tests
- [ ] Use fresh test data per run
- [ ] Parallelize with isolated accounts
- [ ] Retry failed tests in CI (max 2)

### Step 11: Documentation

- [ ] README with setup commands
- [ ] CONTRIBUTING.md for selectors and patterns
- [ ] Troubleshooting guide for common failures

## Verification Checklist

- [ ] Framework installed and running locally
- [ ] At least 5 smoke tests passing
- [ ] Page Object Model for main flows
- [ ] CI pipeline runs on every PR
- [ ] Artifacts uploaded on failure
- [ ] Team can run tests locally with one command
- [ ] Selector strategy documented

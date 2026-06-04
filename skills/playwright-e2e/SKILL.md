---
name: Playwright E2E
version: 1.0.0
author: Mathias Paulenko Echeverz
description: End-to-end testing with Playwright: codegen, selectors, auto-waiting, tracing, component testing, parallel execution, and CI/CD integration.
tags: [e2e, playwright, testing, automation, frontend]
role: qa-engineer
model: any
trigger: When the user asks about Playwright testing, E2E automation, browser testing, or web UI automation.
---

# Playwright E2E

Comprehensive skill for Playwright end-to-end testing.

## 1. Architecture

```
Playwright E2E Suite
├── playwright.config.ts      # Parallelism, retries, projects
├── tests/
│   ├── auth.spec.ts          # Page Object Model
│   ├── checkout.spec.ts
│   └── fixtures/
│       └── test.ts           # Custom fixtures + auth state
├── pages/
│   ├── LoginPage.ts          # POM classes
│   └── CartPage.ts
└── .auth/                    # Reused auth state
```

## 2. Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { open: 'never' }],
    ['junit', { outputFile: 'results.xml' }],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 12'] } },
  ],
});
```

## 3. Page Object Model

```typescript
// pages/LoginPage.ts
import { Page, Locator, expect } from '@playwright/test';

export class LoginPage {
  readonly username: Locator;
  readonly password: Locator;
  readonly submit: Locator;

  constructor(private page: Page) {
    this.username = page.getByTestId('username');
    this.password = page.getByTestId('password');
    this.submit = page.getByRole('button', { name: 'Sign in' });
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(user: string, pass: string) {
    await this.username.fill(user);
    await this.password.fill(pass);
    await this.submit.click();
  }
}
```

## 4. Selectors Strategy

| Strategy | Example | When to Use |
|----------|---------|-------------|
| `getByRole` | `getByRole('button', { name: 'Submit' })` | Primary — semantic |
| `getByTestId` | `getByTestId('checkout-form')` | Stable, dev-controlled |
| `getByLabel` | `getByLabel('Email address')` | Form accessibility |
| `getByText` | `getByText('Welcome')` | Visible text match |
| `getByPlaceholder` | `getByPlaceholder('Search...')` | Input hints |

**Avoid**: CSS/XPath selectors, text that changes with i18n, `nth-child`.

## 5. Auto-Waiting & Actions

```typescript
// Playwright auto-waits for elements to be actionable
await page.getByRole('button').click();      // waits up to 30s
await page.getByLabel('Email').fill('a@b.com'); // waits for editable
await page.getByRole('listbox').selectOption('Option 2');
await page.getByText('Confirm').hover();

// Manual waits (avoid if possible)
await page.waitForLoadState('networkidle');
await expect(page.getByText('Saved')).toBeVisible();
```

## 6. Fixtures & Auth State

```typescript
// fixtures/test.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

export const test = base.extend<{
  loginPage: LoginPage;
  adminPage: Page;
}>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  adminPage: async ({ browser }, use) => {
    const ctx = await browser.newContext({
      storageState: '.auth/admin.json',
    });
    await use(ctx.newPage());
    await ctx.close();
  },
});

// Setup auth once
// tests/auth.setup.ts
import { test as setup } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('admin@test.com');
  await page.getByLabel('Password').fill('secret');
  await page.getByRole('button').click();
  await page.waitForURL('/dashboard');
  await page.context().storageState({ path: '.auth/admin.json' });
});
```

## 7. Component Testing (Experimental)

```typescript
// Button.spec.tsx
import { test, expect } from '@playwright/experimental-ct-react';
import { Button } from './Button';

test('button renders and clicks', async ({ mount }) => {
  let clicked = false;
  const component = await mount(
    <Button onClick={() => (clicked = true)}>Click me</Button>
  );
  await component.click();
  expect(clicked).toBe(true);
});
```

## 8. Tracing & Debugging

```bash
# Run with trace
npx playwright test --trace on

# Show report
npx playwright show-report

# Open last trace
npx playwright show-trace trace.zip

# Inspector (step through)
npx playwright test --debug

# Codegen (record interactions)
npx playwright codegen http://localhost:3000
```

## 9. CI/CD Integration

```yaml
# .github/workflows/e2e.yml
- name: Run Playwright
  run: npx playwright test
- name: Upload report
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: playwright-report
    path: playwright-report/
```

## 10. Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|--------------|--------------|-----|
| `page.waitForTimeout(3000)` | Flaky, slow | Use auto-wait or `expect().toBeVisible()` |
| `page.click('.btn-primary')` | Brittle CSS | Use `getByRole` or `getByTestId` |
| No POM | Duplicated selectors | Extract Page Objects |
| Single browser project | Misses cross-browser bugs | Define chromium, firefox, webkit |
| Tests depend on order | Cascading failures | Isolated auth state per test |

## 11. Related Resources

- Prompts: `generate-e2e-test-suite` (QA), `generate-api-test-suite` (QA)
- Skills: `robot-framework`, `selenium-grid` (if needed)
- Agents: `test-architect`, `qa-automation-engineer`

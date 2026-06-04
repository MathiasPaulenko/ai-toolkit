---
name: WebdriverIO
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "WebdriverIO for E2E testing: Page Object Model, selectors, cross-browser execution, mobile emulation, visual regression, and CI/CD integration."
tags: [e2e, webdriverio, selenium, automation, cross-browser]
role: qa-automation-engineer
---

# WebdriverIO

Invoke when user asks about WebdriverIO, WDIO, or Selenium-based E2E automation with modern JavaScript.

## Core Principles

- **WebDriver protocol**: Standard, cross-browser, cross-platform.
- **Modern syntax**: `async/await`, TypeScript, built-in assertions.
- **Ecosystem**: Services, reporters, visual regression, mobile emulation.

## Installation & Setup

```bash
# Init project
npm create wdio@latest ./

# Select:
# - E2E Testing
# - On my local machine
# - Mocha
# - TypeScript
# - Chrome + Firefox
# - Spec reporter
# - Page Object Model
```

## wdio.conf.ts

```typescript
export const config: WebdriverIO.Config = {
  runner: 'local',
  specs: ['./features/**/*.feature'],
  exclude: [],
  maxInstances: 5,
  capabilities: [
    {
      browserName: 'chrome',
      'goog:chromeOptions': { args: ['--headless', '--disable-gpu'] },
    },
    {
      browserName: 'firefox',
      'moz:firefoxOptions': { args: ['-headless'] },
    },
  ],
  logLevel: 'warn',
  baseUrl: 'https://example.com',
  waitforTimeout: 10000,
  connectionRetryTimeout: 90000,
  connectionRetryCount: 3,
  services: ['selenium-standalone'],
  framework: 'mocha',
  reporters: ['spec', ['allure', { outputDir: 'allure-results' }]],

  // Page Object auto-import
  autoCompileOpts: {
    autoCompile: true,
    tsNodeOpts: { project: './tsconfig.json' },
  },
};
```

## Page Object Model

```typescript
// pages/Login.page.ts
export default class LoginPage {
  get inputUsername() { return $('#username'); }
  get inputPassword() { return $('#password'); }
  get btnSubmit() { return $('button[type="submit"]'); }
  get flashMessage() { return $('.flash'); }

  async open() {
    await browser.url('/login');
  }

  async login(username: string, password: string) {
    await this.inputUsername.setValue(username);
    await this.inputPassword.setValue(password);
    await this.btnSubmit.click();
  }

  async getFlashMessage(): Promise<string> {
    return this.flashMessage.getText();
  }
}
```

## Test Example

```typescript
// specs/login.spec.ts
import LoginPage from '../pages/Login.page';

describe('Login', () => {
  const loginPage = new LoginPage();

  it('should login with valid credentials', async () => {
    await loginPage.open();
    await loginPage.login('tomsmith', 'SuperSecretPassword!');
    await expect(loginPage.flashMessage).toHaveTextContaining(
      'You logged into a secure area!'
    );
  });

  it('should fail with invalid credentials', async () => {
    await loginPage.open();
    await loginPage.login('foo', 'bar');
    await expect(loginPage.flashMessage).toHaveTextContaining(
      'Your username is invalid!'
    );
  });
});
```

## Selectors

```typescript
// CSS
await $('#username');           // ID
await $('.login-form');         // Class
await $('input[type="email"]'); // Attribute

// XPath
await $("//button[contains(text(), 'Submit')]");

// Accessibility
await $('[aria-label="Search"]');
await $('aria/Search');         // WDIO aria selector

// Chain
await $('.cart').$('button.checkout');

// React (with resq)
await $('=LoginForm');
```

## Mobile Emulation

```typescript
// wdio.conf.ts
capabilities: [{
  browserName: 'chrome',
  'goog:chromeOptions': {
    mobileEmulation: { deviceName: 'iPhone 14 Pro Max' },
  },
}];
```

## Visual Regression

```bash
npm install -D wdio-image-comparison-service
```

```typescript
// wdio.conf.ts
services: [
  ['image-comparison', {
    baselineFolder: './baseline',
    formatImageName: '{tag}-{width}x{height}',
    screenshotPath: './screenshots',
    savePerInstance: true,
    autoSaveBaseline: true,
  }],
];
```

```typescript
// test
it('should match homepage', async () => {
  await browser.url('/');
  expect(await browser.checkScreen('homepage', {})).toEqual(0);
});
```

## CI/CD Integration

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npx wdio run wdio.conf.ts
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: wdio-screenshots
          path: screenshots/
```

## Cucumber Integration

```bash
npm install -D @wdio/cucumber-framework
```

```typescript
// features/login.feature
Feature: Login
  Scenario: Valid login
    Given I open the login page
    When I enter valid credentials
    Then I should see the secure area
```

```typescript
// step-definitions/login.steps.ts
import { Given, When, Then } from '@wdio/cucumber-framework';
import LoginPage from '../pages/Login.page';

const loginPage = new LoginPage();

Given('I open the login page', async () => {
  await loginPage.open();
});

When('I enter valid credentials', async () => {
  await loginPage.login('tomsmith', 'SuperSecretPassword!');
});

Then('I should see the secure area', async () => {
  await expect(loginPage.flashMessage).toHaveTextContaining('secure');
});
```

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| `browser.pause(3000)` | Use explicit waits: `waitForDisplayed`, `waitForClickable` |
| XPath with indices | Use CSS or stable `data-testid` |
| One massive spec file | Split by domain/page |
| No baseline for visual tests | Auto-save baseline in CI on main branch |
| Testing in only Chrome | Add Firefox, Safari in pipeline |

## Quick Reference

| Command | Purpose |
|---------|---------|
| `browser.url('/path')` | Navigate |
| `$('#id').click()` | Click element |
| `$('#id').setValue('text')` | Type text |
| `$('#id').getText()` | Get text |
| `$('#id').isDisplayed()` | Check visibility |
| `browser.saveScreenshot('name.png')` | Screenshot |
| `browser.execute(() => window.scrollTo(0,0))` | Execute JS |

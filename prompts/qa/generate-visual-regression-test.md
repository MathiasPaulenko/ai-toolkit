---
name: Generate Visual Regression Test
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Set up visual regression testing with Percy, Chromatic, or Storybook. Covers component snapshots, diff thresholds, CI integration, and baseline management.
tags: [visual-regression, percy, chromatic, storybook, ui-testing]
role: qa-engineer
model: any
trigger: When the user asks about visual regression testing, snapshot testing, UI diff detection, or Percy/Chromatic setup.
---

# Generate Visual Regression Test

Set up visual regression testing for UI components and pages.

## Tools Comparison

| Tool | Best For | CI Integration | Cost |
|------|----------|---------------|------|
| **Chromatic** | Storybook components | Native | Paid |
| **Percy** | Full-page + component | CLI + GitHub Action | Paid |
| **Loki** | Storybook (self-hosted) | CLI | Free |
| **BackstopJS** | Full-page (self-hosted) | CLI | Free |

## Chromatic Setup (Storybook)

```bash
# Install
npm install --save-dev chromatic

# Add to package.json scripts
"chromatic": "chromatic --project-token=TOKEN"

# In .github/workflows/chromatic.yml
- name: Publish to Chromatic
  uses: chromaui/action@v1
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
    onlyChangedStories: true
```

```javascript
// Component story with interaction test
import { within, userEvent } from '@storybook/testing-library';

export const HoverState = {
  render: () => <Button>Hover me</Button>,
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.hover(canvas.getByRole('button'));
  },
};
```

## Percy Setup (Cypress/Playwright)

```javascript
// cypress/e2e/visual.cy.js
import '@percy/cypress';

describe('Visual Regression', () => {
  it('homepage matches baseline', () => {
    cy.visit('/');
    cy.percySnapshot('Homepage');
  });

  it('modal at mobile breakpoint', () => {
    cy.viewport(375, 667);
    cy.get('[data-testid=open-modal]').click();
    cy.percySnapshot('Modal - Mobile', { widths: [375] });
  });
});
```

## Configuration Best Practices

```yaml
# .percy.yml
version: 2
snapshot:
  widths: [375, 768, 1280]
  minHeight: 1024
  percyCSS: |
    .dynamic-date { visibility: hidden !important; }
  enableJavaScript: true
```

## Baseline Management

1. **Main branch = baseline**: Only update baseline on merge to main
2. **PR diffs**: Review visual diffs in PR checks before merging
3. **Intentional changes**: Approve new baseline when UI intentionally changes
4. **Ignore dynamic content**: Hide timestamps, ads, user-generated content

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| No viewport breakpoints | Test at mobile, tablet, desktop |
| Dynamic content not hidden | Use `percyCSS` to hide timestamps |
| Testing entire page instead of components | Component-level snapshots are faster |
| Ignoring flaky diffs | Set threshold or stabilize animations |

## Output

Provide:
1. Tool recommendation based on tech stack
2. Setup commands and config
3. Example snapshot test code
4. CI integration steps
5. Baseline management workflow

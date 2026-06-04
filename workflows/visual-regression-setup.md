---
name: Visual Regression Setup
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Set up visual regression testing for UI components and pages. Configure Chromatic, Percy, or Loki; establish baselines; integrate with CI; and manage intentional UI changes.
tags: [workflow, visual-regression, chromatic, percy, storybook]
role: qa-engineer
---

# Visual Regression Setup

Bootstrap visual regression testing for a project.

## Prerequisites

- [ ] UI components exist (Storybook preferred)
- [ ] Design system or style guide documented
- [ ] CI/CD pipeline active
- [ ] Team agrees on baseline management process

## Phase 1: Tool Selection

### Decision Matrix

| Tool | Best For | Setup Effort | Cost | Self-Hosted |
|------|----------|-------------|------|-------------|
| **Chromatic** | Storybook components | Low | Paid | No |
| **Percy** | Full pages + components | Low | Paid | No |
| **Loki** | Storybook (free) | Medium | Free | Yes |
| **BackstopJS** | Full pages (free) | Medium | Free | Yes |

### Recommendation
- **Storybook + budget** → Chromatic
- **No Storybook + budget** → Percy
- **Open source / budget constraints** → Loki or BackstopJS

## Phase 2: Installation

### Chromatic (Storybook)

```bash
# Install
npm install --save-dev chromatic

# Add token to CI secrets
# CHROMATIC_PROJECT_TOKEN=xxx

# Add script
# package.json: "chromatic": "chromatic --exit-zero-on-changes"
```

```yaml
# .github/workflows/chromatic.yml
name: Chromatic
on: push
jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - name: Publish to Chromatic
        uses: chromaui/action@v1
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          onlyChangedStories: true
          exitZeroOnChanges: true
          exitOnceUploaded: true
```

### Percy (Any framework)

```bash
# Install
npm install --save-dev @percy/cli @percy/cypress

# Add to Cypress test
cy.percySnapshot('Homepage');
```

```yaml
# .github/workflows/percy.yml
- run: npx percy exec -- cypress run
  env:
    PERCY_TOKEN: ${{ secrets.PERCY_TOKEN }}
```

### Loki (Self-hosted)

```bash
npm install --save-dev loki
npx loki init

# .loki.config.js
module.exports = {
  configurations: {
    chrome: { target: 'chrome.docker', width: 1366, height: 768 },
    chromeMobile: { target: 'chrome.docker', preset: 'iPhone 7' },
  },
};
```

## Phase 3: Baseline Management

### Step 1: Initial Baseline

1. Merge baseline-capturing PR to `main`
2. Tool captures all component/page snapshots
3. Review and approve baseline images
4. Lock baseline — only intentional changes update it

### Step 2: PR Workflow

```
Developer pushes PR
    ↓
CI runs visual tests
    ↓
If diffs detected → PR check fails
    ↓
Designer reviews diffs in tool UI
    ↓
Approve (intentional) or Reject (regression)
    ↓
Merge updates baseline
```

### Step 3: Approval Rules

| Change Type | Who Approves | Notes |
|-------------|-------------|-------|
| Pixel shifts (< 5px) | Auto-approve | Font rendering, sub-pixel |
| Content changes | Developer | Dynamic data, timestamps |
| Component redesign | Designer | Intentional UI update |
| Cross-browser diff | QA Lead | Known browser differences |

## Phase 4: Configuration

### Chromatic Settings

```javascript
// .storybook/preview.js
export const parameters = {
  chromatic: {
    delay: 300,              // Wait for animations
    diffThreshold: 0.2,      // Ignore < 0.2% pixel diff
    viewports: [320, 768, 1280],
  },
};
```

### Percy Settings

```yaml
# .percy.yml
version: 2
snapshot:
  widths: [375, 768, 1280, 1440]
  minHeight: 1024
  percyCSS: |
    .dynamic-date { visibility: hidden !important; }
    .ad-banner { display: none !important; }
  enableJavaScript: true
```

## Phase 5: Component Testing

### Storybook Stories for Visual Regression

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  component: Button,
  parameters: {
    chromatic: { disableSnapshot: false },
  },
};

export default meta;

export const Primary: StoryObj = {
  args: { variant: 'primary', children: 'Click me' },
};

export const Loading: StoryObj = {
  args: { variant: 'primary', loading: true },
  parameters: {
    chromatic: { delay: 500 }, // Wait for spinner
  },
};

export const Disabled: StoryObj = {
  args: { variant: 'primary', disabled: true },
};
```

## Phase 6: Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Flaky diffs | Animations not settled | Add `delay` or disable animations |
| Timestamp diffs | Dynamic dates in UI | Hide with CSS or mock dates |
| Font rendering diff | OS/browser differences | Use consistent Docker image |
| Content shifts | Async loading | Wait for `networkidle` before capture |
| False positives | Anti-aliasing | Increase `diffThreshold` slightly |

## Verification Checklist

- [ ] Tool installed and CI running
- [ ] Initial baseline captured on main
- [ ] PR workflow documented
- [ ] Approval rules agreed with design team
- [ ] Dynamic content hidden or mocked
- [ ] Team trained on diff review process
- [ ] Baseline update process defined

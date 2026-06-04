---
name: Generate Accessibility Audit
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Conduct WCAG 2.2 AA accessibility audits using automated tools (axe, Lighthouse) and manual checks. Covers screen readers, keyboard navigation, color contrast, and ARIA.
tags: [accessibility, a11y, wcag, axe, audit]
role: qa-engineer
model: any
trigger: When the user asks about accessibility testing, WCAG audit, screen reader testing, or a11y compliance.
---

# Generate Accessibility Audit

Conduct a comprehensive WCAG 2.2 AA accessibility audit.

## Automated Tools

### axe-core (Recommended)
```javascript
// Cypress
import 'cypress-axe';

describe('Accessibility', () => {
  it('has no detectable a11y violations', () => {
    cy.visit('/');
    cy.injectAxe();
    cy.checkA11y(null, {
      runOnly: {
        type: 'tag',
        values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']
      }
    });
  });
});
```

### Playwright + axe
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('homepage should not have a11y issues', async ({ page }) => {
  await page.goto('/');
  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();
  expect(accessibilityScanResults.violations).toEqual([]);
});
```

### Lighthouse CI
```bash
npm install -g @lhci/cli
lhci autorun --config=lighthouserc.json
```

```json
// lighthouserc.json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:accessibility": ["error", { "minScore": 0.95 }]
      }
    }
  }
}
```

## Manual Checklist (WCAG 2.2 AA)

### Perceivable
- [ ] **1.1.1** Non-text content has alt text
- [ ] **1.4.3** Contrast ratio ≥ 4.5:1 for normal text
- [ ] **1.4.6** Contrast ratio ≥ 7:1 for enhanced (AAA)
- [ ] **1.4.10** Reflow — content readable at 400% zoom
- [ ] **1.4.11** Non-text contrast ≥ 3:1 for UI components

### Operable
- [ ] **2.1.1** All functionality available via keyboard
- [ ] **2.1.2** No keyboard traps
- [ ] **2.4.3** Focus order is logical
- [ ] **2.4.7** Focus indicator is visible
- [ ] **2.5.5** Target size ≥ 44×44 CSS pixels (WCAG 2.5.5 AAA, good practice for AA)

### Understandable
- [ ] **3.1.1** Page language identified
- [ ] **3.2.4** Components with same function have same labels
- [ ] **3.3.1** Error identification is clear
- [ ] **3.3.3** Error suggestions provided

### Robust
- [ ] **4.1.2** Name, role, value programmatically determinable
- [ ] **4.1.3** Status messages announced without focus change

## Screen Reader Testing

### NVDA (Windows, free)
- Download from nvaccess.org
- Test with Firefox or Chrome
- Key commands: `Insert + F7` (elements list), `H` (headings), `T` (tables)

### VoiceOver (macOS/iOS)
- `Cmd + F5` to toggle
- `Ctrl + Option + U` (rotor)
- Test on Safari primarily

### Common Issues
| Issue | Screen Reader Behavior | Fix |
|-------|------------------------|-----|
| Missing `alt` | Announces "image" or filename | Add descriptive alt |
| Empty headings | Confusing navigation | Remove or add content |
| Form without labels | "Edit, blank" | Use `<label>` or `aria-label` |
| Tables without headers | Reads cell-by-cell without context | Use `<th scope="col">` |
| Modal without focus trap | User tabs out of modal | `aria-modal="true"` + JS focus trap |

## Color Contrast

```bash
# axe CLI for quick check
axe https://example.com --tags wcag2aa
```

### Manual Check
- Deuteranopia (red-green): Use Chrome DevTools → Rendering → Emulate vision deficiencies
- Total colorblindness: Ensure UI doesn't rely solely on color

## ARIA Best Practices

```html
<!-- Correct: Landmark roles -->
<nav aria-label="Main">
<main>
<aside aria-label="Related articles">
<footer>

<!-- Correct: Live regions -->
<div aria-live="polite" aria-atomic="true">
  3 items added to cart
</div>

<!-- Avoid: Redundant roles -->
<button role="button">  <!-- Don't do this -->
```

## Audit Report Template

```markdown
## Accessibility Audit: [Page/App]

### Summary
- **WCAG Version**: 2.2
- **Level**: AA
- **Date**: [Date]
- **Tools**: axe-core, Lighthouse, NVDA

### Automated Results
| Tool | Violations | Warnings | Score |
|------|------------|----------|-------|
| axe | 3 | 7 | — |
| Lighthouse | — | — | 87/100 |

### Violations Found
| Rule | Severity | Element | Fix |
|------|----------|---------|-----|
| color-contrast | Serious | `.btn-secondary` | Change to #767676 |
| missing-label | Critical | `#search` | Add `<label>` |

### Manual Checks
- [ ] Keyboard navigation — [Pass/Needs Fix]
- [ ] Screen reader — [Pass/Needs Fix]
- [ ] Zoom 400% — [Pass/Needs Fix]
- [ ] Colorblind simulation — [Pass/Needs Fix]

### Remediation Plan
| Priority | Issue | Owner | Due |
|----------|-------|-------|-----|
| P0 | Missing form labels | Dev | Sprint X |
| P1 | Low contrast buttons | Design | Sprint X+1 |
```

## Output

Provide:
1. Tool configuration for automated testing
2. Manual checklist results
3. Violation report with fixes
4. Remediation plan with priorities

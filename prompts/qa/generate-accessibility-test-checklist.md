---
name: Generate Accessibility Test Checklist
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a WCAG 2.1 AA accessibility test checklist for web applications. Covers keyboard navigation, screen readers, color contrast, and focus management.
tags: [qa, accessibility, a11y, wcag, screen-reader, keyboard]
role: qa-engineer
model: any
trigger: When the user asks for accessibility tests, a11y audit, WCAG compliance, or screen reader testing.
---

# Generate Accessibility Test Checklist

Generate a comprehensive WCAG 2.1 AA accessibility test checklist for any web application or component.

## Perceivable (WCAG 1.x)

- [ ] All images have meaningful `alt` text
- [ ] Decorative images have empty `alt=""`
- [ ] Videos have captions and transcripts
- [ ] Color is not the only means of conveying info
- [ ] Text contrast ratio ≥ 4.5:1 (normal), ≥ 3:1 (large)
- [ ] UI component contrast ≥ 3:1 against background
- [ ] Text can be resized to 200% without loss
- [ ] Content reflows correctly at 1280px × 1024px (400% zoom)

## Operable (WCAG 2.x)

- [ ] All functionality available via keyboard (Tab, Enter, Space, Arrow keys)
- [ ] No keyboard traps (can Tab out of any element)
- [ ] Focus order is logical and visible
- [ ] Skip links present for repetitive content
- [ ] No flashing content > 3Hz
- [ ] Form errors identified and described
- [ ] Sufficient time limits with option to extend

## Understandable (WCAG 3.x)

- [ ] Page language declared (`lang` attribute)
- [ ] Form labels associated with inputs
- [ ] Error messages are specific and helpful
- [ ] Consistent navigation across pages
- [ ] Input assistance for errors

## Robust (WCAG 4.x)

- [ ] Valid HTML markup
- [ ] ARIA roles used correctly (no redundant roles)
- [ ] Name, role, value accessible to assistive tech
- [ ] Status messages announced without focus change

## Screen Reader Tests (NVDA / JAWS / VoiceOver)

- [ ] Page title announced on navigation
- [ ] Headings hierarchy is logical (h1 → h2 → h3)
- [ ] Tables have proper `scope` and `headers`
- [ ] Live regions announce dynamic updates
- [ ] Modal dialogs trap focus and announce role

## Automated Tools

- axe-core, WAVE, Lighthouse a11y audit
- Pa11y for CI/CD integration
- Storybook a11y addon for component testing

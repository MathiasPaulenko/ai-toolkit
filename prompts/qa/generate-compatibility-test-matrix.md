---
name: Generate Compatibility Test Matrix
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a browser, OS, and device compatibility test matrix for web and mobile applications.
tags: [qa, compatibility, cross-browser, browser-matrix, responsive]
role: qa-engineer
model: any
trigger: When the user asks for browser compatibility, cross-browser testing, device matrix, or responsive testing.
---

# Generate Compatibility Test Matrix

Generate a comprehensive compatibility test matrix for web and mobile applications.

## Browser Matrix (Web)

| Browser | Version | OS | Priority | Notes |
|---------|---------|----|----------|-------|
| Chrome | Latest, Latest-1 | Windows 11, macOS | P0 | Primary browser |
| Firefox | Latest, Latest-1 | Windows 11, macOS | P0 | |
| Safari | Latest | macOS, iOS | P0 | WebKit engine |
| Edge | Latest | Windows 11 | P1 | Chromium-based |
| Chrome | Latest | Android 14 | P1 | Mobile |
| Safari | Latest | iOS 17 | P1 | Mobile |
| Firefox | Latest | Android 14 | P2 | Lower usage |
| Samsung Internet | Latest | Android 14 | P2 | Samsung devices |

## Screen Resolution Matrix

| Resolution | Aspect Ratio | Device Type | Priority |
|------------|-------------|-------------|----------|
| 1920×1080 | 16:9 | Desktop | P0 |
| 1366×768 | 16:9 | Laptop | P0 |
| 375×667 | 9:16 | iPhone SE | P1 |
| 390×844 | 9:19.5 | iPhone 14 | P1 |
| 360×800 | 9:20 | Android | P1 |
| 768×1024 | 3:4 | iPad | P1 |
| 2560×1440 | 16:9 | Desktop | P2 |

## Test Scenarios per Combination

For each (Browser, OS, Resolution) cell:

- [ ] Layout does not break (no horizontal scroll on mobile)
- [ ] All interactive elements clickable/tappable
- [ ] Fonts render correctly (no fallback issues)
- [ ] Images load and are appropriately sized
- [ ] Modals/popovers position correctly
- [ ] Forms submit correctly
- [ ] Print styles work (if applicable)

## Tooling

- **Automated**: BrowserStack, Sauce Labs, Playwright cross-browser
- **Visual regression**: Percy, Chromatic, BackstopJS
- **Manual**: Test on physical devices for gestures

## Output Template

```markdown
| Browser | OS | Resolution | Status | Issues |
|---------|----|------------|--------|--------|
| Chrome 120 | Win11 | 1920x1080 | ✅ Pass | — |
| Safari 17 | macOS | 1440x900 | ⚠️ Minor | Dropdown misaligned |
```

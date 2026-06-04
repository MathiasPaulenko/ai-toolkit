---
name: Mobile Testing Rules
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Rules for testing mobile applications: iOS and Android, gestures, real device vs emulator trade-offs, Appium best practices, and CI integration.
tags: [mobile, testing, appium, ios, android]
role: mobile-testing-rules
type: rules
language: en
---

# Mobile Testing Rules

## 1. Device Strategy

### Rule 1.1: Test on Real Devices
- Emulators are acceptable for development, but critical flows must be validated on real devices.
- Real devices catch issues emulators miss: memory pressure, thermal throttling, carrier-specific behavior.

### Rule 1.2: Cover Form Factors
- Test on at least one phone and one tablet per OS.
- Include notch/dynamic island and foldable devices if target audience uses them.

### Rule 1.3: OS Version Coverage
- Support N (latest), N-1, and N-2 for each platform.
- Update within 6 months of major OS release.

## 2. Gestures & Interactions

### Rule 2.1: Test All Touch Gestures
- Tap, long press, swipe (all directions), pinch, zoom, rotate.
- Multi-touch interactions if app supports them.

### Rule 2.2: Hardware Button Behavior
- Back button (Android), home gesture, app switcher, volume, power.
- Interrupts: incoming call, notification, low battery popup.

### Rule 2.3: Orientation Changes
- Test all primary flows in portrait and landscape.
- Verify state preservation after orientation change.

## 3. Appium Specific

### Rule 3.1: Prefer Accessibility IDs
- Use `content-desc` (Android) and `accessibilityLabel` (iOS) as primary locators.
- Add IDs specifically for automation if UI doesn't have them.

### Rule 3.2: No XPath for Large Lists
- XPath is slow on mobile; use ID or class chain instead.
- For lists, locate parent then iterate children natively.

### Rule 3.3: Handle Context Switching
- WebView contexts require explicit switch in hybrid apps.
- Verify context list before attempting switch.

```python
# Switch to WebView
contexts = driver.contexts
driver.switch_to.context(contexts[-1])  # Usually last is WebView

# Switch back to native
driver.switch_to.context('NATIVE_APP')
```

## 4. Environment & Data

### Rule 4.1: Use Debug Builds for Automation
- Debug builds must include test hooks: clear data, mock locations, disable animations.
- Release builds must be tested separately for performance and behavior parity.

### Rule 4.2: Network Condition Testing
- Test on Wi-Fi, 4G, 3G, and offline.
- Simulate high latency (300ms+) and packet loss.

### Rule 4.3: Location & Permissions
- Test with location enabled, disabled, and mock locations.
- Verify permission dialogs and "Don't ask again" behavior.

## 5. Performance

### Rule 5.1: Cold Start Time
- Measure time from tap to first meaningful paint.
- Target: < 3 seconds on mid-range devices.

### Rule 5.2: Memory Leaks
- Monitor memory usage during 30-minute usage session.
- Memory should return to baseline after navigation away from heavy screens.

### Rule 5.3: Battery Drain
- Profile CPU and network usage during typical session.
- High battery drain = frequent wake-locks, GPS polling, or unoptimized animations.

## 6. CI/CD

### Rule 6.1: Parallel Device Execution
- Use device farms (BrowserStack, Sauce Labs, Firebase) for parallel execution.
- Group tests by OS to optimize farm allocation.

### Rule 6.2: Artifact Collection
- Capture screenshot, video, and device logs on failure.
- Include app logs (logcat for Android, sysdiagnose for iOS).

### Rule 6.3: Emulator Smoke in CI
- Run smoke tests on emulators for every PR.
- Full regression on real devices nightly.

## 7. Accessibility

### Rule 7.1: Screen Reader Testing
- Verify all UI elements have meaningful labels.
- Test navigation order with TalkBack (Android) and VoiceOver (iOS).

### Rule 7.2: Font Scaling
- Test at 100%, 150%, and 200% system font sizes.
- UI must not clip, overlap, or become unusable.

### Rule 7.3: Color & Contrast
- Verify touch targets meet minimum size (48dp Android, 44pt iOS).
- Colorblind-friendly palettes (deuteranopia simulation).

## Checklist

- [ ] Real device testing for critical flows
- [ ] Form factor coverage (phone + tablet)
- [ ] OS versions N, N-1, N-2
- [ ] All gestures tested
- [ ] Hardware interrupts handled
- [ ] Accessibility labels present
- [ ] Screen reader navigation works
- [ ] Network conditions varied
- [ ] Cold start < 3 seconds
- [ ] CI runs on emulators + nightly on real devices

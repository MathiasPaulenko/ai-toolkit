---
name: Generate Mobile Test Strategy
version: 1.0.0
author: Mathias Paulenko Echeverz
description: Generate a mobile testing strategy covering iOS/Android, device fragmentation, gestures, offline mode, push notifications, and app store compliance.
tags: [qa, mobile, android, ios, appium, device-fragmentation]
role: qa-engineer
model: any
trigger: When the user asks for mobile testing, app testing, device compatibility, or Appium tests.
---

# Generate Mobile Test Strategy

Generate a comprehensive mobile testing strategy for iOS and Android applications.

## Device Matrix

| OS | Version | Device Examples | Priority |
|----|---------|-----------------|----------|
| Android | 14, 13, 12 | Pixel 7, Samsung S23, Xiaomi | High |
| Android | 11, 10 | Samsung A53, budget devices | Medium |
| iOS | 17, 16 | iPhone 15, 14, 13 | High |
| iOS | 15 | iPhone 12, SE | Medium |
| Tablet | iPadOS 17, Android 14 | iPad Pro, Galaxy Tab | Low |

## Test Areas

### 1. Installation & Launch
- Fresh install, update, reinstall
- Cold start, warm start time (< 3s ideal)
- First-run onboarding flow
- Deep linking from push/email

### 2. UI / UX
- Orientation change (portrait ↔ landscape)
- Dark mode / light mode
- Font size accessibility (largest font)
- Notch / safe area handling
- Gesture conflicts (swipe back vs in-app swipe)

### 3. Connectivity
- Offline mode (airplane, tunnel)
- Slow network (2G, 3G simulation)
- Intermittent connectivity
- Background/foreground transitions

### 4. Platform-Specific
- Permissions (camera, location, notifications, storage)
- Biometric auth (Face ID, fingerprint)
- Battery optimization (Doze mode on Android)
- Background app refresh

### 5. Notifications
- Push notification delivery
- Rich notifications (images, actions)
- Badge count accuracy
- Notification grouping

## Automation (Appium)

```python
# Android test with UIAutomator2
from appium import webdriver

desired_caps = {
    "platformName": "Android",
    "appium:deviceName": "Pixel 7",
    "appium:app": "/path/to/app.apk",
    "appium:automationName": "UiAutomator2"
}

driver = webdriver.Remote("http://localhost:4723", desired_caps)
```

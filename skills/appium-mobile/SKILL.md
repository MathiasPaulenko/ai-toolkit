---
name: appium-mobile
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Mobile automation with Appium: iOS and Android, gestures, device farms (BrowserStack, Sauce Labs), parallel execution, and CI/CD."
tags: [mobile, appium, ios, android, automation]
role: qa-engineer
model: any
trigger: When the user asks about Appium, mobile testing, iOS automation, Android automation, or mobile device farms.
---

# Appium Mobile

Mobile test automation with Appium for iOS and Android.

## 1. Architecture

```
Appium Test Suite
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ conftest.py         # Driver fixtures
â”‚   â”œâ”€â”€ test_login.py
â”‚   â”œâ”€â”€ test_checkout.py
â”‚   â””â”€â”€ pages/
â”‚       â”œâ”€â”€ base_page.py
â”‚       â”œâ”€â”€ login_page.py
â”‚       â””â”€â”€ home_page.py
â”œâ”€â”€ capabilities/
â”‚   â”œâ”€â”€ android.json        # Device configs
â”‚   â””â”€â”€ ios.json
â””â”€â”€ pytest.ini
```

## 2. Driver Setup

```python
# conftest.py
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

@pytest.fixture
def android_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Pixel_7_API_34"
    options.app = "./app/build/app-debug.apk"
    options.automation_name = "UiAutomator2"
    options.no_reset = False

    driver = webdriver.Remote("http://localhost:4723", options=options)
    yield driver
    driver.quit()

@pytest.fixture
def ios_driver():
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.device_name = "iPhone 15"
    options.platform_version = "17.0"
    options.app = "./app/build/ios-simulator.app"
    options.automation_name = "XCUITest"

    driver = webdriver.Remote("http://localhost:4723", options=options)
    yield driver
    driver.quit()
```

## 3. Page Object Model

```python
# pages/login_page.py
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_username(self):
        return self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "username")

    def find_password(self):
        return self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "password")

    def find_login_button(self):
        return self.driver.find_element(AppiumBy.ID, "com.example.app:id/login")

    def login(self, user, password):
        self.find_username().send_keys(user)
        self.find_password().send_keys(password)
        self.find_login_button().click()

    def is_logged_in(self):
        return self.wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "welcome")
            )
        )
```

## 4. Locators

| Strategy | Android | iOS | Best Practice |
|----------|---------|-----|---------------|
| `ACCESSIBILITY_ID` | `content-desc` | `accessibilityLabel` | Preferred â€” stable |
| `ID` | `resource-id` | `name` (limited) | Good for unique IDs |
| `XPATH` | Any XML path | Any XML path | Slow; use sparingly |
| `CLASS_NAME` | `android.widget.Button` | `XCUIElementTypeButton` | For type filtering |
| `IOS_PREDICATE` | N/A | `type == 'XCUIElementTypeButton'` | iOS-specific, fast |
| `ANDROID_UIAUTOMATOR` | `new UiSelector().text("OK")` | N/A | Android-specific |

## 5. Gestures & Interactions

```python
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

# Tap
TouchAction(driver).tap(x=100, y=200).perform()

# Swipe / Scroll
def swipe(driver, start, end):
    action = TouchAction(driver)
    action.press(x=start[0], y=start[1])
    action.wait(ms=500)
    action.move_to(x=end[0], y=end[1])
    action.release().perform()

# W3C Actions (modern)
actions = ActionBuilder(driver)
pointer = PointerInput("touch", "finger")
actions.pointer_action.move_to_location(100, 500)
actions.pointer_action.pointer_down()
actions.pointer_action.move_to_location(100, 200)
actions.pointer_action.pointer_up()
actions.perform()

# Wait for element
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (AppiumBy.ACCESSIBILITY_ID, "loading-complete")
    )
)
```

## 6. Device Farms

### BrowserStack
```python
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Samsung Galaxy S23"
options.app = "bs://<app-id>"

# bs-local for local testing
from browserstack.local import Local
local = Local()
local.start({"key": BROWSERSTACK_KEY})

driver = webdriver.Remote(
    f"https://{USER}:{KEY}@hub-cloud.browserstack.com/wd/hub",
    options=options
)
```

### Sauce Labs
```python
# Replace with your Sauce Labs credentials
# Endpoint format: ondemand.saucelabs.com/wd/hub
driver = webdriver.Remote(
    "https://ondemand.example.com/wd/hub",
    options=options
)
```

## 7. Parallel Execution

```bash
# pytest-xdist with device-specific ports
pytest -n 2 --dist loadgroup \
  --capabilities '{"udid": "emulator-5554"}' \
  --capabilities '{"udid": "emulator-5556"}'
```

## 8. CI/CD

```yaml
# .github/workflows/mobile-tests.yml
name: Mobile Tests
on: [push]
jobs:
  android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          script: |
            adb install app/build/app-debug.apk
            pytest tests/ --driver=android
```

## 9. Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| XPath without accessibility IDs | Add `content-desc` / `accessibilityLabel` |
| Hardcoded waits | Use `WebDriverWait` with expected conditions |
| Testing on emulators only | Run on real devices via cloud farm |
| No app state cleanup | Uninstall or clear data between tests |
| Ignoring rotation | Test landscape + portrait |
| No offline scenarios | Toggle airplane mode / network throttling |

## 10. Related Resources

- Skills: `android-native`, `playwright-e2e`
- Prompts: `generate-mobile-test-strategy`

---
name: XCTest iOS
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Native iOS testing with XCTest: unit tests, UI automation, performance, snapshot testing, parallel execution, and CI/CD with Xcode Cloud."
tags: [ios, xctest, swift, mobile, unit-testing]
role: mobile-tester
---

# XCTest iOS

Invoke when user asks about XCTest, iOS testing, Swift unit tests, or native iOS automation.

## Core Principles

- **First-party**: Apple's framework, no third-party dependencies.
- **Unified**: Unit, UI, and performance tests in one framework.
- **Tooling**: Xcode integration, parallel testing, code coverage, CI with Xcode Cloud.

## Project Setup

```swift
// In Xcode: File > New > Target > UI Testing Bundle
// Or add test target to Package.swift

// Package.swift
targets: [
  .target(name: "MyApp"),
  .testTarget(
    name: "MyAppTests",
    dependencies: ["MyApp"]
  ),
]
```

## Unit Tests (XCTestCase)

```swift
import XCTest
@testable import MyApp

final class CalculatorTests: XCTestCase {
  var calculator: Calculator!

  override func setUp() {
    super.setUp()
    calculator = Calculator()
  }

  override func tearDown() {
    calculator = nil
    super.tearDown()
  }

  func testAddition() {
    XCTAssertEqual(calculator.add(2, 3), 5)
  }

  func testDivisionByZeroThrows() {
    XCTAssertThrowsError(try calculator.divide(10, 0)) { error in
      XCTAssertEqual(error as? CalculatorError, .divisionByZero)
    }
  }

  // Async test
  func testFetchUser() async throws {
    let user = try await api.fetchUser(id: 1)
    XCTAssertEqual(user.name, "Alice")
  }

  // Parameterized with enum
  func testSquares() {
    let cases = [(input: 2, expected: 4), (input: 3, expected: 9)]
    for c in cases {
      XCTAssertEqual(calculator.square(c.input), c.expected)
    }
  }
}
```

## UI Tests (XCUIApplication)

```swift
import XCTest

final class LoginUITests: XCTestCase {
  let app = XCUIApplication()

  override func setUp() {
    continueAfterFailure = false
    app.launch()
  }

  func testSuccessfulLogin() {
    let emailField = app.textFields["emailTextField"]
    let passwordField = app.secureTextFields["passwordTextField"]
    let loginButton = app.buttons["loginButton"]
    let welcomeLabel = app.staticTexts["welcomeLabel"]

    emailField.tap()
    emailField.typeText("alice@test.com")

    passwordField.tap()
    passwordField.typeText("password123")

    loginButton.tap()

    XCTAssertTrue(welcomeLabel.waitForExistence(timeout: 5))
    XCTAssertEqual(welcomeLabel.label, "Welcome, Alice")
  }

  func testInvalidPasswordShowsError() {
    app.textFields["emailTextField"].tap()
    app.textFields["emailTextField"].typeText("alice@test.com")

    app.secureTextFields["passwordTextField"].tap()
    app.secureTextFields["passwordTextField"].typeText("wrong")

    app.buttons["loginButton"].tap()

    let errorAlert = app.alerts["Error"]
    XCTAssertTrue(errorAlert.waitForExistence(timeout: 3))
  }
}
```

## Performance Tests

```swift
func testTableScrollPerformance() throws {
  measure(
    metrics: [
      XCTClockMetric(),
      XCTCPUMetric(),
      XCTMemoryMetric(),
    ]
  ) {
    let table = app.tables.element(boundBy: 0)
    table.swipeUp(velocity: .fast)
    table.swipeDown(velocity: .fast)
  }
}
```

## Snapshot Testing (Point-Free)

```swift
// Package.swift: .package(url: "https://github.com/pointfreeco/swift-snapshot-testing", from: "1.15.0")

import SnapshotTesting
import XCTest

func testLoginScreen() {
  let view = LoginView()
  let controller = UIHostingController(rootView: view)
  
  assertSnapshot(
    of: controller,
    as: .image(on: .iPhone13Pro)
  )
}
```

## Parallel Test Execution

```bash
# xcodebuild with parallel testing
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  -parallel-testing-enabled YES \
  -maximum-parallel-testing-workers 4
```

## CI/CD (Xcode Cloud)

```yaml
# ci_post_clone.sh
#!/bin/bash
brew install swiftlint
swiftlint lint --reporter json > swiftlint.json
```

```yaml
# ci_post_xcodebuild.sh
#!/bin/bash
# Upload coverage to external service
bash <(curl -s https://codecov.io/bash) -J 'MyApp'
```

## Accessibility Testing

```swift
func testAccessibilityLabels() {
  let emailField = app.textFields["emailTextField"]
  XCTAssertEqual(
    emailField.label,
    "Email Address"
  )
}
```

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| `sleep(3)` in UI tests | Use `waitForExistence(timeout:)` |
| Accessing views by index | Use `accessibilityIdentifier` |
| Testing only on iPhone | Add iPad targets |
| No tearDown | Clean state between tests |
| Hardcoded device names in CI | Use `xcrun simctl list` dynamically |

## Quick Reference

| API | Purpose |
|-----|---------|
| `XCUIApplication().launch()` | Launch app |
| `.tap()` | Tap element |
| `.typeText("text")` | Type text |
| `.swipeUp()` / `.swipeDown()` | Scroll |
| `.pinch(withScale: 2)` | Pinch zoom |
| `.twoFingerTap()` | Two-finger tap |
| `.waitForExistence(timeout:)` | Wait for element |
| `XCTAssertTrue` / `XCTAssertEqual` | Assertions |

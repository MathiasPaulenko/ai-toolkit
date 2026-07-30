# YAML Session Format Specification

> Complete specification of the wavexis YAML session format for recording and replaying browser sessions.

## Overview

A wavexis session is a YAML file that describes a sequence of browser actions. Sessions can be recorded interactively, generated from action lists, or written manually. They are replayed deterministically in CI or local environments.

## File Structure

```yaml
session:
  name: Session Name
  description: Brief description of what the session does
  recorded_at: "2024-01-15T10:30:00Z"
  viewport: "1280x720"
  user_agent: "Mozilla/5.0 ..."  # optional
  base_url: "https://example.com"  # optional, used with --base-url override

actions:
  - action1
  - action2
  - ...
```

## Session Metadata

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `str` | yes | Human-readable session name |
| `description` | `str` | no | Brief description |
| `recorded_at` | `str` | no | ISO 8601 timestamp of recording |
| `viewport` | `str` | no | Viewport size (WxH) |
| `user_agent` | `str` | no | Custom user agent |
| `base_url` | `str` | no | Default origin for URL replacement |

## Action Types

### navigate

Navigate to a URL.

```yaml
- navigate:
    url: https://example.com/page
    wait_until: networkidle  # load, domcontentloaded, networkidle
    timeout: 30000  # ms
    referer: https://example.com  # optional
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `url` | `str` | required | Target URL |
| `wait_until` | `str` | `load` | Wait condition |
| `timeout` | `int` | `30000` | Navigation timeout (ms) |
| `referer` | `str` | None | Referer header |

### click

Click an element.

```yaml
- click:
    selector: "#button"
    button: left  # left, right, middle
    click_count: 1
    delay: 0  # ms between mousedown and mouseup
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `selector` | `str` | required | CSS selector |
| `button` | `str` | `left` | Mouse button |
| `click_count` | `int` | `1` | Number of clicks |
| `delay` | `int` | `0` | Delay between mousedown/mouseup (ms) |

### input

Type text into a field.

```yaml
- input:
    selector: "#textfield"
    value: "hello world"
    delay: 50  # ms between keystrokes
    clear: true  # clear field before typing
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `selector` | `str` | required | CSS selector |
| `value` | `str` | required | Text to type |
| `delay` | `int` | `0` | Delay between keystrokes (ms) |
| `clear` | `bool` | `true` | Clear field before typing |

### select

Select an option in a dropdown.

```yaml
- select:
    selector: "#country"
    value: "US"
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `selector` | `str` | required | CSS selector |
| `value` | `str` | required | Option value |

### keypress

Press a keyboard key.

```yaml
- keypress:
    key: Enter
    selector: "#input"  # optional: focus element first
    modifiers:  # optional
      - Control
      - Shift
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `key` | `str` | required | Key name (Enter, Tab, Escape, etc.) |
| `selector` | `str` | None | Focus element before pressing |
| `modifiers` | `array` | `[]` | Modifier keys (Control, Shift, Alt, Meta) |

### scroll

Scroll the page or an element.

```yaml
- scroll:
    x: 0
    y: 500
    selector: ".scrollable"  # optional: scroll within element
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `x` | `int` | `0` | Horizontal scroll pixels |
| `y` | `int` | `0` | Vertical scroll pixels |
| `selector` | `str` | None | Scroll within specific element |

### wait_for

Wait for an element to reach a state.

```yaml
- wait_for:
    selector: ".results"
    state: visible  # visible, hidden, attached, detached
    timeout: 10000  # ms
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `selector` | `str` | required | CSS selector |
| `state` | `str` | `visible` | Element state to wait for |
| `timeout` | `int` | `30000` | Wait timeout (ms) |

### screenshot

Take a screenshot.

```yaml
- screenshot:
    full_page: false
    selector: ".element"  # optional: element screenshot
    output: ./screenshots/page.png
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `full_page` | `bool` | `false` | Capture full page |
| `selector` | `str` | None | Capture specific element |
| `output` | `str` | `screenshot.png` | Output file path |

### assert

Assert page state.

```yaml
- assert:
    title: "== Welcome"
    url: "matches https://example\\.com"
    text: "contains Sign In"
    text: "!contains Error"
```

Multiple assertions in one action must all pass. See `ci-assertions.md` in the CI/CD skill for operator reference.

### upload

Upload a file.

```yaml
- upload:
    selector: "#file-input"
    path: ./test-files/document.pdf
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `selector` | `str` | required | File input CSS selector |
| `path` | `str` | required | File path to upload |

### submit

Submit a form.

```yaml
- submit:
    selector: "#form"
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `selector` | `str` | required | Form CSS selector |

## Complete Example

```yaml
session:
  name: E-commerce Checkout
  description: Complete checkout flow from cart to confirmation
  recorded_at: "2024-01-15T14:20:00Z"
  viewport: "1280x720"

actions:
  - navigate:
      url: https://example.com/cart
      wait_until: networkidle
  - assert:
      text: "contains Shopping Cart"
  - click:
      selector: "#checkout-button"
  - wait_for:
      selector: "#shipping-form"
      state: visible
  - input:
      selector: "#full-name"
      value: "Alice Smith"
  - input:
      selector: "#address"
      value: "123 Main St"
  - input:
      selector: "#city"
      value: "Anytown"
  - select:
      selector: "#state"
      value: "CA"
  - input:
      selector: "#zip"
      value: "12345"
  - click:
      selector: "#continue-to-payment"
  - wait_for:
      selector: "#payment-form"
      state: visible
  - input:
      selector: "#card-number"
      value: "4111111111111111"
  - input:
      selector: "#expiry"
      value: "12/25"
  - input:
      selector: "#cvv"
      value: "123"
  - click:
      selector: "#place-order"
  - wait_for:
      selector: ".order-confirmation"
      state: visible
      timeout: 30000
  - assert:
      url: "matches https://example\\.com/order/.*"
      text: "contains Order Confirmed"
  - screenshot:
      full_page: true
      output: ./screenshots/confirmation.png
```

## Environment Variables

Session YAML supports environment variable substitution:

```yaml
- input:
    selector: "#username"
    value: "${TEST_USERNAME}"
- input:
    selector: "#password"
    value: "${TEST_PASSWORD}"
```

Variables are resolved from the environment at replay time. Undefined variables cause an error.

## References

- [wavexis CLI documentation](https://github.com/MathiasPaulenko/wavexis)
- `skills/wavexis-ci-cd/references/ci-assertions.md` — Assertion operators reference

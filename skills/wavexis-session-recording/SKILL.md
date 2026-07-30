---
name: WaveXis Session Recording
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Record and replay browser sessions with wavexis. Interactive recording, YAML session format, replay in CI."
tags: [record-replay, session, yaml, automation]
trigger: When the user asks about recording browser sessions with wavexis, needs interactive recording, wants to replay sessions in CI, or needs to understand the YAML session format.
---

# WaveXis Session Recording

## Description

Record and replay browser sessions with wavexis — capture real user interactions interactively, generate sessions from action lists, and replay recorded sessions in CI environments for deterministic test automation.

## When to Invoke

- Recording interactive browser sessions for testing
- Generating session YAML from action lists
- Replaying recorded sessions in CI
- Converting manual testing into automated tests
- Debugging flaky tests by replaying recorded sessions

## Prerequisites

- `pip install wavexis[cdp]`
- Chrome or Edge installed
- Basic familiarity with wavexis CLI (see `wavexis-cli-automation` skill)

## Interactive Recording

### record --interactive

Launch a browser and record all user interactions in real time:

```bash
wavexis record --interactive https://example.com --output session.yml
```

This opens a Chrome window. Every click, input, scroll, and navigation is captured into a YAML session file.

### Interactive recording with options

```bash
wavexis record --interactive https://example.com \
    --output login-session.yml \
    --viewport 1920x1080 \
    --timeout 120000
```

### What gets recorded

| Interaction | Captured as | YAML action |
|-------------|-------------|-------------|
| Click | selector + coordinates | `click` |
| Type text | selector + value | `input` |
| Navigate | URL | `navigate` |
| Scroll | coordinates | `scroll` |
| Select dropdown | selector + value | `select` |
| Key press | key name | `keypress` |
| Form submit | selector | `submit` |
| File upload | selector + path | `upload` |

### Stopping recording

- **Manual stop**: Press `Ctrl+C` in terminal or close the browser window.
- **Auto stop**: After `--timeout` ms or when `--stop-url` is reached.
- **Selector stop**: When `--stop-selector` becomes visible.

```bash
wavexis record --interactive https://example.com/login \
    --output session.yml \
    --stop-selector ".dashboard" \
    --timeout 60000
```

### record --interactive options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--output` | `str` | `session.yml` | Output session file |
| `--viewport` | `str` | `1280x720` | Browser viewport size |
| `--timeout` | `int` | `60000` | Max recording time in ms |
| `--stop-selector` | `str` | None | Stop when selector appears |
| `--stop-url` | `str` | None | Stop when URL matches |
| `--headless` | `flag` | off | Record headless (no visible window) |
| `--stealth` | `flag` | off | Enable stealth mode |
| `--user-agent` | `str` | None | Custom user agent |
| `--cookie` | `str` | None | Pre-set cookies (name=value) |
| `--header` | `str` | None | Pre-set headers |

## Non-Interactive Recording

### record with --actions

Generate a session YAML from a list of actions without launching a browser:

```bash
wavexis record https://example.com \
    --actions "navigate,click:#login,input:#username:admin,input:#password:secret,click:#submit" \
    --output login-session.yml
```

### record from action file

```bash
wavexis record https://example.com \
    --actions-file ./actions.txt \
    --output session.yml
```

### Action file format

```
# One action per line
# Format: action:selector:value

navigate:https://example.com/login
click:#username
input:#username:admin@example.com
click:#password
input:#password:secret
click:#submit
wait_for:.dashboard
screenshot:full_page
```

### Action syntax

| Action | Syntax | Example |
|--------|--------|---------|
| `navigate` | `navigate:url` | `navigate:https://example.com` |
| `click` | `click:selector` | `click:#submit` |
| `input` | `input:selector:value` | `input:#email:test@example.com` |
| `select` | `select:selector:value` | `select:#country:US` |
| `keypress` | `keypress:key` | `keypress:Enter` |
| `scroll` | `scroll:x:y` | `scroll:0:500` |
| `wait_for` | `wait_for:selector` | `wait_for:.results` |
| `screenshot` | `screenshot:mode` | `screenshot:full_page` |
| `submit` | `submit:selector` | `submit:#form` |
| `upload` | `upload:selector:path` | `upload:#file:./test.pdf` |

## Session Replay

### replay command

Replay a recorded session:

```bash
wavexis replay ./session.yml --output result.json
```

### replay with assertions

```bash
wavexis replay ./login-session.yml \
    --assert 'url matches "https://example\.com/dashboard"' \
    --assert 'text contains "Welcome"' \
    --output result.json
```

### replay with screenshots

```bash
wavexis replay ./session.yml \
    --screenshot \
    --output-dir ./screenshots/
```

### replay in headless mode

```bash
wavexis replay ./session.yml \
    --headless \
    --output result.json
```

### replay with speed control

```bash
# Slow down replay (useful for debugging)
wavexis replay ./session.yml \
    --speed 0.5 \
    --output result.json

# Speed up replay
wavexis replay ./session.yml \
    --speed 2.0 \
    --output result.json
```

### replay options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--headless` | `flag` | off | Run headless |
| `--speed` | `float` | `1.0` | Replay speed multiplier (0.1-10.0) |
| `--screenshot` | `flag` | off | Take screenshot after each action |
| `--output-dir` | `str` | `./output/` | Screenshot output directory |
| `--assert` | `str` | None | Assertion expression (can repeat) |
| `--output` | `str` | stdout | Result output file |
| `--viewport` | `str` | `1280x720` | Browser viewport |
| `--stealth` | `flag` | off | Enable stealth mode |
| `--timeout` | `int` | `60000` | Per-action timeout in ms |
| `--stop-on-error` | `flag` | off | Stop replay on first error |

### replay output

```json
{
  "session": "login-session.yml",
  "actions": [
    {
      "action": "navigate",
      "url": "https://example.com/login",
      "status": "PASS",
      "time": 1234
    },
    {
      "action": "input",
      "selector": "#username",
      "value": "admin@example.com",
      "status": "PASS",
      "time": 45
    },
    {
      "action": "click",
      "selector": "#submit",
      "status": "PASS",
      "time": 120
    }
  ],
  "summary": {
    "total_actions": 3,
    "passed": 3,
    "failed": 0,
    "total_time": 1399,
    "status": "PASS"
  }
}
```

## YAML Session Format

### Basic structure

```yaml
session:
  name: Login Flow
  description: Record a login session
  recorded_at: "2024-01-15T10:30:00Z"
  viewport: "1280x720"

actions:
  - navigate:
      url: https://example.com/login
      wait_until: networkidle
  - input:
      selector: "#username"
      value: admin@example.com
  - input:
      selector: "#password"
      value: secret
  - click:
      selector: "#submit"
  - wait_for:
      selector: ".dashboard"
      timeout: 10000
  - assert:
      url: "matches https://example\\.com/dashboard"
      text: "contains Welcome"
  - screenshot:
      full_page: true
```

### Action reference

#### navigate

```yaml
- navigate:
    url: https://example.com
    wait_until: networkidle  # load, domcontentloaded, networkidle
    timeout: 30000
```

#### click

```yaml
- click:
    selector: "#button"
    button: left  # left, right, middle
    click_count: 1
    delay: 0  # ms between clicks
```

#### input

```yaml
- input:
    selector: "#textfield"
    value: "text to type"
    delay: 0  # ms between keystrokes
    clear: true  # clear field before typing
```

#### select

```yaml
- select:
    selector: "#dropdown"
    value: "option-value"
```

#### keypress

```yaml
- keypress:
    key: Enter  # Enter, Tab, Escape, ArrowDown, etc.
    selector: "#input"  # optional: focus element first
```

#### scroll

```yaml
- scroll:
    x: 0
    y: 500
    selector: ".scrollable"  # optional: scroll within element
```

#### wait_for

```yaml
- wait_for:
    selector: ".results"
    state: visible  # visible, hidden, attached, detached
    timeout: 10000
```

#### screenshot

```yaml
- screenshot:
    full_page: false
    selector: ".element"  # optional: element screenshot
    output: ./screenshots/page.png
```

#### assert

```yaml
- assert:
    title: "== Welcome"
    url: "matches https://example\\.com"
    text: "contains Sign In"
    text: "!contains Error"
```

#### upload

```yaml
- upload:
    selector: "#file-input"
    path: ./test-files/document.pdf
```

#### submit

```yaml
- submit:
    selector: "#form"
```

## CI Integration

### GitHub Actions with session replay

```yaml
name: Session Replay Tests

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  replay:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install wavexis
        run: pip install wavexis[cdp]

      - name: Install Chrome
        run: |
          wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
          sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
          sudo apt-get update && sudo apt-get install -y google-chrome-stable

      - name: Replay login session
        run: |
          wavexis replay ./sessions/login.yml \
            --headless \
            --assert 'url matches "https://staging\.example\.com/dashboard"' \
            --assert 'text contains "Welcome"' \
            --output login-result.json

      - name: Replay form fill session
        run: |
          wavexis replay ./sessions/form-fill.yml \
            --headless \
            --assert 'text contains "Submitted"' \
            --output form-result.json

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: session-results
          path: |
            login-result.json
            form-result.json
```

### Environment-specific replay

```bash
# Replay against staging
wavexis replay ./sessions/login.yml \
    --base-url https://staging.example.com \
    --headless \
    --output result.json

# Replay against production
wavexis replay ./sessions/login.yml \
    --base-url https://production.example.com \
    --headless \
    --output result.json
```

The `--base-url` option replaces the recorded URL's origin with the specified base URL.

## Best Practices

- **Record at the target viewport** — use `--viewport` matching your CI environment.
- **Use stable selectors** — prefer `#id`, `[data-testid]`, or `.class` over XPath.
- **Add assertions after recording** — edit the YAML to add `assert` actions.
- **Use `wait_for` between actions** — ensure dynamic content is loaded before clicking.
- **Store sessions in git** — version-control session YAML files.
- **Use `--base-url` for environment switching** — don't hardcode URLs.
- **Replay headless in CI** — use `--headless` for faster, reliable runs.
- **Use `--speed` for debugging** — slow down replay to see what's happening.
- **Name sessions descriptively** — `login.yml`, `checkout.yml`, `form-fill.yml`.
- **Break long sessions into shorter ones** — smaller sessions are easier to debug.

## Common Pitfalls

- **Selectors changed since recording** — UI changes break replay; update sessions after UI updates.
- **Missing `wait_for`** — dynamic content may not be loaded when the next action fires.
- **Hardcoded URLs** — use `--base-url` to switch environments without re-recording.
- **Recording too much** — long sessions are fragile; record focused flows.
- **Not handling popups** — unexpected modals or popups can break replay.
- **Timing-dependent actions** — use `wait_for` instead of fixed delays.
- **Headless differences** — some sites behave differently headless; test with `--headless` before CI.
- **Speed too fast** — `--speed 10.0` can cause race conditions; use moderate speeds.

## References

- `references/session-yaml-format.md` — YAML session format specification
- `assets/templates/record-login.yml` — Login recording template
- `assets/templates/record-form-fill.yml` — Form fill recording template
- [wavexis CLI documentation](https://github.com/MathiasPaulenko/wavexis)

# Multi-Action YAML — Syntax, Actions, and Examples

> Complete guide to wavexis multi-action YAML configs for chained browser operations.

## Overview

Multi-action YAML lets you chain multiple browser actions in a single session. This avoids the overhead of launching a browser for each command and enables complex workflows like login + scrape + screenshot sequences.

## Basic Structure

```yaml
actions:
  - <action_type>: <value>
  - <action_type>:
      <param1>: <value1>
      <param2>: <value2>
```

## Action Types

### `navigate`

Navigate to a URL.

```yaml
- navigate: https://example.com
```

With options:

```yaml
- navigate:
    url: https://example.com
    wait_until: networkidle
    timeout: 30000
```

### `screenshot`

Take a screenshot.

```yaml
- screenshot: {}
```

With options:

```yaml
- screenshot:
    full_page: true
    output: page-full.png
    selector: "#content"
    format: png
    quality: 90
    delay: 1000
    wait_for: "#loaded"
```

### `pdf`

Generate a PDF.

```yaml
- pdf:
    output: page.pdf
    paper: a4
    landscape: false
    scale: 1.0
    print_background: true
```

### `scrape`

Scrape page content.

```yaml
- scrape:
    selector: "article"
    format: markdown
    output: content.md
```

### `eval`

Evaluate JavaScript.

```yaml
- eval: document.title
```

With assertion:

```yaml
- eval:
    expression: document.title
    assert: "== Expected Title"
```

### `click`

Click an element.

```yaml
- click:
    selector: "#button"
    delay: 500
```

### `type`

Type text into a field.

```yaml
- type:
    selector: "#username"
    text: admin@example.com
    delay: 50
    clear: true
```

### `fill`

Fill a field (instant, no keystroke simulation).

```yaml
- fill:
    selector: "#password"
    text: secretpass
```

### `key`

Press a key.

```yaml
- key:
    key: Enter
    modifiers: [Shift]
```

### `hover`

Hover over an element.

```yaml
- hover:
    selector: "#menu"
```

### `select`

Select an option from a dropdown.

```yaml
- select:
    selector: "select.country"
    value: "US"
```

### `drag`

Drag from one element to another.

```yaml
- drag:
    from: "#source"
    to: "#target"
```

### `tap`

Tap an element (touch).

```yaml
- tap:
    selector: "#button"
```

### `wait`

Wait for a specified duration.

```yaml
- wait:
    duration: 2000
```

### `wait_for`

Wait for an element to appear.

```yaml
- wait_for:
    selector: "#loaded"
    visible: true
    timeout: 10000
```

### `cookies`

Cookie operations.

```yaml
# Get cookies
- cookies: {}

# Set cookie
- cookies:
    set:
      name: session
      value: abc123
      domain: example.com

# Delete cookie
- cookies:
    delete: session

# Clear all
- cookies:
    clear: true
```

### `headers`

Get response headers.

```yaml
- headers: {}
```

### `user_agent`

Set custom user agent.

```yaml
- user_agent: "Mozilla/5.0 (Custom Agent)"
```

### `block`

Block requests matching a pattern.

```yaml
- block:
    pattern: "*/ads/*"
```

### `throttle`

Throttle network.

```yaml
- throttle:
    download: 50000
    upload: 25000
    latency: 400
```

### `intercept`

Intercept requests.

```yaml
- intercept:
    pattern: "*/api/*"
    block: true
```

### `mock`

Mock a response.

```yaml
- mock:
    pattern: "*/api/users"
    body: '{"users":[]}'
    status: 200
    headers:
      Content-Type: application/json
```

### `modify`

Modify request headers.

```yaml
- modify:
    pattern: "*/api/*"
    headers:
      X-Custom: value
```

### `modify_response`

Modify response body.

```yaml
- modify_response:
    pattern: "*/api/*"
    body: '{"modified":true}'
    status: 200
```

### `har`

Capture HAR.

```yaml
- har:
    output: network.har
    timeout: 30000
```

### `emulation`

Device emulation.

```yaml
- emulation:
    type: device
    device: iphone-15
```

Viewport:

```yaml
- emulation:
    type: viewport
    width: 375
    height: 812
```

Geolocation:

```yaml
- emulation:
    type: geolocation
    latitude: 35.6762
    longitude: 139.6503
```

Dark mode:

```yaml
- emulation:
    type: dark_mode
    enabled: true
```

### `perf`

Performance metrics.

```yaml
- perf:
    mode: metrics
    output: metrics.json
```

### `cwv`

Core Web Vitals.

```yaml
- cwv:
    budget:
      lcp_ms: 2500
      cls: 0.1
      inp_ms: 200
    output: cwv-report.json
```

### `a11y`

Accessibility tree.

```yaml
- a11y:
    format: json
    output: a11y.json
```

### `axe`

axe-core audit.

```yaml
- axe:
    output: axe-report.json
```

### `visual_diff`

Visual regression.

```yaml
- visual_diff:
    baseline: baseline.png
    output: diff.png
    threshold: 0.01
```

### `scroll`

Scroll the page.

```yaml
- scroll:
    x: 0
    y: 500
```

### `scroll_to`

Scroll to an element.

```yaml
- scroll_to:
    selector: "#footer"
```

### `reload`

Reload the page.

```yaml
- reload: {}
```

### `back`

Go back in history.

```yaml
- back: {}
```

### `forward`

Go forward in history.

```yaml
- forward: {}
```

### `tabs`

Tab management.

```yaml
# Open new tab
- tabs:
    action: new
    url: https://example.org

# Switch to tab
- tabs:
    action: switch
    index: 1

# Close tab
- tabs:
    action: close
    index: 1

# List tabs
- tabs:
    action: list
```

### `raw`

Raw CDP/BiDi method call.

```yaml
- raw:
    method: Page.printToPDF
    params:
      paperWidth: 8.5
      paperHeight: 11
```

### `download`

Download a file.

```yaml
- download:
    selector: "#download-link"
    output: ./downloads/
```

### `dialog`

Handle a dialog.

```yaml
- dialog:
    action: accept
    text: "OK"
```

### `permissions`

Set permissions.

```yaml
- permissions:
    name: geolocation
    state: granted
```

### `security`

Get security state.

```yaml
- security: {}
```

### `screencast`

Record a screencast.

```yaml
- screencast:
    output: ./screencast/
    duration: 10
    fps: 10
    format: gif
```

### `lighthouse`

Run Lighthouse audit.

```yaml
- lighthouse:
    output: lighthouse.json
    categories: [performance, accessibility]
    form_factor: mobile
```

### `trace`

Tracing.

```yaml
- trace:
    action: start
- navigate: https://example.com
- trace:
    action: stop
    output: trace.json
```

### `console`

Capture console output.

```yaml
- console:
    output: console.log
```

### `events`

Capture browser events.

```yaml
- events:
    types: [Page.loadEventFired, Network.responseReceived]
    output: events.json
    duration: 10000
```

### `storage`

Storage operations.

```yaml
- storage:
    type: local
    action: set
    key: theme
    value: dark
```

### `indexeddb`

IndexedDB operations.

```yaml
- indexeddb:
    action: list
```

### `sw`

Service worker operations.

```yaml
- sw:
    action: list
```

### `extension_install`

Install a browser extension.

```yaml
- extension_install:
    path: /path/to/extension/
```

### `webauthn`

WebAuthn virtual authenticator.

```yaml
- webauthn:
    action: add
    protocol: ctap2
    transport: internal
    has_resident_key: true
    has_user_verification: true
```

### `cast`

Cast operations.

```yaml
- cast:
    action: start
    sink_name: "Chromecast"
```

### `bluetooth`

Bluetooth emulation.

```yaml
- bluetooth:
    action: emulate
    manufacturer_name: "Test"
```

### `animation`

Animation control.

```yaml
- animation:
    action: set_playback_rate
    rate: 2.0
```

### `pref`

Browser preferences.

```yaml
- pref:
    action: set
    key: download.default_directory
    value: /tmp/downloads
```

---

## Complete Examples

### Login and screenshot

```yaml
actions:
  - navigate: https://example.com/login
  - wait_for:
      selector: "#username"
      visible: true
  - fill:
      selector: "#username"
      text: admin@example.com
  - fill:
      selector: "#password"
      text: secretpass
  - click:
      selector: "#submit"
  - wait_for:
      selector: ".dashboard"
      visible: true
      timeout: 10000
  - screenshot:
      full_page: true
      output: dashboard.png
```

### Scrape multiple pages

```yaml
actions:
  - navigate: https://example.com/page1
  - scrape:
      selector: "article"
      format: markdown
      output: page1.md
  - navigate: https://example.com/page2
  - scrape:
      selector: "article"
      format: markdown
      output: page2.md
  - navigate: https://example.com/page3
  - scrape:
      selector: "article"
      format: markdown
      output: page3.md
```

### Performance audit with budget

```yaml
actions:
  - navigate: https://example.com
  - cwv:
      budget:
        lcp_ms: 2500
        cls: 0.1
        inp_ms: 200
      output: cwv.json
  - perf:
      mode: trace
      duration: 5000
      output: trace.json
  - lighthouse:
      output: lighthouse.json
      categories: [performance, accessibility, seo]
```

### Stealth scraping with block and mock

```yaml
actions:
  - block:
      pattern: "*/ads/*"
  - mock:
      pattern: "*/api/geo"
      body: '{"country":"US"}'
      status: 200
  - navigate: https://protected-site.com
  - wait_for:
      selector: ".content"
      timeout: 15000
  - scrape:
      selector: ".content"
      format: markdown
      output: content.md
  - screenshot:
      full_page: true
      output: proof.png
```

### CI assertion pipeline

```yaml
actions:
  - navigate: https://staging.example.com
  - eval:
      expression: document.title
      assert: "== My App - Staging"
  - eval:
      expression: document.querySelector("#status").textContent
      assert: "contains Operational"
  - screenshot:
      output: ci-screenshot.png
  - cwv:
      budget:
        lcp_ms: 2500
        cls: 0.1
        inp_ms: 200
```

### Multi-tab scraping

```yaml
actions:
  - navigate: https://example.com
  - scrape:
      selector: "h1"
      output: tab0.txt
  - tabs:
      action: new
      url: https://example.org
  - scrape:
      selector: "h1"
      output: tab1.txt
  - tabs:
      action: switch
      index: 0
  - scrape:
      selector: "h1"
      output: tab0-again.txt
```

### Network interception and HAR

```yaml
actions:
  - intercept:
      pattern: "*/api/*"
      block: false
  - navigate: https://example.com
  - har:
      output: network.har
      timeout: 30000
  - inspect: {}
```

### Visual regression

```yaml
actions:
  - navigate: https://example.com
  - wait_for:
      selector: "#loaded"
      visible: true
  - screenshot:
      output: current.png
  - visual_diff:
      baseline: baseline.png
      output: diff.png
      threshold: 0.01
```

---

## Execution Options

### Watch mode

Re-run the config when the file changes:

```bash
wavexis multi config.yml --watch
```

### Dry run

Show actions without executing:

```bash
wavexis multi config.yml --dry-run
```

### Parallel execution

Run independent actions in parallel:

```bash
wavexis multi config.yml --parallel
```

### Caching

Cache results for repeated runs:

```bash
wavexis multi config.yml --cache-ttl 60
```

Cacheable actions: `screenshot`, `dom`, `scrape`, `eval`, `cookies`, `headers`.
Cache key: URL + action type + params hash.

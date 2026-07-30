---
name: wavexis-cli-automation
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Browser automation with wavexis CLI: screenshots, PDFs, scraping, REPL, multi-action YAML, stealth mode, serve mode, performance audits, and CI assertions. 130+ commands, CDP + BiDi backends."
tags: [wavexis, cli-automation, browser-automation, screenshot, scraping]
trigger: When the user asks about wavexis CLI commands, browser automation from the command line, multi-action YAML configs, stealth scraping, serve mode, REPL, or CI assertions with wavexis.
---

# WaveXis CLI Automation

## Description

wavexis is a command-line tool for browser automation. It wraps cdpwave (Chrome DevTools Protocol) and bidiwave (WebDriver BiDi) behind a unified CLI with 130+ top-level commands and 480+ sub-commands. No Node.js, no Chromium download — it uses your existing Chrome or Edge installation directly.

## When to Invoke

- Running browser automation tasks from the command line
- Taking screenshots, generating PDFs, or scraping page content
- Creating multi-action YAML configs for chained browser operations
- Using stealth mode for anti-bot scraping
- Setting up serve mode (HTTP API + WebSocket streaming)
- Writing CI assertions with `--assert` flags
- Using the interactive REPL for live browser sessions
- Batch processing multiple URLs
- Recording and replaying browser sessions
- Capturing HAR files or performance metrics

---

## 1. Installation

### CDP backend (default, recommended)

```bash
pip install wavexis[cdp]
```

### BiDi backend

```bash
pip install wavexis[bidi]
```

### Serve mode + image extras

```bash
pip install wavexis[cdp,serve,image]
```

### Docker

```bash
docker run -p 8080:8080 ghcr.io/mathiaspaulenko/wavexis:latest
```

### Verify installation

```bash
wavexis install_check
```

---

## 2. Backend Selection

wavexis supports two backends with full feature parity:

| Backend | Flag | Browsers | Driver needed |
|---------|------|----------|---------------|
| CDP (default) | `--backend cdp` | Chrome, Edge, Brave, Chromium | No |
| BiDi | `--backend bidi` | Chrome, Firefox, Edge | Yes (ChromeDriver / geckodriver) |

Switch backend per command:

```bash
# CDP (default)
wavexis screenshot https://example.com -o out.png

# BiDi
wavexis screenshot https://example.com -o out.png --backend bidi
```

---

## 3. Core Commands

### Screenshot

```bash
# Basic screenshot
wavexis screenshot https://example.com -o out.png

# Full-page screenshot
wavexis screenshot https://example.com -o full.png --full-page

# Screenshot of a specific element
wavexis screenshot https://example.com -o el.png --selector "h1"

# Screenshot with device emulation
wavexis screenshot https://example.com -o mobile.png --device iphone-15
```

### PDF

```bash
# Generate a PDF
wavexis pdf https://example.com -o out.pdf

# Specific paper size
wavexis pdf https://example.com -o out.pdf --paper a4
```

### Scrape

```bash
# Scrape page content
wavexis scrape https://example.com --selector "article"

# Scrape with text output
wavexis scrape https://example.com --selector "div.content" --format text
```

### Evaluate JavaScript

```bash
# Evaluate expression
wavexis eval https://example.com -e "document.title"

# With CI assertion
wavexis eval https://example.com -e "document.title" --assert "== Expected Title"
```

### Navigate

```bash
wavexis navigate https://example.com
```

---

## 4. REPL (Interactive Mode)

Launch a non-headless browser and execute commands in real time:

```bash
wavexis repl
```

Supported REPL commands:

| Command | Description |
|---------|-------------|
| `navigate <url>` | Navigate to URL |
| `screenshot` | Take screenshot |
| `eval <expr>` | Evaluate JavaScript |
| `click <selector>` | Click element |
| `type <selector> <text>` | Type text into element |
| `fill <selector> <text>` | Fill input field |
| `hover <selector>` | Hover over element |
| `key <key>` | Press key |
| `cookies` | Show cookies |
| `url` | Show current URL |
| `title` | Show page title |
| `wait <seconds>` | Wait |
| `back` | Go back |
| `forward` | Go forward |
| `reload` | Reload page |
| `help` | Show help |
| `exit` / `quit` | Exit REPL |

---

## 5. Multi-Action YAML

Chain multiple actions in sequence on a single browser session:

```bash
wavexis multi config.yml
```

### YAML config format

```yaml
actions:
  - navigate: https://example.com
  - screenshot:
      full_page: true
  - eval: document.title
  - click: "#login"
  - type:
      selector: "#username"
      text: admin@example.com
  - screenshot: {}
```

### Multi-action options

```bash
# Watch mode — re-run on file change
wavexis multi config.yml --watch

# Dry run — show actions without executing
wavexis multi config.yml --dry-run

# Parallel execution
wavexis multi config.yml --parallel

# Action caching — cache results for 60 seconds
wavexis multi config.yml --cache-ttl 60
```

Cacheable actions: `screenshot`, `dom`, `scrape`, `eval`, `cookies`, `headers`. Cache is keyed by URL, action type, and params hash.

### Init wizard

Generate a `wavexis.yaml` config interactively:

```bash
wavexis init
```

Or with flags:

```bash
wavexis init -t multi-step -u https://example.com -s "#login" --text "admin" -o config.yaml
```

List available templates:

```bash
wavexis init --list
```

Templates: `screenshot`, `pdf`, `scrape`, `eval`, `multi-step`, `cookies`, `har`.

---

## 6. Stealth Mode

Hide headless browser indicators for scraping protected sites:

```bash
# Global flag — applies to all commands
wavexis --stealth screenshot https://example.com -o out.png
wavexis --stealth scrape https://protected-site.com --selector "article"
```

Stealth mode hides:

- `navigator.webdriver`
- Fakes plugins, languages, chrome runtime
- Fakes WebGL vendor/renderer
- Fakes permissions API
- Fakes `navigator.connection`, `hardwareConcurrency`, `deviceMemory`, `platform`

Works with both CDP and BiDi backends.

---

## 7. CI Assertions

Use `--assert` with `eval` to create CI gates:

```bash
# Equality check — exit 0 if title matches, 1 otherwise
wavexis eval https://example.com -e "document.title" --assert "== Expected Title"

# Inequality
wavexis eval https://example.com -e "document.title" --assert "!= Old Title"

# Substring
wavexis eval https://example.com -e "document.body.innerText" --assert "contains Welcome"

# Regex
wavexis eval https://example.com -e "document.title" --assert "matches Error \\d+"
```

Output includes `assert:`, `result:`, and `status: PASS/FAIL`. Exit code 0 on pass, 1 on fail.

---

## 8. Performance Metrics

### Key metrics

```bash
# LCP, FCP, CLS, TTFB with human-readable summary
wavexis perf https://example.com
```

### Advanced metrics

```bash
# CPU trace
wavexis perf https://example.com -m trace -d 5000 -o trace.json

# CPU profile
wavexis perf https://example.com -m profile -o profile.json

# JS code coverage
wavexis perf https://example.com -m coverage -o coverage.json

# CSS coverage
wavexis perf https://example.com -m css-coverage -o css-coverage.json

# Heap snapshot
wavexis perf https://example.com -m heap-snapshot -o heap.json
```

Metrics modes: `metrics` (default), `trace`, `profile`, `heap-snapshot`, `coverage`, `css-coverage`.

### Core Web Vitals scoring

```bash
# Basic measurement
wavexis cwv https://example.com

# With CI budgets (fails if thresholds exceeded)
wavexis cwv https://example.com --budget '{"lcp_ms":2500,"cls":0.1,"inp_ms":200}'

# Save report to file
wavexis cwv https://example.com -o cwv-report.json
```

Ratings: **good** / **needs-improvement** / **poor** based on official Google thresholds.

| Metric | Good | Poor |
|--------|------|------|
| LCP | < 2500ms | > 4000ms |
| CLS | < 0.1 | > 0.25 |
| INP | < 200ms | > 500ms |

---

## 9. Network Commands

### Headers and user agent

```bash
wavexis headers https://example.com
wavexis user-agent https://example.com --ua "Custom UA"
```

### Block and throttle

```bash
wavexis block https://example.com -p "*/ads/*"
wavexis throttle https://example.com --download 50000 --upload 25000 --latency 400
```

### HAR capture

```bash
wavexis har https://example.com -o out.har
```

### Intercept and mock

```bash
# Intercept requests matching pattern
wavexis intercept https://example.com -p "*/api/*" --block

# Mock response
wavexis mock https://example.com -p "*/api/*" -b '{"mock":true}' -s 200
```

### Request modification

```bash
# Modify request headers
wavexis modify https://example.com -p "*/api/*" --header "X-Custom: value"

# Modify response body
wavexis modify-response https://example.com -p "*/api/*" -b '{"modified":true}' -s 200

# Keep browser open for interception
wavexis modify https://example.com -p "*/api/*" --wait 10
```

### HAR replay

```bash
wavexis har-replay captured.har --url https://staging.example.com
```

### Network inspection

```bash
wavexis inspect https://example.com
```

---

## 10. Emulation

### Device emulation

```bash
wavexis emulation device https://example.com --device iphone-15 -o shot.png
```

### Viewport

```bash
wavexis emulation viewport https://example.com --width 375 --height 812 -o shot.png
```

### Geolocation

```bash
wavexis emulation geolocation https://example.com --lat 35.6762 --lon 139.6503 -o shot.png
```

### Timezone

```bash
wavexis emulation timezone https://example.com --timezone "Asia/Tokyo"
```

### Dark mode

```bash
wavexis emulation dark-mode https://example.com --enabled
```

### Other emulation

```bash
wavexis emulation media https://example.com --media print
wavexis emulation vision-deficiency https://example.com --type achromatopsia
wavexis emulation idle-override https://example.com --idle
wavexis emulation disable-js https://example.com
wavexis emulation visible-size https://example.com --width 800 --height 600
```

### List available devices

```bash
wavexis devices
```

---

## 11. Input Commands

```bash
# Click
wavexis click https://example.com --selector "#button"

# Type text
wavexis type https://example.com --selector "#input" --text "Hello"

# Fill field
wavexis fill https://example.com --selector "#input" --text "value"

# Select option
wavexis select https://example.com --selector "select" --value "option1"

# Hover
wavexis hover https://example.com --selector "#menu"

# Press key
wavexis key https://example.com --key "Enter"

# Drag
wavexis drag https://example.com --from "#source" --to "#target"

# Tap (touch)
wavexis tap https://example.com --selector "#button"
```

---

## 12. Cookies

```bash
# Get cookies
wavexis cookies https://example.com

# Set cookie
wavexis cookies https://example.com --set --name "session" --value "abc123"

# Delete cookie
wavexis cookies https://example.com --delete --name "session"

# Clear all cookies
wavexis cookies https://example.com --clear
```

---

## 13. Auth

Apply an auth context (cookies, headers, basic auth) from a JSON file:

```bash
# Apply auth context and print page title
wavexis auth context.json https://example.com/login

# Apply auth context and save a screenshot
wavexis auth context.json https://example.com/login --screenshot -o authed.png
```

Auth context JSON format:

```json
{
  "cookies": [
    {"name": "session", "value": "abc123", "domain": "example.com"}
  ],
  "headers": {"Authorization": "Bearer token"},
  "username": "user",
  "password": "pass"
}
```

---

## 14. Record and Replay

```bash
# Generate a YAML session from action types (non-interactive)
wavexis record https://example.com -o session.yml --actions "screenshot,eval"

# Record real interactions in a visible browser window
wavexis record https://example.com --interactive --duration 60 -o session.yml

# Replay a recorded session
wavexis replay session.yml
```

---

## 15. Serve Mode

HTTP API server with WebSocket streaming:

```bash
# Start serve mode
wavexis serve --host 0.0.0.0 --port 8080

# With rate limiting (60 requests/min)
wavexis serve --host 0.0.0.0 --port 8080 --rate-limit 60
```

### HTTP API

```bash
curl -X POST http://localhost:8080/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  -o screenshot.png
```

### WebSocket streaming

Connect to `ws://localhost:8080/ws` for real-time streaming of:

- Screenshots
- Console events
- Navigation events
- DOM mutations
- Performance metrics

---

## 16. Batch and Crawl

### Batch processing

```bash
# Process multiple URLs from file
wavexis batch urls.txt --action screenshot --output-dir ./screenshots/
```

### Crawling

```bash
# Crawl a website collecting titles and links
wavexis crawl https://example.com --depth 3 --output crawl-results.json
```

---

## 17. Advanced Commands

### Accessibility

```bash
# Accessibility tree
wavexis a11y https://example.com

# axe-core audit
wavexis axe https://example.com -o a11y-report.json
```

### Shadow DOM

```bash
# Click inside shadow root
wavexis shadow https://example.com click "#host" "#button"

# Fill inside shadow root
wavexis shadow https://example.com fill "#host" "#input" "value"

# Evaluate inside shadow root
wavexis shadow https://example.com eval "#host" "document.title"
```

### Natural language selectors

```bash
# Click using natural language
wavexis nl https://example.com click "the login button"

# Fill using natural language
wavexis nl https://example.com fill "the email field" "user@example.com"

# Find using natural language
wavexis nl https://example.com find "the submit button"
```

### WebExtensions

```bash
# Install an unpacked extension directory
wavexis extension-install /path/to/extension/

# Install a .crx file
wavexis extension-install /path/to/extension.crx

# List installed extensions
wavexis extension-list

# Uninstall by extension ID
wavexis extension-uninstall <extension-id>
```

### Browser preferences

```bash
# Get a preference
wavexis pref-get download.default_directory

# Set a preference
wavexis pref-set download.default_directory /tmp/downloads
```

### Security

```bash
# Get security state
wavexis security https://example.com

# Ignore certificate errors
wavexis security https://example.com --ignore-cert
```

### Visual diff

```bash
# Compare current page with baseline
wavexis visual-diff https://example.com --baseline baseline.png -o diff.png
```

### Lighthouse

```bash
wavexis lighthouse https://example.com -o lighthouse-report.json
```

### Tracing

```bash
# Start unified tracing
wavexis trace https://example.com start

# Stop tracing
wavexis trace https://example.com stop -o trace.json
```

---

## 18. Docker

### Pull and run

```bash
docker run -p 8080:8080 ghcr.io/mathiaspaulenko/wavexis:latest
```

### Build locally

```bash
docker build -t wavexis .
docker run -p 8080:8080 wavexis
```

### Docker Compose

```yaml
version: "3.8"
services:
  wavexis:
    image: ghcr.io/mathiaspaulenko/wavexis:latest
    ports:
      - "8080:8080"
    environment:
      - WAVEXIS_BACKEND=cdp
```

---

## 19. Command Categories Reference

| Category | Commands |
|----------|----------|
| Capture | `screenshot`, `pdf`, `screencast`, `scrape` |
| Navigate | `navigate`, `back`, `forward`, `reload`, `stop`, `tabs` |
| Console | `console`, `logs` |
| Cookies | `cookies` (get/set/delete/clear) |
| Network | `headers`, `user-agent`, `block`, `throttle`, `cache`, `intercept`, `mock`, `har` |
| Browser | `open`, `close`, `version` |
| Emulation | `emulation device`, `emulation viewport`, `emulation geolocation`, `emulation timezone`, `emulation dark-mode`, `emulation media`, `emulation vision-deficiency`, `emulation idle-override`, `emulation disable-js`, `emulation visible-size`, `devices` |
| Input | `click`, `type`, `fill`, `select`, `hover`, `key`, `drag`, `tap` |
| CSS | `css get-styles`, `css get-computed`, `css get-rules` |
| Debug | `debug break`, `debug step`, `debug pause`, `debug resume` |
| Performance | `perf metrics`, `perf trace`, `perf profile`, `perf coverage`, `perf heap-snapshot`, `perf css-coverage`, `cwv` |
| Storage | `storage get`, `storage set`, `storage clear`, `storage list`, `indexeddb` |
| Advanced | `sw`, `animation`, `record`, `replay`, `webauthn`, `cast`, `bluetooth`, `extension-install`, `extension-uninstall`, `extension-list`, `lighthouse`, `a11y`, `download`, `dialog`, `permissions`, `security` |
| Preferences | `pref-get`, `pref-set` |
| Auth | `auth` |
| Serve | `serve` |
| Interactive | `repl`, `init` |
| Network inspection | `inspect`, `modify`, `modify-response`, `har-replay` |
| Tracing | `trace` |
| Accessibility | `axe` |
| Events | `events` |
| Natural language | `nl` |
| Shadow DOM | `shadow` |
| Batch | `batch` |
| Crawl | `crawl` |
| Utility | `multi`, `raw`, `backends`, `install_check`, `completions`, `plugins` |

Run `wavexis --help` for the full list.

---

## 20. Best Practices

- **Start with the CLI** — Use `wavexis` commands for one-off tasks before writing Python scripts
- **Use multi-action YAML** — Chain actions in a single session to avoid browser launch overhead
- **Cache when repeating** — Use `--cache-ttl` for repeated multi-action workflows
- **Stealth for scraping** — Always use `--stealth` when scraping protected sites
- **CI assertions** — Use `--assert` with `eval` for reliable CI gates (exit 0/1)
- **Batch for multiple URLs** — Use `batch` instead of running commands in a loop
- **Serve mode for shared use** — Deploy `wavexis serve` in Docker for team-wide browser access
- **Choose backend early** — CDP for Chrome-only (no driver), BiDi for Firefox support
- **Use init wizard** — Run `wavexis init` to scaffold YAML configs from templates
- **REPL for exploration** — Use `wavexis repl` to interactively test selectors and actions

---

## 21. Common Pitfalls

| Pitfall | Cause | Solution |
|---------|-------|----------|
| Browser not found | No Chrome/Edge installed | Install Chrome or Edge; run `wavexis install_check` |
| BiDi backend fails | No ChromeDriver/geckodriver | Install the driver or use CDP backend (default) |
| Slow multi-action | Browser launches per action | Use `wavexis multi` with YAML config |
| Scraping blocked | Anti-bot detection | Use `--stealth` flag |
| CI flaky assertions | Timing issues | Add `wait` actions in YAML before assertions |
| Duplicate screenshots | No caching | Use `--cache-ttl` for repeated runs |
| Serve mode exposed | Bound to 0.0.0.0 without protection | Use rate limiting and reverse proxy |
| Large HAR files | Capturing everything | Filter with `-p` URL patterns |
| Extension not loading | Wrong path format | Use absolute path to unpacked extension dir |
| Device not found | Misspelled device name | Run `wavexis devices` to list available devices |

---

## 22. References

- `references/cli-command-reference.md` — Full command catalog with all flags and options
- `references/multi-action-yaml.md` — YAML config syntax, action types, and examples
- `references/serve-mode.md` — HTTP API endpoints, WebSocket events, and Docker deployment
- `assets/templates/screenshot.yml` — Screenshot multi-action template
- `assets/templates/multi-step.yml` — Multi-step login + screenshot template
- `assets/templates/scrape.yml` — Scraping multi-action template
- `assets/templates/ci-assertion.yml` — CI assertion template
- Related skills: `wave-ecosystem-guide`, `wavexis-mcp-agent-integration`, `wavexis-web-scraping`, `wavexis-performance-audit`

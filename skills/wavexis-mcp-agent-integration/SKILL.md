---
name: wavexis-mcp-agent-integration
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "MCP server integration for LLM browser automation: 220 tools, 13 capability tiers, session management, natural language interaction, multi-action workflows, and IDE configuration for Claude, Cursor, Windsurf, and VS Code."
tags: [wavexis-mcp, mcp-server, llm-integration, browser-automation, ai-agent]
trigger: When the user asks about wavexis-mcp, MCP server configuration for browser automation, LLM agent browser control, capability tiers, session management, or integrating wavexis with Claude, Cursor, Windsurf, or VS Code.
---

# WaveXis MCP Agent Integration

## Description

wavexis-mcp is an MCP (Model Context Protocol) server that exposes 220 tools for LLM-driven browser automation. It wraps wavexis (which wraps cdpwave + bidiwave) and provides 13 capability tiers so LLMs can control browsers with natural language, take screenshots, scrape content, fill forms, run performance audits, and execute multi-step workflows — all through structured tool calls.

## When to Invoke

- Configuring wavexis-mcp in an IDE or MCP client (Claude, Cursor, Windsurf, VS Code)
- Choosing capability tiers for a specific use case
- Managing browser sessions (open, close, list, switch)
- Using natural language interaction (`wavexis_act`) for form filling and clicks
- Creating multi-action YAML workflows via MCP
- Debugging MCP connection issues or tool errors
- Understanding the 220-tool catalog and tier system
- Setting up stateless vs session mode
- Configuring rate limiting, stealth mode, or SSRF protection

---

## 1. Installation

### Install

```bash
pip install wavexis-mcp[cdp]
```

### Run without installing

```bash
uvx wavexis-mcp --caps all
```

### Verify

```bash
wavexis-mcp --version
```

---

## 2. IDE Configuration

### Claude Desktop

Edit `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "wavexis": {
      "command": "uvx",
      "args": ["wavexis-mcp", "--caps", "all"]
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "wavexis": {
      "command": "uvx",
      "args": ["wavexis-mcp", "--caps", "core,network,storage"]
    }
  }
}
```

### Windsurf

Add to MCP settings:

```json
{
  "mcpServers": {
    "wavexis": {
      "command": "uvx",
      "args": ["wavexis-mcp", "--caps", "all"]
    }
  }
}
```

### VS Code (Copilot)

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "wavexis": {
      "command": "uvx",
      "args": ["wavexis-mcp", "--caps", "core,devtools,a11y"]
    }
  }
}
```

### HTTP transport (remote)

```bash
wavexis-mcp --transport http --host 0.0.0.0 --port 8765 --caps all
```

Then configure the client with the URL:

```json
{
  "mcpServers": {
    "wavexis": {
      "url": "http://localhost:8765"
    }
  }
}
```

---

## 3. Capability Tiers

13 tiers from `core` (always on, 72 tools) to `all` (220 tools). Select tiers with `--caps`:

```bash
# All 220 tools
wavexis-mcp --caps all

# Core only (72 tools — minimal, saves tokens)
wavexis-mcp --caps core

# Core + network + storage (110 tools — common scraping setup)
wavexis-mcp --caps core,network,storage

# Core + devtools + a11y (107 tools — debugging + accessibility)
wavexis-mcp --caps core,devtools,a11y

# Everything except experimental (189 tools)
wavexis-mcp --caps core,network,storage,emulation,a11y,interactions,devtools,vision,video,testing,workflows,data
```

### Tier Catalog

| Tier | Flag | Tools | Key Features |
|------|------|-------|--------------|
| Core | always on | 72 | Session, navigation, screenshot, PDF, scrape, eval, DOM, input, cookies, tabs, NL interaction, iframe, shadow DOM, events |
| Network | `network` | 20 | Headers, UA, block, throttle, cache, HAR, intercept, mock, modify req/resp, request body, replay HAR, request list |
| Storage | `storage` | 18 | localStorage, sessionStorage, cache storage, IndexedDB, state save/restore |
| Emulation | `emulation` | 9 | Device, viewport, geolocation, timezone, dark mode, locale, CPU, touch, sensors |
| A11y | `a11y` | 4 | Accessibility tree snapshot, node traversal, axe-core audit |
| Interactions | `interactions` | 5 | Dialogs, downloads, permissions |
| DevTools | `devtools` | 31 | Performance, CSS, debugging, overlay, console, security, window mgmt, combined trace, annotated screenshot |
| Vision | `vision` | 7 | Coordinate-based mouse (pixel-precise) |
| Video | `video` | 4 | Video recording, chapters, action overlay |
| Testing | `testing` | 6 | Assertions, locator generation |
| Workflows | `workflows` | 6 | Multi-action YAML, raw CDP/BiDi, browser context CRUD |
| Data | `data` | 7 | Codegen, Lighthouse audit, extract, websocket intercept, crawl, visual diff, core web vitals |
| Experimental | `experimental` | 31 | Service workers, animations, WebAuthn, WebAudio, media, cast, bluetooth, extensions, prefs |
| **Total** | `all` | **220** | |

### Tier Selection Guide

| Use Case | Recommended Tiers | Tools |
|----------|------------------|-------|
| Basic browser control | `core` | 72 |
| Web scraping | `core,network,storage` | 110 |
| Performance debugging | `core,devtools,data` | 110 |
| Accessibility audit | `core,a11y` | 76 |
| Visual regression | `core,vision,data` | 86 |
| Full automation | `all` | 220 |
| CI/CD pipeline | `core,testing,data` | 85 |
| Form filling via NL | `core` | 72 |
| Network analysis | `core,network` | 92 |
| Video recording | `core,video` | 76 |
| Extension testing | `core,experimental` | 103 |
| Token-efficient | `core` | 72 |

---

## 4. Session Management

wavexis-mcp supports two modes: **session** and **stateless**.

### Session mode (default)

Open a persistent browser session, execute multiple tool calls, then close:

```text
1. wavexis_session_open          → session_id
2. wavexis_navigate(url)          → uses session
3. wavexis_screenshot()           → uses session
4. wavexis_eval(expression)       → uses session
5. wavexis_session_close          → cleanup
```

Benefits:
- Browser stays open between tool calls
- State preserved (cookies, localStorage, page position)
- Multi-step workflows in a single browser instance
- Faster (no browser launch per call)

### Stateless mode

Each tool call opens and closes a browser:

```text
1. wavexis_screenshot(url)        → opens browser, captures, closes
2. wavexis_scrape(url)            → opens browser, scrapes, closes
```

Benefits:
- No session management overhead
- Each call is independent
- Simpler for one-off tasks

### Session tools

| Tool | Description |
|------|-------------|
| `wavexis_session_open` | Open a new browser session, returns `session_id` |
| `wavexis_session_close` | Close a session and release resources |
| `wavexis_session_list` | List all active sessions |
| `wavexis_session_info` | Get details of a specific session |
| `wavexis_tabs_new` | Open a new tab in a session |
| `wavexis_tabs_close` | Close a tab in a session |
| `wavexis_tabs_list` | List tabs in a session |
| `wavexis_tabs_switch` | Switch to a tab in a session |

### Best practices

- **Always close sessions** — Unclosed sessions leak resources
- **One session per workflow** — Don't interleave sessions
- **Use stateless for one-offs** — No cleanup needed
- **List sessions to debug** — `wavexis_session_list` shows active sessions

---

## 5. Core Tools (72 — always available)

### Navigation

| Tool | Description |
|------|-------------|
| `wavexis_navigate` | Navigate to a URL |
| `wavexis_navigate_back` | Go back in history |
| `wavexis_navigate_forward` | Go forward in history |
| `wavexis_navigate_reload` | Reload the page |
| `wavexis_navigate_stop` | Stop loading |

### Capture

| Tool | Description |
|------|-------------|
| `wavexis_screenshot` | Take a screenshot (viewport, full-page, element) |
| `wavexis_pdf` | Generate a PDF |
| `wavexis_scrape` | Scrape page content (text, HTML, markdown) |
| `wavexis_dom` | Get DOM tree or specific element |

### Evaluate

| Tool | Description |
|------|-------------|
| `wavexis_eval` | Evaluate JavaScript expression |
| `wavexis_call_function` | Call a JS function with arguments |

### Input

| Tool | Description |
|------|-------------|
| `wavexis_click` | Click an element by selector |
| `wavexis_type` | Type text into an element |
| `wavexis_fill` | Fill a field (instant) |
| `wavexis_press_key` | Press a keyboard key |
| `wavexis_hover` | Hover over an element |
| `wavexis_select_option` | Select a dropdown option |
| `wavexis_scroll` | Scroll the page |
| `wavexis_scroll_to` | Scroll to an element |

### Cookies

| Tool | Description |
|------|-------------|
| `wavexis_cookies_get` | Get cookies |
| `wavexis_cookies_set` | Set a cookie |
| `wavexis_cookies_delete` | Delete a cookie |
| `wavexis_cookies_clear` | Clear all cookies |

### Natural Language

| Tool | Description |
|------|-------------|
| `wavexis_act` | Natural language browser interaction |
| `wavexis_find` | Find element by natural language description |

### Advanced DOM

| Tool | Description |
|------|-------------|
| `wavexis_shadow_click` | Click inside shadow DOM |
| `wavexis_shadow_fill` | Fill inside shadow DOM |
| `wavexis_shadow_eval` | Evaluate JS inside shadow DOM |
| `wavexis_iframe_eval` | Evaluate JS inside iframe |
| `wavexis_iframe_click` | Click inside iframe |

### Events

| Tool | Description |
|------|-------------|
| `wavexis_events_listen` | Listen for browser events |
| `wavexis_events_wait` | Wait for a specific event |

### Console

| Tool | Description |
|------|-------------|
| `wavexis_console_get` | Get console logs |
| `wavexis_console_clear` | Clear console |

### Browser info

| Tool | Description |
|------|-------------|
| `wavexis_url` | Get current URL |
| `wavexis_title` | Get page title |
| `wavexis_user_agent` | Get or set user agent |
| `wavexis_headers` | Get response headers |

---

## 6. Natural Language Interaction

`wavexis_act` lets LLMs control browsers using natural language instead of CSS selectors:

```text
User: "Click the login button"
→ wavexis_act(action="click", description="the login button")

User: "Fill the email field with admin@example.com"
→ wavexis_act(action="fill", description="the email field", text="admin@example.com")

User: "Find the submit button"
→ wavexis_find(description="the submit button")
```

### Supported actions

| Action | Description | Parameters |
|--------|-------------|------------|
| `click` | Click an element | `description` |
| `fill` | Fill a field | `description`, `text` |
| `type` | Type into a field | `description`, `text` |
| `hover` | Hover over an element | `description` |
| `scroll` | Scroll the page | `description` (direction) |
| `screenshot` | Take a screenshot | `description` (area) |

### How it works

1. LLM calls `wavexis_act` with a natural language description
2. wavexis-mcp analyzes the page DOM
3. Matches the description to the most likely element
4. Executes the action
5. Returns the result and element info

This eliminates the need for LLMs to know CSS selectors, making browser automation accessible through plain language.

---

## 7. Multi-Action Workflows

Chain multiple actions in a single tool call using YAML:

```text
wavexis_multi(config="""
actions:
  - navigate: https://example.com/login
  - fill:
      selector: "#username"
      text: admin@example.com
  - fill:
      selector: "#password"
      text: changeme
  - click:
      selector: "#submit"
  - wait_for:
      selector: ".dashboard"
      timeout: 10000
  - screenshot:
      full_page: true
""")
```

### Workflow tools

| Tool | Description |
|------|-------------|
| `wavexis_multi` | Execute a multi-action YAML config |
| `wavexis_raw_cdp` | Execute a raw CDP method |
| `wavexis_raw_bidi` | Execute a raw BiDi method |
| `wavexis_browser_context_create` | Create a new browser context |
| `wavexis_browser_context_list` | List browser contexts |
| `wavexis_browser_context_close` | Close a browser context |

---

## 8. Network Tools (tier: `network`)

| Tool | Description |
|------|-------------|
| `wavexis_headers_set` | Set request headers |
| `wavexis_headers_get` | Get response headers |
| `wavexis_user_agent_set` | Set custom user agent |
| `wavexis_block` | Block requests by pattern |
| `wavexis_throttle` | Throttle network speed |
| `wavexis_cache_clear` | Clear browser cache |
| `wavexis_har` | Capture HAR file |
| `wavexis_intercept` | Intercept requests |
| `wavexis_mock` | Mock a response |
| `wavexis_modify_request` | Modify request headers/body |
| `wavexis_modify_response` | Modify response body |
| `wavexis_request_body` | Get response body for a request |
| `wavexis_har_replay` | Replay a HAR file |
| `wavexis_request_list` | List captured requests |
| `wavexis_websocket_intercept` | Intercept WebSocket messages |
| `wavexis_websocket_send` | Send a WebSocket message |
| `wavexis_network_conditions` | Set network conditions |
| `wavexis_extra_headers` | Set extra headers for all requests |
| `wavexis_auth_challenge` | Handle HTTP auth challenges |
| `wavexis_request_log` | Get request log |

---

## 9. DevTools Tools (tier: `devtools`)

| Tool | Description |
|------|-------------|
| `wavexis_perf_metrics` | Get performance metrics |
| `wavexis_perf_trace` | Start/stop CPU trace |
| `wavexis_perf_profile` | Start/stop CPU profile |
| `wavexis_perf_coverage` | Get JS code coverage |
| `wavexis_perf_css_coverage` | Get CSS coverage |
| `wavexis_perf_heap_snapshot` | Take heap snapshot |
| `wavexis_css_get_styles` | Get inline styles of element |
| `wavexis_css_get_computed` | Get computed styles |
| `wavexis_css_get_rules` | Get CSS rules matching selector |
| `wavexis_debug_break` | Set a breakpoint |
| `wavexis_debug_step` | Step over/into/out |
| `wavexis_debug_pause` | Pause execution |
| `wavexis_debug_resume` | Resume execution |
| `wavexis_debug_scopes` | Get current scopes |
| `wavexis_debug_callstack` | Get call stack |
| `wavexis_overlay_highlight` | Highlight an element |
| `wavexis_overlay_inspect` | Inspect mode |
| `wavexis_overlay_screenshot` | Annotated screenshot with bounding boxes |
| `wavexis_console_enable` | Enable console capture |
| `wavexis_console_disable` | Disable console capture |
| `wavexis_security_state` | Get security state |
| `wavexis_security_cert` | Get certificate details |
| `wavexis_window_bounds` | Get/set window bounds |
| `wavexis_window_maximize` | Maximize window |
| `wavexis_window_minimize` | Minimize window |
| `wavexis_trace_start` | Start unified tracing |
| `wavexis_trace_stop` | Stop tracing and save |
| `wavexis_trace_combined` | Combined trace with screenshots |
| `wavexis_annotate_screenshot` | Screenshot with annotations |
| `wavexis_set_overlay` | Set overlay grid |
| `wavexis_clear_overlay` | Clear overlays |

---

## 10. Data Tools (tier: `data`)

| Tool | Description |
|------|-------------|
| `wavexis_codegen` | Generate code from browser actions |
| `wavexis_lighthouse` | Run Lighthouse audit |
| `wavexis_extract` | Extract structured data from page |
| `wavexis_websocket_intercept_data` | Intercept and capture WebSocket data |
| `wavexis_crawl` | Crawl a website |
| `wavexis_visual_diff` | Compare page with baseline |
| `wavexis_cwv` | Core Web Vitals scoring with budgets |

---

## 11. Testing Tools (tier: `testing`)

| Tool | Description |
|------|-------------|
| `wavexis_assert` | Assert a condition (pass/fail) |
| `wavexis_assert_visible` | Assert element is visible |
| `wavexis_assert_text` | Assert element text content |
| `wavexis_assert_url` | Assert current URL |
| `wavexis_assert_title` | Assert page title |
| `wavexis_locator` | Generate a robust locator for an element |

---

## 12. Configuration Options

### CLI flags

| Flag | Description | Default |
|------|-------------|---------|
| `--caps` | Capability tiers (comma-separated) | `core` |
| `--transport` | Transport: `stdio` or `http` | `stdio` |
| `--host` | HTTP bind address | `127.0.0.1` |
| `--port` | HTTP port | `8765` |
| `--backend` | Backend: `cdp` or `bidi` | `cdp` |
| `--headless` | Run browser headless | `true` |
| `--stealth` | Enable stealth mode | `false` |
| `--rate-limit` | Requests per minute | `0` (disabled) |
| `--allow-remote` | Allow remote connections (HTTP) | `false` |
| `--browser-path` | Custom browser executable | Auto-detected |
| `--timeout` | Default timeout (ms) | `30000` |
| `--max-sessions` | Maximum concurrent sessions | `10` |
| `--log-level` | Log level: `debug`, `info`, `warn`, `error` | `info` |

### Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WAVEXIS_MCP_CAPS` | Capability tiers | `core` |
| `WAVEXIS_MCP_TRANSPORT` | Transport type | `stdio` |
| `WAVEXIS_MCP_HOST` | HTTP bind address | `127.0.0.1` |
| `WAVEXIS_MCP_PORT` | HTTP port | `8765` |
| `WAVEXIS_MCP_BACKEND` | Backend type | `cdp` |
| `WAVEXIS_MCP_HEADLESS` | Headless mode | `true` |
| `WAVEXIS_MCP_STEALTH` | Stealth mode | `false` |
| `WAVEXIS_MCP_RATE_LIMIT` | Rate limit | `0` |
| `WAVEXIS_MCP_MAX_SESSIONS` | Max sessions | `10` |

---

## 13. Error Handling

wavexis-mcp returns structured errors with actionable suggestions:

```json
{
  "error": {
    "code": "SESSION_NOT_FOUND",
    "message": "Session abc123 not found",
    "suggestion": "Call wavexis_session_open to create a new session, or check wavexis_session_list for active sessions"
  }
}
```

### Common error codes

| Code | Cause | Fix |
|------|-------|-----|
| `SESSION_NOT_FOUND` | Invalid or expired session ID | Open a new session or list active ones |
| `BROWSER_NOT_FOUND` | No Chrome/Edge installed | Install Chrome or set `--browser-path` |
| `NAVIGATION_TIMEOUT` | Page took too long to load | Increase `--timeout` or check network |
| `ELEMENT_NOT_FOUND` | Selector didn't match | Use `wavexis_find` with NL description |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Increase `--rate-limit` or reduce calls |
| `CAPABILITY_NOT_ENABLED` | Tool tier not loaded | Add tier to `--caps` flag |
| `SSRF_BLOCKED` | URL blocked by SSRF protection | Use public URLs only |
| `BACKEND_ERROR` | CDP/BiDi backend error | Check browser process and driver |

---

## 14. Security

### SSRF protection

wavexis-mcp blocks requests to private IP ranges by default:
- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`
- `127.0.0.0/8`
- `169.254.0.0/16`
- `::1/128`

### Rate limiting

```bash
wavexis-mcp --rate-limit 60
```

60 requests per minute per client. Excess requests return `RATE_LIMIT_EXCEEDED`.

### Stealth mode

```bash
wavexis-mcp --stealth
```

Hides `navigator.webdriver`, fakes browser fingerprints. Useful for scraping protected sites.

### Remote access

```bash
wavexis-mcp --transport http --host 0.0.0.0 --port 8765 --allow-remote
```

**Warning:** Only use `--allow-remote` behind a reverse proxy with authentication.

---

## 15. Docker

### Pull and run

```bash
docker run -p 8765:8765 ghcr.io/mathiaspaulenko/wavexis-mcp:latest \
  --transport http --caps all
```

### Docker Compose

```yaml
version: "3.8"
services:
  wavexis-mcp:
    image: ghcr.io/mathiaspaulenko/wavexis-mcp:latest
    ports:
      - "8765:8765"
    command: --transport http --caps all --host 0.0.0.0
    environment:
      - WAVEXIS_MCP_RATE_LIMIT=60
    restart: unless-stopped
```

---

## 16. MCP Resources and Prompts

wavexis-mcp also exposes MCP resources and prompts beyond tools:

### Resources

| Resource | Description |
|----------|-------------|
| `wavexis://browser/info` | Browser version and capabilities |
| `wavexis://session/{id}/screenshot` | Latest screenshot for a session |
| `wavexis://session/{id}/console` | Console logs for a session |
| `wavexis://session/{id}/network` | Network log for a session |

### Prompts

| Prompt | Description |
|--------|-------------|
| `wavexis_scrape_page` | Prompt template for scraping a page |
| `wavexis_fill_form` | Prompt template for filling a form |
| `wavexis_audit_performance` | Prompt template for performance audit |
| `wavexis_test_page` | Prompt template for testing a page |

---

## 17. Best Practices

- **Start with `core` tier** — 72 tools covers most use cases. Add tiers as needed to save tokens
- **Always close sessions** — Call `wavexis_session_close` when done to avoid resource leaks
- **Use `wavexis_act` for forms** — Natural language is more robust than selectors for form filling
- **Use multi-action YAML** — Chain actions in a single call to reduce round trips
- **Enable stealth for scraping** — `--stealth` hides automation indicators
- **Set rate limits** — Prevent runaway LLM agents from making too many calls
- **Use HTTP transport for teams** — Deploy in Docker with `--transport http` for shared access
- **Check `wavexis_session_list`** — Debug stuck sessions by listing active ones
- **Use `wavexis_find` before `wavexis_click`** — NL element finding is more reliable than guessing selectors
- **Leverage assertions for testing** — `wavexis_assert_*` tools provide pass/fail results for CI

---

## 18. Common Pitfalls

| Pitfall | Cause | Solution |
|---------|-------|----------|
| Too many tools loaded | `--caps all` when only core needed | Use specific tiers: `--caps core,network` |
| Session leak | Forgot to close session | Always call `wavexis_session_close` |
| Element not found | Brittle CSS selector | Use `wavexis_act` or `wavexis_find` with NL |
| Rate limit hit | LLM making too many calls | Increase `--rate-limit` or optimize workflow |
| SSRF blocked | Trying to access localhost | Use public URLs or disable SSRF (not recommended) |
| Browser not found | No Chrome installed | Install Chrome or set `--browser-path` |
| Token waste | All 220 tools in context | Use minimal `--caps` for the task |
| Stale session | Session expired | Check `wavexis_session_list`, open new session |
| Capability not enabled | Tool from unloaded tier | Add the tier to `--caps` |
| HTTP transport exposed | `--allow-remote` without proxy | Use reverse proxy with auth |

---

## 19. References

- `references/tool-catalog.md` — Complete 220-tool catalog with parameters and return types
- `references/tier-selection.md` — Detailed tier selection guide with use-case scenarios
- `references/ide-setup-guide.md` — Step-by-step IDE configuration for Claude, Cursor, Windsurf, VS Code
- `assets/mcp-configs/claude-desktop.json` — Claude Desktop config template
- `assets/mcp-configs/cursor.json` — Cursor config template
- `assets/mcp-configs/windsurf.json` — Windsurf config template
- `assets/mcp-configs/vscode.json` — VS Code config template
- `assets/mcp-configs/http-remote.json` — HTTP transport remote config template
- Related skills: `wave-ecosystem-guide`, `wavexis-cli-automation`, `wavexis-web-scraping`, `wavexis-performance-audit`

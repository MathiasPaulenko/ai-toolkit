---
name: wave-ecosystem-guide
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Guide to the Wave browser automation ecosystem: cdpwave (CDP client), bidiwave (WebDriver BiDi client), wavexis (CLI), and wavexis-mcp (MCP server). Helps choose the right tool for each use case."
tags: [wave-ecosystem, browser-automation, cdp, webdriver-bidi, mcp]
trigger: When the user asks about the Wave ecosystem, needs to choose between cdpwave, bidiwave, wavexis, or wavexis-mcp, or wants to understand the architecture and tool selection for browser automation in Python.
---

# Wave Ecosystem Guide

## Description

The Wave ecosystem is a collection of browser automation tools built in 100% Python. No Node.js, no Chromium download, no Selenium, no Playwright. This skill helps you choose the right Wave tool for each use case and understand how the pieces fit together.

## When to Invoke

- Choosing between cdpwave, bidiwave, wavexis, or wavexis-mcp for a browser automation task
- Understanding the Wave ecosystem architecture and how the repos relate
- Migrating from Playwright, Selenium, pyppeteer, or Puppeteer to the Wave ecosystem
- Deciding between CDP (Chromium-specific) and BiDi (W3C cross-browser) backends
- Setting up browser automation in a Python project for the first time
- Answering "which Wave tool should I use for X?"

---

## 1. Architecture

```text
wavexis-mcp (MCP server, 220 tools, 13 tiers)
└─ wraps → wavexis (CLI, 130+ commands, 480+ sub-commands)
               ├─ cdpwave (CDP backend, 60 domains, 689 methods)
               └─ bidiwave (BiDi backend, W3C cross-browser)
```

Each layer builds on the one below:

| Layer | Repo | Role | PyPI |
|-------|------|------|------|
| **Low-level CDP** | `cdpwave` | Direct WebSocket to Chrome/Edge DevTools Protocol | `pip install cdpwave` |
| **Low-level BiDi** | `bidiwave` | W3C WebDriver BiDi protocol for Chrome, Firefox, Edge | `pip install bidiwave` |
| **High-level CLI** | `wavexis` | Unified CLI wrapping cdpwave + bidiwave | `pip install wavexis[cdp]` |
| **MCP server** | `wavexis-mcp` | 220 MCP tools for LLM browser automation | `pip install wavexis-mcp[cdp]` |

---

## 2. Tool Selection

### Decision Tree

```text
What do you need?
│
├── LLM / AI agent needs to control a browser
│   └──► wavexis-mcp
│        (MCP server, 220 tools, works with Claude, Cursor, Windsurf, VS Code)
│
├── Quick one-off task from the command line
│   ├── Screenshot / PDF / scrape a single page
│   ├── CI assertion (title contains X, exit code 0/1)
│   ├── Batch process multiple URLs
│   └──► wavexis CLI
│        (130+ commands, REPL, multi-action YAML, stealth, serve mode)
│
├── Programmatic browser control in Python
│   ├── Chrome / Edge only
│   │   └──► cdpwave
│   │        (60 CDP domains, 689 typed methods, no driver needed)
│   │
│   ├── Cross-browser (Chrome + Firefox + Edge)
│   │   └──► bidiwave
│   │        (W3C WebDriver BiDi, 12 modules, Pydantic v2 models)
│   │
│   └── Both backends with a unified API
│       └──► wavexis as a library
│            (AbstractBackend interface, switch with --backend bidi)
│
└── Not sure?
    └──► Start with wavexis CLI for quick tasks
         Move to cdpwave/bidiwave when you need programmatic control
         Move to wavexis-mcp when you need LLM integration
```

### Quick Reference

| Use Case | Recommended Tool | Why |
|----------|-----------------|-----|
| LLM agent controls browser | `wavexis-mcp` | 220 MCP tools, capability tiers, NL interaction |
| Screenshot from CLI | `wavexis screenshot` | One command, no code |
| CI performance gate | `wavexis cwv --budget` | Core Web Vitals with budgets, exit codes |
| Web scraping with stealth | `wavexis --stealth scrape` | Anti-bot hiding, crawl, batch |
| Chrome-specific CDP access | `cdpwave` | Full 60-domain CDP coverage, escape hatch |
| Cross-browser testing | `bidiwave` | W3C standard, Chrome + Firefox + Edge |
| Multi-tab async automation | `cdpwave` | Multi-tab sessions, event handling, typed methods |
| Network interception (cross-browser) | `bidiwave` | W3C network interception, mock responses |
| Debugging with breakpoints | `cdpwave` | Debugger, HeapProfiler, Profiler domains |
| Visual regression in CI | `wavexis visual-diff` | Baseline comparison, PR integration |
| Form filling via natural language | `wavexis-mcp` (`wavexis_act`) | NL element matching, no selectors needed |
| HAR capture and replay | `wavexis har` / `wavexis har-replay` | Network recording and replay |
| Session recording and replay | `wavexis record` / `wavexis replay` | Interactive recording to YAML |
| Docker browser service | `wavexis serve` | HTTP API + WebSocket streaming in container |

---

## 3. Backend Comparison: CDP vs BiDi

| Feature | cdpwave (CDP) | bidiwave (BiDi) |
|---------|---------------|-----------------|
| **Protocol** | Chrome DevTools Protocol | W3C WebDriver BiDi |
| **Standard** | Chromium-specific (proprietary) | W3C standard |
| **Browsers** | Chrome, Edge, Brave, Chromium | Chrome, Firefox, Edge |
| **Driver needed** | No (direct WebSocket) | Yes (ChromeDriver / geckodriver) |
| **Coverage** | 60 domains, 689 methods | 12 modules, W3C spec |
| **Type system** | Typed dicts, `mypy --strict` | Pydantic v2 models, `mypy` clean |
| **Event handling** | `session.on()`, `wait_for_event()` | 27 event types, async handlers |
| **Escape hatch** | `session.send("Any.CDPMethod", params)` | CDP bridge (`client.cdp`) |
| **Network interception** | Fetch domain | Native BiDi network module |
| **Cross-browser** | No | Yes |
| **Reconnection** | WebSocket keepalive | Exponential backoff |
| **Best for** | Chrome-only, low-level CDP access | Cross-browser, W3C compliance |

### When to use which

- **cdpwave** — You only target Chrome/Edge and need maximum CDP coverage (debugging, profiling, heap snapshots, DOM debugger, WebAuthn, Bluetooth, Cast)
- **bidiwave** — You need cross-browser support (Firefox), W3C standard compliance, or network interception with a clean API
- **Both** — Use `wavexis` which abstracts both behind a unified `AbstractBackend` interface. Switch with `--backend bidi`

---

## 4. Installation

### cdpwave (CDP backend)

```bash
pip install cdpwave
```

Requirements: Python 3.11+, a Chromium-based browser already installed.

### bidiwave (BiDi backend)

```bash
pip install bidiwave
```

Requirements: Python 3.11+, a BiDi-capable browser endpoint (ChromeDriver, Firefox with `--remote-debugging-port`, or EdgeDriver).

### wavexis (CLI)

```bash
# CDP backend (default, recommended)
pip install wavexis[cdp]

# BiDi backend
pip install wavexis[bidi]

# Serve mode + image extras
pip install wavexis[cdp,serve,image]
```

### wavexis-mcp (MCP server)

```bash
pip install wavexis-mcp[cdp]

# Or run without installing
uvx wavexis-mcp --caps all
```

---

## 5. Quick Start Examples

### cdpwave — Screenshot and evaluate

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        result = await session.runtime.evaluate("document.title", return_by_value=True)
        print(result["result"]["value"])  # "Example Domain"
        await session.close()

asyncio.run(main())
```

### bidiwave — Cross-browser evaluate

```python
import asyncio
from bidiwave import BiDiClient, StringValue

async def main():
    async with await BiDiClient.connect("ws://localhost:9515/session") as client:
        async with await client.browsing.open("https://example.com") as page:
            result = await page.evaluate("document.title")
            match result:
                case StringValue(value=title):
                    print(f"Title: {title}")

asyncio.run(main())
```

### wavexis CLI — Screenshot and scrape

```bash
# Screenshot
wavexis screenshot https://example.com -o out.png

# Full-page screenshot
wavexis screenshot https://example.com -o full.png --full-page

# Scrape content
wavexis scrape https://example.com --selector "article"

# Evaluate JavaScript
wavexis eval https://example.com -e "document.title"
```

### wavexis-mcp — MCP config

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

Then ask your LLM: *"Take a full-page screenshot of https://example.com"*

---

## 6. Migration Paths

### From Playwright

| Playwright | Wave equivalent |
|------------|----------------|
| `playwright.chromium.launch()` | `CDPClient.launch()` (cdpwave) |
| `playwright.firefox.launch()` | `BiDiClient.connect()` (bidiwave) |
| `page.goto()` | `session.page.navigate()` / `page.navigate()` |
| `page.screenshot()` | `session.page.capture_screenshot()` / `page.screenshot()` |
| `page.evaluate()` | `session.runtime.evaluate()` / `page.evaluate()` |
| `page.click()` | `client.input.click()` (bidiwave) / JS via eval |
| Playwright MCP | `wavexis-mcp` (220 tools vs ~21) |

Key differences:
- No browser download (uses your existing Chrome/Edge)
- No Node.js required (100% Python)
- CDP + BiDi dual backend (Playwright is CDP-only for Chromium)
- 220 MCP tools vs ~21 in Playwright MCP

### From Selenium

| Selenium | Wave equivalent |
|----------|----------------|
| `webdriver.Chrome()` | `CDPClient.launch()` (cdpwave) |
| `webdriver.Firefox()` | `BiDiClient.connect()` (bidiwave) |
| `driver.get()` | `session.page.navigate()` / `page.navigate()` |
| `driver.find_element()` | DOM queries via `session.dom` / JS eval |
| `driver.execute_script()` | `session.runtime.evaluate()` / `page.evaluate()` |
| Selenium Grid | `wavexis serve` (HTTP API + WebSocket) |

Key differences:
- No ChromeDriver needed for CDP (direct WebSocket)
- No Selenium Server / Grid needed (wavexis serve mode)
- Async-first (Selenium is sync)
- Full CDP domain access (Selenium hides most CDP)

### From pyppeteer / pychrome

| pyppeteer / pychrome | Wave equivalent |
|----------------------|----------------|
| `pyppeteer.launch()` | `CDPClient.launch()` (cdpwave) |
| `pyppeteer.connect()` | `CDPClient.connect()` (cdpwave) |
| `page.evaluate()` | `session.runtime.evaluate()` (cdpwave) |
| Untyped responses | Typed dicts, `mypy --strict` |
| Partial CDP coverage | Full 60-domain, 689-method coverage |

See `references/migration-pyppeteer.md` for detailed migration guide.

---

## 7. Feature Parity Matrix

| Feature | cdpwave | bidiwave | wavexis CLI | wavexis-mcp |
|---------|:-------:|:--------:|:-----------:|:-----------:|
| Screenshot | Yes | Yes | Yes | Yes |
| PDF generation | Yes | Yes | Yes | Yes |
| JavaScript eval | Yes | Yes | Yes | Yes |
| Cookie management | Yes | Yes | Yes | Yes |
| Network interception | Yes | Yes | Yes | Yes |
| Device emulation | Yes | Yes | Yes | Yes |
| Multi-tab sessions | Yes | Yes | Yes | Yes |
| Event handling | Yes | Yes | Yes | Yes |
| Stealth mode | — | — | Yes | Yes |
| REPL | — | — | Yes | — |
| Multi-action YAML | — | — | Yes | Yes |
| Session recording | — | — | Yes | — |
| CI assertions | — | — | Yes | — |
| Serve mode (HTTP API) | — | — | Yes | — |
| LLM tool calls | — | — | — | Yes |
| Natural language interaction | — | — | — | Yes |
| Capability tiers | — | — | — | Yes |
| MCP resources & prompts | — | — | — | Yes |
| Debugging (breakpoints) | Yes | — | Yes | Yes |
| Heap profiler | Yes | — | Yes | Yes |
| CPU profiler | Yes | — | Yes | Yes |
| Code coverage | Yes | — | Yes | Yes |
| WebAuthn | Yes | — | Yes | Yes |
| Bluetooth | Yes | — | Yes | Yes |
| Cast | Yes | — | Yes | Yes |
| Web extensions | — | Yes | Yes | Yes |
| Preload scripts | — | Yes | Yes | Yes |
| Cross-browser (Firefox) | — | Yes | Yes | Yes |
| Lighthouse audits | — | — | Yes | Yes |
| Core Web Vitals scoring | — | — | Yes | Yes |
| Visual diff | — | — | Yes | Yes |
| HAR capture | Yes | — | Yes | Yes |
| HAR replay | — | — | Yes | — |
| Accessibility audit | Yes | — | Yes | Yes |
| Shadow DOM | — | — | Yes | Yes |
| Crawl | — | — | Yes | Yes |
| Batch processing | — | — | Yes | — |
| Docker | — | — | Yes | Yes |

---

## 8. Ecosystem Links

| Resource | URL |
|----------|-----|
| cdpwave repo | https://github.com/MathiasPaulenko/cdpwave |
| cdpwave docs | https://mathiaspaulenko.github.io/cdpwave/ |
| cdpwave PyPI | https://pypi.org/project/cdpwave/ |
| bidiwave repo | https://github.com/MathiasPaulenko/bidiwave |
| bidiwave docs | https://mathiaspaulenko.github.io/bidiwave/ |
| bidiwave PyPI | https://pypi.org/project/bidiwave/ |
| wavexis repo | https://github.com/MathiasPaulenko/wavexis |
| wavexis docs | https://mathiaspaulenko.github.io/wavexis/ |
| wavexis PyPI | https://pypi.org/project/wavexis/ |
| wavexis-mcp repo | https://github.com/MathiasPaulenko/wavexis-mcp |
| wavexis-mcp docs | https://mathiaspaulenko.github.io/wavexis-mcp/ |
| wavexis-mcp PyPI | https://pypi.org/project/wavexis-mcp/ |

---

## 9. Best Practices

- **Start simple** — Use `wavexis` CLI for one-off tasks before writing Python scripts
- **Choose backend early** — CDP for Chrome-only, BiDi for cross-browser. Switch in wavexis with `--backend bidi`
- **Use stealth for scraping** — `--stealth` hides `navigator.webdriver` and fakes browser fingerprints
- **Leverage capability tiers** — In wavexis-mcp, start with `--caps core` (72 tools) and add tiers as needed to save tokens
- **Use multi-action YAML** — Chain actions in a single browser session to avoid launch overhead
- **Close sessions** — Always close sessions in wavexis-mcp to avoid resource leaks
- **Use the escape hatch** — `session.send("Any.CDPMethod", params)` in cdpwave for any uncovered CDP method
- **Preload scripts for monitoring** — Inject JS before page load with bidiwave's `client.preload.add_preload_script()`
- **CI assertions** — Use `--assert` with `eval` for CI gates that pass/fail based on page state
- **Action caching** — Use `--cache-ttl` to avoid re-analyzing pages in repeated multi-action workflows

---

## 10. Common Pitfalls

| Pitfall | Cause | Solution |
|---------|-------|----------|
| Using cdpwave for Firefox | CDP is Chromium-only | Use bidiwave for Firefox |
| Installing Chromium separately | Not needed | Wave uses your existing browser |
| Using wavexis-mcp without tiers | All 220 tools loaded | Use `--caps core` to start, add tiers as needed |
| Not closing MCP sessions | Resource leak | Always call `wavexis_session_close` |
| Using sync code with cdpwave | cdpwave is async-only | Use `asyncio.run()` and `async/await` |
| Missing ChromeDriver for BiDi | BiDi needs a driver | Run `chromedriver --port=9515` or use Firefox (native BiDi) |
| Exposing wavexis-mcp remotely | Security risk | Use `--allow-remote` only behind a reverse proxy |
| Large MCP tier in CI | Token waste | Use minimal `--caps` for the task at hand |

---

## 11. References

- `references/ecosystem-comparison.md` — Full feature comparison table with all 220 MCP tools
- `references/decision-tree.md` — Detailed flowchart for tool and backend selection
- `references/migration-pyppeteer.md` — Step-by-step migration from pyppeteer/pychrome to cdpwave
- `assets/ecosystem-cheatsheet.md` — Quick reference card for printing
- Related skills: `wavexis-cli-automation`, `wavexis-mcp-agent-integration`, `cdpwave-testing`, `bidiwave-cross-browser`

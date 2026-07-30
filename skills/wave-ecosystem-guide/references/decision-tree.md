# Decision Tree — Which Wave Tool Should I Use?

> Detailed flowchart for choosing the right Wave tool and backend for each scenario.

## Primary Decision

```text
START
  │
  ├── Q: Does an LLM/AI agent need to control the browser?
  │   ├── YES → wavexis-mcp
  │   │         ├── Need all 220 tools? → --caps all
  │   │         ├── Need just basics? → --caps core (72 tools)
  │   │         ├── Need network interception? → --caps core,network
  │   │         ├── Need accessibility audit? → --caps core,a11y
  │   │         ├── Need performance/debugging? → --caps core,devtools
  │   │         └── Need video recording? → --caps core,video
  │   │
  │   └── NO → continue
  │
  ├── Q: Is this a one-off task from the command line?
  │   ├── YES → wavexis CLI
  │   │         ├── Screenshot? → wavexis screenshot <url> -o out.png
  │   │         ├── Full-page screenshot? → wavexis screenshot <url> -o out.png --full-page
  │   │         ├── PDF? → wavexis pdf <url> -o out.pdf
  │   │         ├── Scrape content? → wavexis scrape <url> --selector "article"
  │   │         ├── Evaluate JS? → wavexis eval <url> -e "document.title"
  │   │         ├── CI assertion? → wavexis eval <url> -e "..." --assert "== Expected"
  │   │         ├── Batch URLs? → wavexis batch urls.txt --action screenshot
  │   │         ├── Crawl site? → wavexis crawl <url>
  │   │         ├── Stealth scraping? → wavexis --stealth scrape <url> --selector "article"
  │   │         ├── Performance audit? → wavexis cwv <url> --budget '{"lcp_ms":2500}'
  │   │         ├── Interactive REPL? → wavexis repl
  │   │         ├── Multi-action YAML? → wavexis multi config.yml
  │   │         ├── Record session? → wavexis record <url> --interactive -o session.yml
  │   │         └── HTTP API server? → wavexis serve --port 8080
  │   │
  │   └── NO → continue
  │
  ├── Q: Do you need programmatic browser control in Python?
  │   ├── YES → continue to Backend Selection
  │   └── NO → You probably don't need Wave. Re-evaluate your requirements.
  │
  └── Backend Selection:
      │
      ├── Q: Do you need to support Firefox?
      │   ├── YES → bidiwave
      │   │         ├── Need cross-browser testing? → bidiwave with Chrome + Firefox + Edge
      │   │         ├── Need network interception? → bidiwave client.network module
      │   │         ├── Need preload scripts? → bidiwave client.preload module
      │   │         ├── Need web extensions? → bidiwave client.web_extension module
      │   │         ├── Need W3C standard compliance? → bidiwave (W3C WebDriver BiDi)
      │   │         └── Need Chrome-specific CDP via BiDi? → bidiwave client.cdp bridge
      │   │
      │   └── NO → continue
      │
      ├── Q: Do you need Chrome-specific CDP features?
      │   ├── YES → cdpwave
      │   │         ├── Debugging with breakpoints? → cdpwave Debugger domain
      │   │         ├── CPU profiling? → cdpwave Profiler domain
      │   │         ├── Heap snapshots? → cdpwave HeapProfiler domain
      │   │         ├── Code coverage? → cdpwave Profiler + Page
      │   │         ├── WebAuthn? → cdpwave WebAuthn domain
      │   │         ├── Bluetooth? → cdpwave Bluetooth emulation
      │   │         ├── Cast? → cdpwave Cast domain
      │   │         ├── DOM debugger? → cdpwave DOMDebugger domain
      │   │         ├── Smart card? → cdpwave SmartCard domain
      │   │         └── Any CDP method? → cdpwave escape hatch: session.send("Domain.method", params)
      │   │
      │   └── NO → continue
      │
      ├── Q: Do you want both backends with a unified API?
      │   ├── YES → wavexis as a library
      │   │         ├── Switch backend per command: --backend cdp / --backend bidi
      │   │         ├── Full feature parity between backends
      │   │         └── AbstractBackend interface
      │   │
      │   └── NO → Default to cdpwave (simplest setup, no driver needed)
      │
      └── END
```

## Scenario-Based Recommendations

### Testing Scenarios

| Scenario | Tool | Backend | Why |
|----------|------|---------|-----|
| E2E test for Chrome only | cdpwave | CDP | No driver needed, full CDP access |
| E2E test for Chrome + Firefox | bidiwave | BiDi | W3C standard, cross-browser |
| E2E test with parallel browsers | bidiwave | BiDi | Run same test across Chrome, Firefox, Edge |
| Visual regression in CI | wavexis CLI | CDP | `visual-diff` command, exit codes |
| Performance regression in CI | wavexis CLI | CDP | `cwv --budget` command, exit codes |
| Accessibility audit in CI | wavexis CLI | CDP | `axe` command, a11y tree |
| LLM-driven test exploration | wavexis-mcp | CDP | `wavexis_act` for NL interaction |

### Scraping Scenarios

| Scenario | Tool | Backend | Why |
|----------|------|---------|-----|
| Simple page scrape | wavexis CLI | CDP | `scrape` command, one-liner |
| Anti-bot site scraping | wavexis CLI | CDP | `--stealth` flag |
| Multi-page crawling | wavexis CLI | CDP | `crawl` command |
| SPA scraping (wait for render) | wavexis CLI | CDP | `scrape` with wait, multi-action YAML |
| Shadow DOM scraping | wavexis CLI | CDP | `shadow` command |
| Batch URL processing | wavexis CLI | CDP | `batch` command with file input |
| Authenticated scraping | wavexis CLI | CDP | `auth` command with context JSON |
| LLM-driven scraping | wavexis-mcp | CDP | `wavexis_scrape` + `wavexis_act` |

### Development Scenarios

| Scenario | Tool | Backend | Why |
|----------|------|---------|-----|
| Quick screenshot during dev | wavexis CLI | CDP | `screenshot` command |
| Interactive browser session | wavexis CLI | CDP | `repl` command |
| Debug JS in browser | cdpwave | CDP | Debugger domain, breakpoints |
| Profile page performance | cdpwave | CDP | Profiler domain, CPU trace |
| Analyze memory leaks | cdpwave | CDP | HeapProfiler domain |
| Check code coverage | cdpwave | CDP | Profiler + Page coverage |
| Inspect network traffic | wavexis CLI | CDP | `har` command, `inspect` command |

### CI/CD Scenarios

| Scenario | Tool | Backend | Why |
|----------|------|---------|-----|
| Assert page title in CI | wavexis CLI | CDP | `eval --assert "== Expected"` |
| Visual regression on PR | wavexis CLI | CDP | `visual-diff` with baselines |
| Performance gate on deploy | wavexis CLI | CDP | `cwv --budget` with thresholds |
| Batch screenshots in CI | wavexis CLI | CDP | `batch` with URL file |
| Shared browser service | wavexis CLI | CDP | `serve` in Docker |
| LLM agent in CI pipeline | wavexis-mcp | CDP | HTTP transport, rate limiting |

### LLM/AI Agent Scenarios

| Scenario | Tool | Tiers | Why |
|----------|------|-------|-----|
| Basic browser control | wavexis-mcp | core | 72 tools, navigation, screenshot, eval |
| Network analysis | wavexis-mcp | core,network | +20 network tools |
| Accessibility audit | wavexis-mcp | core,a11y | +4 a11y tools |
| Performance debugging | wavexis-mcp | core,devtools | +31 devtools tools |
| Form filling via NL | wavexis-mcp | core | `wavexis_act` for NL interaction |
| Multi-step workflow | wavexis-mcp | core,workflows | Multi-action YAML batching |
| Full browser control | wavexis-mcp | all | All 220 tools |

# Tier Selection Guide

> Detailed guide for choosing the right capability tiers for each use case.

## Token Budget Considerations

Each tool definition consumes tokens in the LLM context window. Loading all 220 tools uses significantly more tokens than loading 72 (core only). Choose the minimal set of tiers that covers your use case.

| Tiers | Tools | Approx. tokens (tool defs) | Use when |
|-------|-------|---------------------------|----------|
| `core` | 72 | ~8K | Basic browser control, screenshots, scraping, form filling |
| `core,network` | 92 | ~10K | Scraping with network interception, HAR capture |
| `core,storage` | 90 | ~10K | Scraping with state management, auth persistence |
| `core,network,storage` | 110 | ~12K | Full scraping setup |
| `core,devtools` | 103 | ~12K | Performance debugging, CSS inspection, tracing |
| `core,a11y` | 76 | ~9K | Accessibility auditing |
| `core,testing` | 78 | ~9K | Automated testing with assertions |
| `core,vision` | 79 | ~9K | Pixel-precise mouse interaction |
| `core,video` | 76 | ~9K | Video recording of browser sessions |
| `core,data` | 79 | ~9K | Lighthouse audits, CWV, visual diff, crawling |
| `core,workflows` | 78 | ~9K | Multi-action YAML, raw CDP/BiDi access |
| `core,emulation` | 81 | ~9K | Device emulation, geolocation, timezone |
| `core,interactions` | 77 | ~9K | Dialogs, downloads, file choosers, permissions |
| `core,experimental` | 103 | ~12K | Service workers, WebAuthn, extensions, media, cast |
| `core,devtools,data` | 110 | ~12K | Performance debugging + audits |
| `core,network,storage,emulation` | 119 | ~13K | Full scraping + emulation |
| `core,devtools,a11y,data` | 114 | ~13K | Full debugging + accessibility + audits |
| `core,network,storage,devtools,data` | 137 | ~15K | Full debugging + scraping + audits |
| `all` | 220 | ~24K | Everything — maximum flexibility |

## Use Case Decision Matrix

### Scraping

| Scenario | Tiers | Why |
|----------|-------|-----|
| Simple page scrape | `core` | `wavexis_scrape` is enough |
| Authenticated scraping | `core,storage` | Persist cookies and localStorage |
| Anti-bot scraping | `core` + `--stealth` | Stealth flag hides automation |
| Network interception | `core,network` | Block ads, mock APIs, capture HAR |
| Multi-page crawl | `core,data` | `wavexis_crawl` for site-wide scraping |
| Structured data extraction | `core,data` | `wavexis_extract` with schema |
| Full scraping setup | `core,network,storage,data` | All scraping capabilities |

### Testing

| Scenario | Tiers | Why |
|----------|-------|-----|
| Basic E2E test | `core,testing` | Assertions + browser control |
| Visual regression | `core,vision,data` | `wavexis_visual_diff` + pixel-precise |
| Performance test | `core,data` | `wavexis_cwv` + `wavexis_lighthouse` |
| Accessibility test | `core,a11y` | `wavexis_axe_audit` + a11y tree |
| Network test | `core,network,testing` | Mock responses + assertions |
| Full test suite | `core,testing,a11y,data,vision` | All testing capabilities |

### Development & Debugging

| Scenario | Tiers | Why |
|----------|-------|-----|
| Quick screenshot | `core` | `wavexis_screenshot` |
| Console inspection | `core` | `wavexis_console_get` |
| CSS inspection | `core,devtools` | `wavexis_css_get_computed`, `wavexis_css_get_rules` |
| Performance profiling | `core,devtools` | `wavexis_perf_trace`, `wavexis_perf_profile` |
| Memory analysis | `core,devtools` | `wavexis_perf_heap_snapshot` |
| Code coverage | `core,devtools` | `wavexis_perf_coverage`, `wavexis_perf_css_coverage` |
| Debugging with breakpoints | `core,devtools` | `wavexis_debug_break`, `wavexis_debug_step` |
| Full debugging | `core,devtools,data` | All debug + audit tools |

### LLM Agent Workflows

| Scenario | Tiers | Why |
|----------|-------|-----|
| Basic agent control | `core` | NL interaction, screenshots, eval |
| Form filling | `core` | `wavexis_act` for NL form filling |
| Multi-step workflow | `core,workflows` | `wavexis_multi` for YAML chains |
| Agent + scraping | `core,network,storage` | Full scraping for agent |
| Agent + testing | `core,testing` | Assertions for agent validation |
| Full agent | `all` | Maximum flexibility |

### CI/CD

| Scenario | Tiers | Why |
|----------|-------|-----|
| Screenshot in CI | `core` | `wavexis_screenshot` |
| Assertion gate | `core,testing` | `wavexis_assert_*` tools |
| Performance gate | `core,data` | `wavexis_cwv` with budgets |
| Visual regression gate | `core,vision,data` | `wavexis_visual_diff` |
| Full CI pipeline | `core,testing,data,vision` | All CI-relevant tools |

### Media & Recording

| Scenario | Tiers | Why |
|----------|-------|-----|
| Video recording | `core,video` | `wavexis_video_start/stop` |
| Screenshot with annotations | `core,devtools` | `wavexis_annotate_screenshot` |
| Screencast frames | `core` | `wavexis_screenshot` in loop |
| Media control | `core,experimental` | `wavexis_media_play/pause/seek` |

### Specialized

| Scenario | Tiers | Why |
|----------|-------|-----|
| Service worker testing | `core,experimental` | `wavexis_sw_list/unregister/update` |
| WebAuthn testing | `core,experimental` | `wavexis_webauthn_add/credential` |
| Extension testing | `core,experimental` | `wavexis_extension_install/list` |
| PWA testing | `core,experimental` | `wavexis_pwa_install/uninstall` |
| Bluetooth emulation | `core,experimental` | `wavexis_bluetooth_emulate` |
| Cast testing | `core,experimental` | `wavexis_cast_start/stop` |
| Geolocation testing | `core,emulation` | `wavexis_emulate_geolocation` |
| Device testing | `core,emulation` | `wavexis_emulate_device` |

## Recommended Starting Points

| Role | Tiers | Tools | Description |
|------|-------|-------|-------------|
| **Minimal** | `core` | 72 | Basic browser control — start here |
| **Scraper** | `core,network,storage` | 110 | Full scraping with state and network |
| **Tester** | `core,testing,a11y` | 82 | E2E testing with accessibility |
| **Debugger** | `core,devtools,data` | 110 | Performance, CSS, debugging, audits |
| **Agent** | `core,workflows` | 78 | LLM agent with multi-action YAML |
| **Full** | `all` | 220 | Everything — use when token budget allows |

## Switching Tiers

You can change tiers by updating the `--caps` flag and restarting the server:

```bash
# Start with core only
uvx wavexis-mcp --caps core

# Later, add network and storage
uvx wavexis-mcp --caps core,network,storage

# Full power
uvx wavexis-mcp --caps all
```

For HTTP transport, update the server command and restart. For stdio, update the IDE config and reload.

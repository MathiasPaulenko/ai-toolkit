# Ecosystem Comparison — Full Feature Matrix

> Detailed comparison of all four Wave ecosystem tools across every capability.

## Tool Overview

| Tool | Layer | Language | Backends | Tools/Commands | Install Size |
|------|-------|----------|----------|----------------|-------------|
| cdpwave | Low-level CDP client | Python 3.11+ | CDP only | 689 typed methods | ~5MB |
| bidiwave | Low-level BiDi client | Python 3.11+ | BiDi only | 12 modules | ~5MB |
| wavexis | High-level CLI | Python 3.11+ | CDP + BiDi | 130+ commands, 480+ sub-commands | ~8MB |
| wavexis-mcp | MCP server | Python 3.11+ | CDP + BiDi | 220 MCP tools, 13 tiers | ~5MB |

## CDP Domain Coverage (cdpwave)

All 60 CDP domains implemented with 689 typed methods:

| Domain | Methods | Key Features |
|--------|---------|--------------|
| Accessibility | 5 | Tree snapshot, root, child nodes |
| Animation | 9 | Playback rate, timing, screenshots |
| Audits | 3 | Issue categories |
| AutoAttach | 1 | Worker auto-attach |
| BackgroundService | 4 | Service events, recording |
| Browser | 6 | Version, permissions, window bounds |
| CacheStorage | 7 | Cache entries, delete, request |
| Cast | 4 | Tab casting, start/stop |
| Console | 3 | Message storage, clearing |
| CSS | 20 | Styles, computed, stylesheets, rules |
| Database | 3 | SQL execution |
| Debugger | 34 | Breakpoints, step, pause, resume, scopes |
| DeviceAccess | 4 | Device selection, prompts |
| DeviceOrientation | 2 | Orientation override |
| DOM | 53 | Document, attributes, children, query |
| DOMDebugger | 11 | Event/DOM breakpoints |
| DOMStorage | 8 | Storage items, clear |
| Emulation | 26 | Device, viewport, geolocation, timezone |
| EventBreakpoints | 4 | Event listener breakpoints |
| FedCM | 7 | Federated credential management |
| Fetch | 12 | Request interception, continue, fail |
| FileSystem | 1 | Directory access |
| Headless | 3 | Frame control, enable/disable |
| HeapProfiler | 14 | Snapshots, sampling, tracking |
| IO | 3 | Read, write, close |
| IndexedDB | 8 | Database listing, data, clear |
| Input | 14 | Key, mouse, touch, IME |
| Inspector | 2 | Enable, disable |
| LayerTree | 10 | Layers, compositing reasons |
| Log | 5 | Enable, clear, violations |
| Memory | 12 | Sampling, pressure, tracking |
| Network | 42 | Cookies, headers, cache, intercept |
| Overlay | 12 | Highlight, inspect, screenshot |
| Page | 68 | Navigation, screenshot, PDF, capture |
| Performance | 4 | Metrics, timeline |
| PerformanceTimeline | 1 | Timeline enable |
| Preload | 2 | Preload enable/disable |
| Profiler | 10 | Start, stop, profile, samples |
| PWA | 7 | Install state, install, uninstall |
| Runtime | 25 | Evaluate, compile, properties |
| Schema | 1 | Domain listing |
| Sensor | 4 | Sensor reading override |
| ServiceWorker | 8 | Workers, update, unregister |
| SmartCard | 13 | Emulation, protocols |
| Storage | 8 | Quota, tracking, clear |
| SystemInfo | 3 | Info, process, features |
| Target | 20 | Create, close, activate, attach |
| Tethering | 2 | Bind, unbind |
| Tracing | 6 | Start, end, categories |
| WebAudio | 2 | Contexts |
| WebAuthn | 5 | Virtual authenticator, credentials |
| WebMCP | 2 | Enable, disable |
| Worker | 2 | Created, disconnected |
| + 7 more | — | Crash report, Device Access, Digital Credentials, Inspector, etc. |

## BiDi Module Coverage (bidiwave)

12 modules with full W3C WebDriver BiDi (WD 2025-07-28) coverage:

| Module | Key Features |
|--------|--------------|
| `client.browsing` | Contexts, navigation, screenshots, viewport, PDF, element waiting, CSS/XPath locators, dialog handling, download events, history |
| `client.script` | Evaluate JS, call functions, RemoteValue with match pattern, preload scripts, realm inspection, user activation |
| `client.input` | Clicks, keyboard, scroll, drag & drop, file upload, file dialog events |
| `client.network` | Block, modify, mock requests, cache overrides, response body, auth, extra headers, data collectors |
| `client.storage` | Get, set, delete cookies with full attributes, partition key, cookie change monitoring |
| `client.emulation` | Geolocation, locale, screen orientation, timezone, user agent, network conditions |
| `client.permissions` | Grant or deny browser permissions without dialogs |
| `client.preload` | Inject JS before page load with channel communication, user context |
| `client.log` | Console log entry monitoring with async handlers |
| `client.web_extension` | Install and uninstall browser extensions |
| `client.cdp` | CDP bridge for Chrome-specific features |
| `client.session` | Session management, subscription, reconnection |

## wavexis-mcp Capability Tiers

13 tiers from `core` (72 tools) to `all` (220 tools):

| Tier | Flag | Tools | Key Features |
|------|------|-------|--------------|
| Core | always on | 72 | Session, navigation, screenshot, PDF, scrape, eval, DOM, input, cookies, tabs, NL interaction, iframe, shadow DOM, events |
| Network | `--caps=network` | 20 | Headers, UA, block, throttle, cache, HAR, intercept, mock, modify req/resp, request body, replay HAR, request list |
| Storage | `--caps=storage` | 18 | localStorage, sessionStorage, cache storage, IndexedDB, state save/restore |
| Emulation | `--caps=emulation` | 9 | Device, viewport, geolocation, timezone, dark mode, locale, CPU, touch, sensors |
| A11y | `--caps=a11y` | 4 | Accessibility tree snapshot, node traversal, axe-core audit |
| Interactions | `--caps=interactions` | 5 | Dialogs, downloads, permissions |
| DevTools | `--caps=devtools` | 31 | Performance, CSS, debugging, overlay, console, security, window mgmt, combined trace, annotated screenshot |
| Vision | `--caps=vision` | 7 | Coordinate-based mouse (pixel-precise) |
| Video | `--caps=video` | 4 | Video recording, chapters, action overlay |
| Testing | `--caps=testing` | 6 | Assertions, locator generation |
| Workflows | `--caps=workflows` | 6 | Multi-action YAML, raw CDP/BiDi, browser context CRUD |
| Data | `--caps=data` | 7 | Codegen, Lighthouse audit, extract, websocket intercept, crawl, visual diff, core web vitals |
| Experimental | `--caps=experimental` | 31 | Service workers, animations, WebAuthn, WebAudio, media, cast, bluetooth, extensions, prefs |
| **Total** | `--caps=all` | **220** | |

## Performance Comparison

| Metric | WaveXisMCP | Playwright MCP |
|--------|-----------|----------------|
| Language | Python | TypeScript |
| Node.js required | No | Yes |
| Downloads Chromium (~200MB) | No | Yes |
| Install size | ~5MB | ~400MB |
| Cold start | 0.8s | 3.2s |
| Total tools | 220 | ~21 |
| Capability tiers | 13 (opt-in) | No |
| Dual protocol (CDP + BiDi) | Yes | No |
| Firefox support | Yes (BiDi + geckodriver) | Basic |
| Stealth mode | Yes | No |
| Rate limiting | Yes | No |
| SSRF protection | Yes | No |
| Structured errors with suggestions | Yes | No |

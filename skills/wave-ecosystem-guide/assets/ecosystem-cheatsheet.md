# Wave Ecosystem Cheatsheet

> Quick reference card for the Wave browser automation ecosystem.

## Tools at a Glance

| Tool | One-liner | Install |
|------|-----------|---------|
| **cdpwave** | CDP client for Chrome/Edge (60 domains, 689 methods) | `pip install cdpwave` |
| **bidiwave** | BiDi client for Chrome + Firefox + Edge (W3C) | `pip install bidiwave` |
| **wavexis** | CLI wrapping cdpwave + bidiwave (130+ commands) | `pip install wavexis[cdp]` |
| **wavexis-mcp** | MCP server with 220 tools for LLMs | `pip install wavexis-mcp[cdp]` |

## Architecture

```
wavexis-mcp (220 MCP tools, 13 tiers)
└─ wavexis (CLI, 130+ commands)
     ├─ cdpwave (CDP, Chrome/Edge)
     └─ bidiwave (BiDi, Chrome/Firefox/Edge)
```

## Quick Decision

| Need | Use |
|------|-----|
| LLM controls browser | wavexis-mcp |
| One-off CLI task | wavexis |
| Chrome-only Python script | cdpwave |
| Cross-browser Python script | bidiwave |
| Not sure | Start with wavexis CLI |

## Backend Choice

| Need | Backend |
|------|---------|
| Chrome/Edge only, no driver | CDP (cdpwave) |
| Firefox support | BiDi (bidiwave) |
| W3C standard compliance | BiDi (bidiwave) |
| Max CDP coverage (debug, profile) | CDP (cdpwave) |
| Both, switchable | wavexis `--backend cdp` / `--backend bidi` |

## wavexis CLI — Common Commands

```bash
# Capture
wavexis screenshot <url> -o out.png [--full-page] [--selector "h1"]
wavexis pdf <url> -o out.pdf [--paper a4]
wavexis scrape <url> --selector "article"

# Evaluate
wavexis eval <url> -e "document.title"
wavexis eval <url> -e "..." --assert "== Expected Title"

# Navigate
wavexis navigate <url>
wavexis repl

# Performance
wavexis perf <url> [-m trace|profile|coverage|heap-snapshot]
wavexis cwv <url> [--budget '{"lcp_ms":2500,"cls":0.1,"inp_ms":200}']

# Network
wavexis har <url> -o out.har
wavexis intercept <url> -p "*/api/*" --block
wavexis mock <url> -p "*/api/*" -b '{"mock":true}' -s 200

# Stealth
wavexis --stealth scrape <url> --selector "article"

# Multi-action
wavexis multi config.yml [--watch] [--dry-run] [--parallel]

# Batch & Crawl
wavexis batch urls.txt --action screenshot
wavexis crawl <url>

# Serve
wavexis serve --host 0.0.0.0 --port 8080

# Record & Replay
wavexis record <url> --interactive -o session.yml
wavexis replay session.yml
```

## wavexis-mcp — Capability Tiers

| Tier | Flag | Tools |
|------|------|-------|
| Core | always on | 72 |
| Network | `--caps=network` | +20 |
| Storage | `--caps=storage` | +18 |
| Emulation | `--caps=emulation` | +9 |
| A11y | `--caps=a11y` | +4 |
| Interactions | `--caps=interactions` | +5 |
| DevTools | `--caps=devtools` | +31 |
| Vision | `--caps=vision` | +7 |
| Video | `--caps=video` | +4 |
| Testing | `--caps=testing` | +6 |
| Workflows | `--caps=workflows` | +6 |
| Data | `--caps=data` | +7 |
| Experimental | `--caps=experimental` | +31 |
| **All** | `--caps=all` | **220** |

**Recommended:** `--caps core,network,storage` (110 tools) for most tasks.

## MCP Config (any IDE)

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

## cdpwave — Quick Start

```python
import asyncio
from cdpwave import CDPClient

async def main() -> None:
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        result = await session.runtime.evaluate("document.title", return_by_value=True)
        print(result["result"]["value"])
        await session.close()

asyncio.run(main())
```

## bidiwave — Quick Start

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

## Key Differences vs Competitors

| Feature | Wave | Playwright | Selenium |
|---------|------|------------|----------|
| Node.js | Not needed | Required | Not needed |
| Browser download | Not needed | Required (~200MB) | Required |
| Install size | ~5MB | ~400MB | ~50MB |
| Language | Python | Multi | Multi |
| CDP + BiDi | Both | CDP only | WebDriver only |
| MCP tools | 220 | ~21 | — |
| Stealth mode | Yes | No | No |
| Async-first | Yes | Yes | No |

## Links

| Resource | URL |
|----------|-----|
| cdpwave | https://github.com/MathiasPaulenko/cdpwave |
| bidiwave | https://github.com/MathiasPaulenko/bidiwave |
| wavexis | https://github.com/MathiasPaulenko/wavexis |
| wavexis-mcp | https://github.com/MathiasPaulenko/wavexis-mcp |

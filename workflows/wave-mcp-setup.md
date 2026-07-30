---
name: MCP Setup Workflow
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Complete setup of wavexis-mcp in any IDE. Covers installation, capability tier selection, client configuration (Claude Desktop, Cursor, Windsurf, VS Code), verification, rate limiting, HTTP transport, and Docker deployment."
tags: [mcp-setup, wavexis-mcp, configuration]
role: mcp-orchestrator
---

# MCP Setup Workflow

Complete setup of wavexis-mcp in any MCP-compatible IDE. Install the server, choose capability tiers, configure the client, verify browser detection, and test with a simple tool call.

## Prerequisites

- [ ] Python 3.11+ installed
- [ ] Chrome 112+ installed (for CDP backend)
- [ ] Firefox installed (optional, for BiDi backend)
- [ ] MCP-compatible IDE installed (Claude Desktop, Cursor, Windsurf, or VS Code)
- [ ] `pip` or `uv` available

## Phase 1: Install wavexis-mcp

### Option A: pip install (recommended for persistent setups)

```bash
pip install wavexis-mcp[cdp]
```

Install with BiDi support for cross-browser:

```bash
pip install wavexis-mcp[cdp,bidi]
```

Install with all optional dependencies:

```bash
pip install wavexis-mcp[all]
```

### Option B: uvx (recommended for ephemeral runs)

```bash
uvx wavexis-mcp --caps core
```

### Option C: from source

```bash
git clone https://github.com/MathiasPaulenko/wavexis-mcp.git
cd wavexis-mcp
pip install -e ".[cdp]"
```

### Verify Installation

```bash
wavexis-mcp --version
wavexis-mcp --help
```

## Phase 2: Choose Capability Tiers

### Available Tiers

| Tier | Description | Tools Included |
|------|-------------|----------------|
| `core` | Navigation, screenshots, eval | `navigate`, `screenshot`, `eval`, `get_title`, `get_url` |
| `interactions` | Click, input, scroll | `click`, `input`, `scroll`, `select`, `keypress` |
| `network` | HAR, interception, throttling | `har`, `inspect`, `mock`, `throttle` |
| `a11y` | Accessibility audits | `a11y_tree`, `a11y_node`, `axe` |
| `data` | Scraping, extraction | `scrape`, `extract`, `get_text`, `get_links` |
| `devtools` | Console, performance | `console`, `perf`, `cwv`, `coverage` |
| `testing` | Assertions, visual diff | `assert`, `visual_diff`, `wait_for` |
| `video` | Recording, screenshots | `record`, `screenshot_full` |
| `vision` | AI visual analysis | `analyze_screenshot`, `compare_visuals` |
| `emulation` | Device, network, geo | `emulate_device`, `set_geolocation` |
| `storage` | Cookies, localStorage | `get_cookies`, `set_cookies`, `clear_storage` |
| `workflows` | Multi-action YAML | `run_workflow`, `session_open`, `session_close` |
| `experimental` | Unstable features | Varies — check release notes |

### Selection Guide

| Use Case | Recommended Tiers |
|----------|-------------------|
| General browsing & screenshots | `core` |
| Form filling & interaction | `core,interactions` |
| Accessibility testing | `core,a11y` |
| Network testing & mocking | `core,network` |
| Web scraping | `core,data` |
| Performance auditing | `core,devtools` |
| CI/CD testing | `core,testing` |
| Visual regression | `core,testing,video` |
| Auth flow testing | `core,interactions,storage` |
| Multi-step automation | `core,workflows` |
| Device testing | `core,emulation` |
| Full-featured (development) | `core,interactions,network,a11y,data,devtools,testing` |

### Minimal vs Full Configuration

```bash
# Minimal — just navigation and screenshots
wavexis-mcp --caps core

# Development — most common tiers
wavexis-mcp --caps core,interactions,network,a11y,testing

# Full — all stable tiers
wavexis-mcp --caps core,interactions,network,a11y,data,devtools,testing,video,emulation,storage,workflows
```

## Phase 3: Add MCP Config to IDE

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "wavexis": {
      "command": "wavexis-mcp",
      "args": ["--caps", "core,interactions,network,a11y,testing"],
      "env": {
        "WAVEXIS_HEADLESS": "true",
        "WAVEXIS_TIMEOUT": "30000"
      }
    }
  }
}
```

Restart Claude Desktop after saving.

### Cursor

Edit `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "wavexis": {
      "command": "wavexis-mcp",
      "args": ["--caps", "core,interactions,testing"],
      "env": {
        "WAVEXIS_HEADLESS": "true"
      }
    }
  }
}
```

Or use the Cursor UI: Settings → MCP → Add Server.

### Windsurf

Edit `.windsurf/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "wavexis": {
      "command": "wavexis-mcp",
      "args": ["--caps", "core,interactions,network,devtools"],
      "env": {
        "WAVEXIS_HEADLESS": "true",
        "WAVEXIS_RATE_LIMIT": "10"
      }
    }
  }
}
```

### VS Code

Edit `settings.json` (via Command Palette → Preferences: Open Settings (JSON)):

```json
{
  "mcp.servers": {
    "wavexis": {
      "command": "wavexis-mcp",
      "args": ["--caps", "core,interactions,a11y,testing"],
      "env": {
        "WAVEXIS_HEADLESS": "true"
      }
    }
  }
}
```

Install the MCP extension for VS Code if not already installed.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WAVEXIS_HEADLESS` | `false` | Run browser in headless mode |
| `WAVEXIS_TIMEOUT` | `30000` | Default timeout in milliseconds |
| `WAVEXIS_RATE_LIMIT` | `0` (disabled) | Max tool calls per second |
| `WAVEXIS_BROWSER` | `chrome` | Default browser (`chrome`, `firefox`, `edge`) |
| `WAVEXIS_REMOTE_URL` | none | Remote debugging URL |
| `WAVEXIS_LOG_LEVEL` | `info` | Log level (`debug`, `info`, `warning`, `error`) |

## Phase 4: Verify Browser Detection

### Step 1: Run Install Check

```bash
wavexis-mcp --install-check
```

Expected output:

```text
Browser Detection:
  Chrome:   Found (version 128.0.0.0)  /usr/bin/google-chrome
  Firefox:  Found (version 129.0.0.0)  /usr/bin/firefox
  Edge:     Not found

MCP Server:
  wavexis-mcp: 1.0.0
  Python:       3.11.7
  Backends:     cdp, bidi

All checks passed.
```

### Step 2: Verify MCP Connection

In your IDE, check that the wavexis MCP server appears in the server list:

- **Claude Desktop**: Look for "wavexis" in the tools panel
- **Cursor**: Settings → MCP → Server status should be "Connected"
- **Windsurf**: Check MCP panel for wavexis server
- **VS Code**: MCP extension should show wavexis as connected

### Step 3: List Available Tools

Ask the LLM to list available wavexis tools:

```text
List all available wavexis MCP tools.
```

Expected response includes tools matching your configured capability tiers.

## Phase 5: Test with a Simple Screenshot

### Step 1: Take a Screenshot

Ask the LLM:

```text
Take a screenshot of https://example.com using wavexis.
```

The LLM should call the `wavexis_screenshot` tool and return a screenshot.

### Step 2: Navigate and Get Title

```text
Navigate to https://example.com and tell me the page title.
```

### Step 3: Run an Accessibility Audit

```text
Run an accessibility audit on https://example.com using wavexis.
```

### Step 4: Test Session Mode

```text
Open a wavexis session, navigate to https://example.com,
click on the "More information" link, and take a screenshot.
Then close the session.
```

## Phase 6: Configure Rate Limiting (Optional)

### Why Rate Limit?

- Prevent LLMs from making too many tool calls in rapid succession
- Reduce browser resource consumption
- Avoid hitting rate limits on target websites

### Configuration

Set the `WAVEXIS_RATE_LIMIT` environment variable in your MCP config:

```json
{
  "env": {
    "WAVEXIS_RATE_LIMIT": "10"
  }
}
```

This limits wavexis to 10 tool calls per second.

### Rate Limit Behavior

| Setting | Behavior |
|---------|----------|
| `0` | No rate limiting (default) |
| `1` | 1 call per second (very conservative) |
| `5` | 5 calls per second (moderate) |
| `10` | 10 calls per second (recommended for most use cases) |
| `20` | 20 calls per second (aggressive) |

When rate limited, tool calls are queued and processed at the configured rate. The LLM receives a "rate limited, retrying" message.

## Phase 7: Set Up HTTP Transport (Optional)

For shared instances or remote access, use HTTP transport instead of stdio:

### Step 1: Start wavexis-mcp in HTTP Mode

```bash
wavexis-mcp --transport http --port 8080 --caps core,interactions
```

### Step 2: Configure Client for HTTP

```json
{
  "mcpServers": {
    "wavexis": {
      "url": "http://localhost:8080/mcp",
      "transport": "http"
    }
  }
}
```

### Step 3: Secure with Reverse Proxy

For production, put behind a reverse proxy with authentication:

```nginx
server {
    listen 443 ssl;
    server_name wavexis-mcp.example.com;

    ssl_certificate /etc/ssl/certs/wavexis.crt;
    ssl_certificate_key /etc/ssl/private/wavexis.key;

    location /mcp {
        proxy_pass http://localhost:8080/mcp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        # Basic auth
        auth_basic "wavexis-mcp";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }
}
```

## Phase 8: Deploy with Docker (Optional)

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget gnupg2 \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    && apt-get -f install -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install wavexis-mcp[cdp]

EXPOSE 8080

CMD ["wavexis-mcp", "--transport", "http", "--port", "8080", "--caps", "core,interactions", "--headless"]
```

### Step 2: Build and Run

```bash
docker build -t wavexis-mcp .
docker run -d -p 8080:8080 --name wavexis-mcp wavexis-mcp
```

### Step 3: Configure Client

```json
{
  "mcpServers": {
    "wavexis": {
      "url": "http://localhost:8080/mcp",
      "transport": "http"
    }
  }
}
```

### Step 4: Docker Compose (Optional)

```yaml
version: "3.8"

services:
  wavexis-mcp:
    build: .
    ports:
      - "8080:8080"
    environment:
      - WAVEXIS_HEADLESS=true
      - WAVEXIS_TIMEOUT=30000
      - WAVEXIS_RATE_LIMIT=10
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Troubleshooting

### Server not appearing in IDE

| Cause | Fix |
|-------|-----|
| Config file path wrong | Check IDE-specific config path |
| JSON syntax error | Validate JSON with `jq` |
| Command not found | Ensure `wavexis-mcp` is in PATH |
| Permission denied | Check file permissions on config |

### Browser not detected

| Cause | Fix |
|-------|-----|
| Chrome not installed | Install Chrome 112+ |
| Wrong Chrome path | Set `WAVEXIS_CHROME_PATH` env var |
| Headless not supported | Update Chrome to latest version |

### Tool calls timing out

| Cause | Fix |
|-------|-----|
| Page too slow | Increase `WAVEXIS_TIMEOUT` |
| Network issues | Check connectivity to target URL |
| Rate limiting | Increase or disable `WAVEXIS_RATE_LIMIT` |

### Connection drops

| Cause | Fix |
|-------|-----|
| Browser crashed | Check `WAVEXIS_LOG_LEVEL=debug` for details |
| Memory exhaustion | Use headless mode, reduce concurrent sessions |
| Docker resource limits | Increase container memory/CPU limits |

## Checklist

- [ ] wavexis-mcp installed (`pip install` or `uvx`)
- [ ] Capability tiers selected based on use case
- [ ] MCP config added to IDE (Claude Desktop / Cursor / Windsurf / VS Code)
- [ ] IDE restarted after config change
- [ ] Browser detection verified (`wavexis-mcp --install-check`)
- [ ] MCP server connected in IDE
- [ ] Screenshot test passed
- [ ] Navigation test passed
- [ ] Session mode test passed (if using `workflows` tier)
- [ ] Rate limiting configured (if needed)
- [ ] HTTP transport configured (if using shared instance)
- [ ] Docker deployment configured (if using containers)
- [ ] Environment variables documented for team

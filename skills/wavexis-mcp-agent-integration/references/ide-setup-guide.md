# IDE Setup Guide — Step-by-Step Configuration

> Complete guide for configuring wavexis-mcp in every supported IDE and MCP client.

## Prerequisites

1. **Python 3.11+** installed
2. **Chrome or Edge** installed (for CDP backend)
3. **uvx** available (install with `pip install uv` or `pipx install uv`)
4. **wavexis-mcp** installed or available via `uvx`

### Verify prerequisites

```bash
python --version    # 3.11+
uvx --version       # uv/uvx installed
wavexis-mcp --version  # or: uvx wavexis-mcp --version
```

---

## Claude Desktop

### macOS

Config file: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows

Config file: `%APPDATA%\Claude\claude_desktop_config.json`

### Configuration

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

### With stealth mode

```json
{
  "mcpServers": {
    "wavexis": {
      "command": "uvx",
      "args": ["wavexis-mcp", "--caps", "all", "--stealth"]
    }
  }
}
```

### With specific backend

```json
{
  "mcpServers": {
    "wavexis": {
      "command": "uvx",
      "args": ["wavexis-mcp", "--caps", "all", "--backend", "bidi"]
    }
  }
}
```

### Steps

1. Open Claude Desktop
2. Go to Settings → Developer → Edit Config
3. Paste the configuration above
4. Save and restart Claude Desktop
5. Verify: Ask Claude "Take a screenshot of https://example.com"

---

## Cursor

### Project-level config

Create `.cursor/mcp.json` in your project root:

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

### Global config

Create `~/.cursor/mcp.json` (macOS/Linux) or `%USERPROFILE%\.cursor\mcp.json` (Windows):

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

### Steps

1. Create the config file
2. Open Cursor
3. Go to Settings → MCP
4. Verify the wavexis server appears and is connected
5. Test: Ask Cursor "Use wavexis to scrape https://example.com"

---

## Windsurf

### Configuration

Add to Windsurf MCP settings (Settings → MCP Servers):

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

### With rate limiting

```json
{
  "mcpServers": {
    "wavexis": {
      "command": "uvx",
      "args": ["wavexis-mcp", "--caps", "all", "--rate-limit", "60"]
    }
  }
}
```

### Steps

1. Open Windsurf
2. Go to Settings → MCP Servers → Add Server
3. Paste the configuration
4. Save and restart Windsurf
5. Verify: Ask Windsurf "Take a full-page screenshot of https://example.com"

---

## VS Code (GitHub Copilot)

### Project-level config

Create `.vscode/mcp.json` in your project:

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

### Steps

1. Create `.vscode/mcp.json` in your project root
2. Open VS Code
3. Go to Command Palette → "MCP: List Servers"
4. Verify wavexis appears and is running
5. Test: Ask Copilot Chat "Use wavexis to get the title of https://example.com"

---

## HTTP Transport (Remote)

### Start the server

```bash
wavexis-mcp --transport http --host 0.0.0.0 --port 8765 --caps all
```

### Client configuration

```json
{
  "mcpServers": {
    "wavexis": {
      "url": "http://localhost:8765"
    }
  }
}
```

### With authentication (reverse proxy)

Set up Nginx or Caddy in front of wavexis-mcp:

```nginx
server {
    listen 443 ssl;
    server_name wavexis-mcp.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    auth_basic "MCP Access";
    auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        proxy_pass http://127.0.0.1:8765;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Client config:

```json
{
  "mcpServers": {
    "wavexis": {
      "url": "https://wavexis-mcp.example.com"
    }
  }
}
```

---

## Docker

### Docker run

```bash
docker run -p 8765:8765 ghcr.io/mathiaspaulenko/wavexis-mcp:latest \
  --transport http --caps all --host 0.0.0.0
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
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8765/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Client config for Docker

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

## Troubleshooting

### Server not appearing in IDE

1. Check the config file path is correct for your OS
2. Verify `uvx` is in PATH: `which uvx` (macOS/Linux) or `where uvx` (Windows)
3. Check JSON syntax is valid
4. Restart the IDE after saving config

### Tools not available

1. Check `--caps` flag includes the needed tier
2. Run `wavexis-mcp --caps <your_caps>` manually to see startup errors
3. Check the IDE's MCP logs for error messages

### Browser not found

1. Install Chrome or Edge
2. Set `--browser-path` to the executable:
   ```json
   {
     "mcpServers": {
       "wavexis": {
         "command": "uvx",
         "args": ["wavexis-mcp", "--caps", "all", "--browser-path", "/usr/bin/google-chrome"]
       }
     }
   }
   ```
3. Run `wavexis-mcp install_check` to verify

### Session errors

1. Check `wavexis_session_list` for active sessions
2. Close stale sessions with `wavexis_session_close`
3. Increase `--max-sessions` if needed

### Rate limit errors

1. Increase `--rate-limit` value
2. Or disable rate limiting: `--rate-limit 0`
3. Optimize workflow to use `wavexis_multi` for batched actions

### Connection refused (HTTP transport)

1. Verify the server is running: `curl http://localhost:8765/health`
2. Check firewall rules
3. Verify `--host` and `--port` match the client config
4. For remote access, use `--allow-remote` behind a reverse proxy

# Serve Mode — HTTP API, WebSocket, and Docker

> Complete guide to wavexis serve mode for shared browser automation via HTTP API.

## Overview

Serve mode turns wavexis into an HTTP API server with WebSocket streaming. This enables:

- Shared browser access for teams
- Browser automation as a service
- Integration with non-Python applications
- Real-time streaming of browser events
- Docker deployment for scalable browser infrastructure

## Starting the Server

### Basic

```bash
wavexis serve
```

Default: `127.0.0.1:8080`

### Custom host and port

```bash
wavexis serve --host 0.0.0.0 --port 9090
```

### With rate limiting

```bash
wavexis serve --host 0.0.0.0 --port 8080 --rate-limit 60
```

60 requests per minute per client.

### Allow remote connections

```bash
wavexis serve --host 0.0.0.0 --port 8080 --allow-remote
```

**Warning:** Only use `--allow-remote` behind a reverse proxy with authentication.

---

## HTTP API Endpoints

### `POST /screenshot`

Take a screenshot.

```bash
curl -X POST http://localhost:8080/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "full_page": true}' \
  -o screenshot.png
```

Request body:

```json
{
  "url": "https://example.com",
  "full_page": false,
  "selector": null,
  "format": "png",
  "quality": 80,
  "delay": 0,
  "wait_for": null,
  "viewport": null,
  "device": null
}
```

Response: Binary image data (`image/png`, `image/jpeg`, `image/webp`).

### `POST /pdf`

Generate a PDF.

```bash
curl -X POST http://localhost:8080/pdf \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "paper": "a4"}' \
  -o output.pdf
```

Request body:

```json
{
  "url": "https://example.com",
  "paper": "a4",
  "landscape": false,
  "scale": 1.0,
  "print_background": true,
  "margin": {"top": "1cm", "bottom": "1cm", "left": "1cm", "right": "1cm"}
}
```

Response: Binary PDF data (`application/pdf`).

### `POST /scrape`

Scrape page content.

```bash
curl -X POST http://localhost:8080/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "selector": "article", "format": "markdown"}'
```

Request body:

```json
{
  "url": "https://example.com",
  "selector": "body",
  "format": "text",
  "wait_for": null,
  "delay": 0
}
```

Response: JSON with scraped content.

### `POST /eval`

Evaluate JavaScript.

```bash
curl -X POST http://localhost:8080/eval \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "expression": "document.title"}'
```

Request body:

```json
{
  "url": "https://example.com",
  "expression": "document.title",
  "return_by_value": true,
  "await_promise": false
}
```

Response: JSON with evaluation result.

### `POST /navigate`

Navigate to a URL.

```bash
curl -X POST http://localhost:8080/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "wait_until": "load"}'
```

### `POST /cookies`

Get, set, delete, or clear cookies.

```bash
# Get cookies
curl -X POST http://localhost:8080/cookies \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "action": "get"}'

# Set cookie
curl -X POST http://localhost:8080/cookies \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "action": "set",
    "name": "session",
    "value": "abc123",
    "domain": "example.com"
  }'
```

### `POST /perf`

Get performance metrics.

```bash
curl -X POST http://localhost:8080/perf \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "mode": "metrics"}'
```

### `POST /cwv`

Core Web Vitals scoring.

```bash
curl -X POST http://localhost:8080/cwv \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "budget": {"lcp_ms": 2500, "cls": 0.1, "inp_ms": 200}
  }'
```

### `POST /multi`

Execute a multi-action YAML config.

```bash
curl -X POST http://localhost:8080/multi \
  -H "Content-Type: application/json" \
  -d '{"config": "actions:\n  - navigate: https://example.com\n  - screenshot: {full_page: true}"}'
```

### `GET /health`

Health check.

```bash
curl http://localhost:8080/health
```

Response:

```json
{
  "status": "ok",
  "backend": "cdp",
  "browser": "Chrome/125.0.6422.142",
  "uptime": 3600
}
```

### `GET /backends`

List available backends.

```bash
curl http://localhost:8080/backends
```

---

## WebSocket Streaming

Connect to `ws://localhost:8080/ws` for real-time browser event streaming.

### Events

| Event | Description |
|-------|-------------|
| `screenshot` | Screenshot frames (base64) |
| `console` | Console log messages |
| `navigation` | Navigation events |
| `dom_mutation` | DOM mutations |
| `network_request` | Network requests |
| `network_response` | Network responses |
| `performance` | Performance metrics |
| `error` | Error events |

### JavaScript client example

```javascript
const ws = new WebSocket("ws://localhost:8080/ws");

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.type, data.payload);
};

// Send a command
ws.send(JSON.stringify({
  type: "navigate",
  url: "https://example.com"
}));
```

### Python client example

```python
import asyncio
import websockets
import json

async def main():
    async with websockets.connect("ws://localhost:8080/ws") as ws:
        # Send a command
        await ws.send(json.dumps({
            "type": "navigate",
            "url": "https://example.com"
        }))

        # Listen for events
        async for message in ws:
            data = json.loads(message)
            print(f"[{data['type']}] {data['payload']}")

asyncio.run(main())
```

---

## Docker Deployment

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
      - WAVEXIS_RATE_LIMIT=60
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wavexis
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wavexis
  template:
    metadata:
      labels:
        app: wavexis
    spec:
      containers:
        - name: wavexis
          image: ghcr.io/mathiaspaulenko/wavexis:latest
          ports:
            - containerPort: 8080
          env:
            - name: WAVEXIS_BACKEND
              value: cdp
            - name: WAVEXIS_RATE_LIMIT
              value: "60"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 30
          resources:
            limits:
              memory: "1Gi"
              cpu: "1000m"
            requests:
              memory: "512Mi"
              cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: wavexis
spec:
  selector:
    app: wavexis
  ports:
    - port: 80
      targetPort: 8080
  type: LoadBalancer
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WAVEXIS_BACKEND` | Backend: `cdp` or `bidi` | `cdp` |
| `WAVEXIS_HOST` | Bind address | `127.0.0.1` |
| `WAVEXIS_PORT` | Port | `8080` |
| `WAVEXIS_RATE_LIMIT` | Requests per minute | `0` (disabled) |
| `WAVEXIS_ALLOW_REMOTE` | Allow remote connections | `false` |
| `WAVEXIS_BROWSER_PATH` | Custom browser executable | Auto-detected |
| `WAVEXIS_HEADLESS` | Run headless | `true` |
| `WAVEXIS_TIMEOUT` | Default timeout (ms) | `30000` |

---

## Security Considerations

- **Never expose serve mode directly to the internet** — Use a reverse proxy with authentication
- **Enable rate limiting** — Prevent abuse with `--rate-limit`
- **Use SSRF protection** — wavexis blocks requests to private IP ranges by default
- **Restrict `--allow-remote`** — Only enable behind a firewall or VPN
- **Use HTTPS** — Terminate TLS at the reverse proxy level
- **Validate input** — Sanitize URLs and expressions in your API wrapper

### Nginx reverse proxy example

```nginx
server {
    listen 443 ssl;
    server_name wavexis.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Rate limiting
        limit_req zone=wavexis burst=10 nodelay;
    }
}
```

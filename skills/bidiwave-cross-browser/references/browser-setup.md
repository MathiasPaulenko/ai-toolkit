# Browser Setup Guide — Chrome, Firefox, Edge

> Complete guide for setting up BiDi-capable browser endpoints for bidiwave.

## Prerequisites

- Python 3.11+
- `pip install bidiwave`
- At least one of: Chrome, Firefox, or Edge installed

## Chrome Setup

### Option 1: ChromeDriver (recommended)

Chrome requires ChromeDriver as a BiDi proxy.

#### Install ChromeDriver

```bash
# macOS (via Homebrew)
brew install chromedriver

# Linux (via package manager)
sudo apt install chromium-chromedriver

# Windows (via Chocolatey)
choco install chromedriver

# Or download manually from:
# https://googlechromelabs.github.io/chrome-for-testing/
```

#### Start ChromeDriver

```bash
chromedriver --port=9515
```

#### Verify

```bash
curl http://localhost:9515/status
# Should return JSON with "ready": true
```

#### Connect with bidiwave

```python
from bidiwave import BiDiClient

async with await BiDiClient.connect("ws://localhost:9515/session") as client:
    # ...
```

### Option 2: Chrome with --remote-debugging-port

Chrome can also expose BiDi directly without ChromeDriver:

```bash
google-chrome --headless --remote-debugging-port=9222
```

```python
async with await BiDiClient.connect("ws://localhost:9222/session") as client:
    # ...
```

### Chrome flags for testing

```bash
google-chrome \
    --headless \
    --no-sandbox \
    --disable-gpu \
    --disable-dev-shm-usage \
    --remote-debugging-port=9222
```

### Chrome in Docker

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-chromedriver \
    && rm -rf /var/lib/apt/lists/*

RUN pip install bidiwave

CMD ["chromedriver", "--port=9515"]
```

## Firefox Setup

Firefox implements BiDi natively — no driver needed.

### Start Firefox with remote debugging

```bash
firefox --headless --remote-debugging-port=9223 --no-remote
```

### Verify

```bash
curl http://localhost:9223/status
# Should return JSON with BiDi status
```

### Connect with bidiwave

```python
from bidiwave import BiDiClient

async with await BiDiClient.connect("ws://localhost:9223/session") as client:
    # ...
```

### Firefox flags for testing

```bash
firefox \
    --headless \
    --remote-debugging-port=9223 \
    --no-remote \
    --safe-mode
```

### Firefox in Docker

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

RUN pip install bidiwave

CMD ["firefox", "--headless", "--remote-debugging-port=9223", "--no-remote"]
```

### Firefox with Geckodriver (alternative)

If native BiDi is not available, use Geckodriver:

```bash
geckodriver --port=4444
```

```python
async with await BiDiClient.connect("ws://localhost:4444/session") as client:
    # ...
```

## Edge Setup

Edge requires EdgeDriver as a BiDi proxy.

### Install EdgeDriver

```bash
# macOS (via Homebrew)
brew install --cask microsoft-edge

# Download EdgeDriver from:
# https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

# Linux (via package manager)
sudo apt install microsoft-edge-stable
```

### Start EdgeDriver

```bash
msedgedriver --port=9516
```

### Verify

```bash
curl http://localhost:9516/status
# Should return JSON with "ready": true
```

### Connect with bidiwave

```python
from bidiwave import BiDiClient

async with await BiDiClient.connect("ws://localhost:9516/session") as client:
    # ...
```

### Edge in Docker

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    microsoft-edge-stable \
    && rm -rf /var/lib/apt/lists/*

RUN pip install bidiwave

CMD ["msedgedriver", "--port=9516"]
```

## Multi-Browser Setup

For cross-browser testing, run all three browsers simultaneously:

### Start all browsers

```bash
# Terminal 1 — Chrome
chromedriver --port=9515

# Terminal 2 — Firefox
firefox --headless --remote-debugging-port=9223 --no-remote

# Terminal 3 — Edge
msedgedriver --port=9516
```

### Connect to all in tests

```python
import pytest
from bidiwave import BiDiClient

ENDPOINTS = {
    "chrome": "ws://localhost:9515/session",
    "firefox": "ws://localhost:9223/session",
    "edge": "ws://localhost:9516/session",
}

@pytest.fixture(params=list(ENDPOINTS.keys()))
async def client(request):
    browser = request.param
    url = ENDPOINTS[browser]
    async with await BiDiClient.connect(url) as client:
        yield client
```

## Docker Compose for Multi-Browser

```yaml
version: "3.8"
services:
  chromedriver:
    image: selenoid/chromedriver:latest
    ports:
      - "9515:9515"
    command: --port=9515

  firefox:
    image: selenium/standalone-firefox:latest
    ports:
      - "9223:4444"
    environment:
      - SE_VNC_NO_PASSWORD=1

  edgedriver:
    image: selenoid/edgedriver:latest
    ports:
      - "9516:9516"
    command: --port=9516
```

## Troubleshooting

### ChromeDriver not found

```bash
# Check if ChromeDriver is in PATH
which chromedriver

# Check version compatibility
chromedriver --version
google-chrome --version
# Versions must match
```

### Firefox BiDi not working

```bash
# Ensure Firefox supports BiDi (Firefox 124+)
firefox --version

# Check remote debugging
curl http://localhost:9223/status
```

### WebSocket connection refused

```bash
# Check if the port is open
lsof -i :9515  # Chrome
lsof -i :9223  # Firefox
lsof -i :9516  # Edge

# Check WebSocket endpoint
curl -s http://localhost:9515/status | jq .
```

### BiDi version mismatch

```bash
# Check BiDi protocol version
python -c "import bidiwave; print(bidiwave.__version__)"
# Ensure your browser/driver supports the same BiDi spec version
```

### Headless mode issues

- Chrome: use `--no-sandbox` in Docker
- Firefox: use `--no-remote` to avoid profile conflicts
- Edge: ensure EdgeDriver version matches Edge browser version

## CI/CD Setup

### GitHub Actions — Chrome

```yaml
- name: Install ChromeDriver
  run: |
    LATEST=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json | jq -r '.channels.Stable.version')
    npx @puppeteer/browsers install chromedriver@${LATEST}
    echo "$(pwd)/chromedriver/$(ls chromedriver)" >> $GITHUB_PATH

- name: Start ChromeDriver
  run: chromedriver --port=9515 &

- name: Run tests
  run: pytest tests/ -v
```

### GitHub Actions — Firefox

```yaml
- name: Install Firefox
  run: |
    sudo apt install firefox
    firefox --headless --remote-debugging-port=9223 --no-remote &

- name: Run tests
  run: pytest tests/ -v
```

### GitHub Actions — Multi-browser

```yaml
strategy:
  matrix:
    browser: [chrome, firefox, edge]
steps:
  - name: Setup ${{ matrix.browser }}
    run: ./scripts/setup-${{ matrix.browser }}.sh
  - name: Run tests
    run: pytest tests/ --browser=${{ matrix.browser }} -v
```

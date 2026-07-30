# CLI Command Reference — Full Catalog

> Complete list of wavexis CLI commands with flags and options.

## Global Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--backend` | Backend to use: `cdp` or `bidi` | `cdp` |
| `--stealth` | Enable stealth mode (anti-bot hiding) | `false` |
| `--headless` | Run browser headless | `true` |
| `--timeout` | Navigation timeout in milliseconds | `30000` |
| `--viewport` | Viewport size `WIDTHxHEIGHT` | Browser default |
| `--device` | Device to emulate (see `wavexis devices`) | — |
| `--user-agent` | Custom user agent string | Browser default |
| `--proxy` | Proxy server URL | — |
| `--ignore-cert` | Ignore certificate errors | `false` |
| `--extra-args` | Extra Chrome/Edge arguments | — |
| `--executable-path` | Custom browser executable path | Auto-detected |
| `--remote-debugging-port` | Remote debugging port | `9222` |
| `--profile` | Browser profile directory | — |
| `--incognito` | Use incognito mode | `false` |
| `--output` / `-o` | Output file path | — |
| `--format` | Output format: `json`, `text`, `yaml` | `json` |
| `--verbose` | Verbose logging | `false` |
| `--quiet` | Suppress non-essential output | `false` |

---

## Capture Commands

### `wavexis screenshot`

```bash
wavexis screenshot <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output file path | `screenshot.png` |
| `--full-page` | Capture full page | `false` |
| `--selector` | Capture specific element | — |
| `--quality` | JPEG quality (0-100) | `80` |
| `--format` | Image format: `png`, `jpeg`, `webp` | `png` |
| `--delay` | Delay before screenshot (ms) | `0` |
| `--wait-for` | CSS selector to wait for | — |
| `--wait-for-visible` | Wait for element to be visible | `false` |
| `--beyond-viewport` | Capture beyond viewport | `false` |
| `--from-surface` | Capture from surface | `true` |
| `--annotate` | Annotate screenshot with bounding boxes | `false` |

### `wavexis pdf`

```bash
wavexis pdf <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output file path | `output.pdf` |
| `--paper` | Paper size: `a4`, `letter`, `legal`, `tabloid` | `a4` |
| `--landscape` | Landscape orientation | `false` |
| `--scale` | Scale factor (0.1-2.0) | `1.0` |
| `--margin-top` | Top margin (e.g., `1cm`) | `1cm` |
| `--margin-bottom` | Bottom margin | `1cm` |
| `--margin-left` | Left margin | `1cm` |
| `--margin-right` | Right margin | `1cm` |
| `--print-background` | Print background graphics | `true` |
| `--header-template` | HTML header template | — |
| `--footer-template` | HTML footer template | — |
| `--page-ranges` | Page ranges (e.g., `1-5`) | — |
| `--prefer-css-page-size` | Use CSS page size | `false` |

### `wavexis scrape`

```bash
wavexis scrape <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--selector` | CSS selector to scrape | `body` |
| `--format` | Output format: `text`, `html`, `markdown` | `text` |
| `--attributes` | Attributes to extract (comma-separated) | — |
| `--wait-for` | CSS selector to wait for | — |
| `--delay` | Delay before scraping (ms) | `0` |
| `--all` | Scrape all matching elements | `false` |
| `-o, --output` | Output file path | stdout |

### `wavexis screencast`

```bash
wavexis screencast <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output directory | `./screencast/` |
| `--duration` | Recording duration (seconds) | `10` |
| `--fps` | Frames per second | `10` |
| `--quality` | JPEG quality (0-100) | `80` |
| `--format` | Output format: `gif`, `webm`, `frames` | `gif` |

---

## Navigation Commands

### `wavexis navigate`

```bash
wavexis navigate <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--wait-until` | Wait condition: `load`, `domcontentloaded`, `networkidle` | `load` |
| `--timeout` | Navigation timeout (ms) | `30000` |

### `wavexis tabs`

```bash
wavexis tabs <url> [subcommand] [options]
```

Subcommands: `new`, `close`, `list`, `switch`, `activate`.

---

## Evaluate Commands

### `wavexis eval`

```bash
wavexis eval <url> -e "<expression>" [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-e, --expression` | JavaScript expression to evaluate | — |
| `--assert` | Assertion: `==`, `!=`, `contains`, `matches` | — |
| `--return-by-value` | Return value instead of reference | `true` |
| `--await-promise` | Await promise resolution | `false` |
| `--timeout` | Evaluation timeout (ms) | `30000` |

---

## Input Commands

### `wavexis click`

```bash
wavexis click <url> --selector "<selector>" [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--selector` | CSS selector | — |
| `--delay` | Delay before click (ms) | `0` |
| `--button` | Button: `left`, `right`, `middle` | `left` |
| `--click-count` | Number of clicks | `1` |

### `wavexis type`

```bash
wavexis type <url> --selector "<selector>" --text "<text>" [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--selector` | CSS selector | — |
| `--text` | Text to type | — |
| `--delay` | Delay between keystrokes (ms) | `0` |
| `--clear` | Clear field before typing | `true` |

### `wavexis fill`

```bash
wavexis fill <url> --selector "<selector>" --text "<text>"
```

Same as `type` but uses `Input.insertText` (instant, no keystroke simulation).

### `wavexis key`

```bash
wavexis key <url> --key "<key>" [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--key` | Key name (e.g., `Enter`, `Tab`, `Escape`) | — |
| `--modifiers` | Modifiers: `Shift`, `Control`, `Alt`, `Meta` | — |

### `wavexis hover`

```bash
wavexis hover <url> --selector "<selector>"
```

### `wavexis drag`

```bash
wavexis drag <url> --from "<selector>" --to "<selector>"
```

### `wavexis tap`

```bash
wavexis tap <url> --selector "<selector>"
```

### `wavexis select`

```bash
wavexis select <url> --selector "<selector>" --value "<value>"
```

---

## Network Commands

### `wavexis headers`

```bash
wavexis headers <url>
```

### `wavexis user-agent`

```bash
wavexis user-agent <url> --ua "<user-agent>"
```

### `wavexis block`

```bash
wavexis block <url> -p "<pattern>" [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-p, --pattern` | URL pattern to block (glob) | — |
| `--wait` | Keep browser open for N seconds | `0` |

### `wavexis throttle`

```bash
wavexis throttle <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--download` | Download throughput (bytes/s) | — |
| `--upload` | Upload throughput (bytes/s) | — |
| `--latency` | Latency (ms) | — |
| `--offline` | Simulate offline | `false` |

### `wavexis intercept`

```bash
wavexis intercept <url> -p "<pattern>" [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-p, --pattern` | URL pattern to intercept | — |
| `--block` | Block matching requests | `false` |
| `--wait` | Keep browser open for N seconds | `0` |

### `wavexis mock`

```bash
wavexis mock <url> -p "<pattern>" -b "<body>" [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-p, --pattern` | URL pattern to mock | — |
| `-b, --body` | Mock response body | — |
| `-s, --status` | Mock response status code | `200` |
| `--headers` | Mock response headers (JSON) | — |
| `--wait` | Keep browser open for N seconds | `0` |

### `wavexis modify`

```bash
wavexis modify <url> -p "<pattern>" [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-p, --pattern` | URL pattern to modify | — |
| `--header` | Header to add/modify (`Key: Value`) | — |
| `--wait` | Keep browser open for N seconds | `0` |

### `wavexis modify-response`

```bash
wavexis modify-response <url> -p "<pattern>" -b "<body>" [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-p, --pattern` | URL pattern to modify | — |
| `-b, --body` | Replacement response body | — |
| `-s, --status` | Replacement status code | `200` |
| `--wait` | Keep browser open for N seconds | `0` |

### `wavexis har`

```bash
wavexis har <url> -o <output.har> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output HAR file | — |
| `--timeout` | Capture duration (ms) | `30000` |

### `wavexis har-replay`

```bash
wavexis har-replay <har-file> --url <target-url>
```

### `wavexis inspect`

```bash
wavexis inspect <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--filter` | Filter requests by URL pattern | — |
| `--method` | Filter by HTTP method | — |
| `--status` | Filter by status code | — |
| `--duration` | Capture duration (seconds) | `10` |

---

## Performance Commands

### `wavexis perf`

```bash
wavexis perf <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-m, --mode` | Mode: `metrics`, `trace`, `profile`, `heap-snapshot`, `coverage`, `css-coverage` | `metrics` |
| `-o, --output` | Output file | stdout |
| `-d, --duration` | Trace/profile duration (ms) | `5000` |

### `wavexis cwv`

```bash
wavexis cwv <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--budget` | Budget JSON (e.g., `{"lcp_ms":2500}`) | — |
| `-o, --output` | Output report file | stdout |

### `wavexis lighthouse`

```bash
wavexis lighthouse <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output report file | stdout |
| `--categories` | Categories: `performance`, `accessibility`, `best-practices`, `seo` | All |
| `--form-factor` | Form factor: `mobile`, `desktop` | `mobile` |

### `wavexis trace`

```bash
wavexis trace <url> <start|stop> [options]
```

---

## Emulation Commands

### `wavexis emulation`

```bash
wavexis emulation <type> <url> [options]
```

Types: `device`, `viewport`, `geolocation`, `timezone`, `dark-mode`, `media`, `vision-deficiency`, `idle-override`, `disable-js`, `visible-size`.

### `wavexis devices`

```bash
wavexis devices
```

Lists all available device presets.

---

## Storage Commands

### `wavexis cookies`

```bash
wavexis cookies <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--set` | Set a cookie | `false` |
| `--delete` | Delete a cookie | `false` |
| `--clear` | Clear all cookies | `false` |
| `--name` | Cookie name | — |
| `--value` | Cookie value | — |
| `--domain` | Cookie domain | — |
| `--path` | Cookie path | `/` |
| `--secure` | Secure flag | `false` |
| `--http-only` | HTTP-only flag | `false` |

### `wavexis storage`

```bash
wavexis storage <get|set|clear|list> <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--type` | Storage type: `local`, `session` | `local` |
| `--key` | Storage key | — |
| `--value` | Storage value | — |

### `wavexis indexeddb`

```bash
wavexis indexeddb <url> [options]
```

---

## Advanced Commands

### `wavexis a11y`

```bash
wavexis a11y <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--node-id` | Root node ID | — |
| `--format` | Output format: `json`, `tree` | `json` |

### `wavexis axe`

```bash
wavexis axe <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output report file | stdout |
| `--tags` | Filter by WCAG tags | — |

### `wavexis shadow`

```bash
wavexis shadow <url> <action> <host-selector> [options]
```

Actions: `click`, `fill`, `eval`, `screenshot`.

### `wavexis nl`

```bash
wavexis nl <url> <action> "<description>" [options]
```

Actions: `click`, `fill`, `find`, `type`, `hover`, `scroll`, `screenshot`.

### `wavexis visual-diff`

```bash
wavexis visual-diff <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--baseline` | Baseline image path | — |
| `-o, --output` | Diff output path | — |
| `--threshold` | Pixel difference threshold | `0.01` |

### `wavexis security`

```bash
wavexis security <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--ignore-cert` | Ignore certificate errors | `false` |

### `wavexis auth`

```bash
wavexis auth <context.json> <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--screenshot` | Take screenshot after auth | `false` |
| `-o, --output` | Screenshot output path | — |

---

## Utility Commands

### `wavexis multi`

```bash
wavexis multi <config.yml> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--watch` | Re-run on file change | `false` |
| `--dry-run` | Show actions without executing | `false` |
| `--parallel` | Execute actions in parallel | `false` |
| `--cache-ttl` | Cache TTL in seconds | `0` (disabled) |

### `wavexis init`

```bash
wavexis init [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-t, --template` | Template name | `screenshot` |
| `-u, --url` | Target URL | — |
| `-s, --selector` | CSS selector | — |
| `--text` | Text for type/fill actions | — |
| `-o, --output` | Output config file | `wavexis.yaml` |
| `--list` | List available templates | `false` |

### `wavexis repl`

```bash
wavexis repl [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--url` | Initial URL | — |

### `wavexis serve`

```bash
wavexis serve [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--host` | Bind address | `127.0.0.1` |
| `--port` | Port | `8080` |
| `--rate-limit` | Requests per minute | `0` (disabled) |
| `--allow-remote` | Allow remote connections | `false` |

### `wavexis batch`

```bash
wavexis batch <urls-file> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--action` | Action to perform | `screenshot` |
| `--output-dir` | Output directory | `./output/` |
| `--parallel` | Parallel workers | `1` |

### `wavexis crawl`

```bash
wavexis crawl <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--depth` | Crawl depth | `2` |
| `-o, --output` | Output file | stdout |
| `--same-origin` | Only crawl same origin | `true` |

### `wavexis record`

```bash
wavexis record <url> [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output YAML file | `session.yml` |
| `--interactive` | Record real interactions | `false` |
| `--duration` | Recording duration (seconds) | `30` |
| `--actions` | Action types to record (comma-separated) | — |

### `wavexis replay`

```bash
wavexis replay <session.yml>
```

### `wavexis raw`

```bash
wavexis raw <url> --method "<Domain.method>" [options]
```

| Flag | Description | Default |
|------|-------------|---------|
| `--method` | CDP/BiDi method (e.g., `Page.printToPDF`) | — |
| `--params` | Method parameters (JSON) | `{}` |

### `wavexis install_check`

```bash
wavexis install_check
```

### `wavexis backends`

```bash
wavexis backends
```

Lists installed backends (cdp, bidi).

### `wavexis completions`

```bash
wavexis completions <shell>
```

Shells: `bash`, `zsh`, `fish`, `powershell`.

### `wavexis plugins`

```bash
wavexis plugins [list|install|uninstall]
```

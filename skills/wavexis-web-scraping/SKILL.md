---
name: WaveXis Web Scraping
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Web scraping with wavexis. Stealth mode for anti-bot sites, crawl command for multi-page scraping, natural language selectors, shadow DOM scraping, batch processing."
tags: [web-scraping, stealth, crawl, data-extraction]
trigger: When the user asks about web scraping with wavexis, needs stealth mode for anti-bot sites, wants to crawl multi-page sites, needs natural language selectors or Shadow DOM scraping, or wants batch processing of multiple URLs.
---

# WaveXis Web Scraping

## Description

Web scraping with wavexis — the CLI tool that wraps cdpwave and bidiwave. Covers stealth mode for anti-bot sites, the `scrape` command with CSS selectors, `crawl` for site-wide crawling, `nl` for natural language selectors, `shadow` for Shadow DOM scraping, `batch` for processing multiple URLs, auth context for scraping behind login, action caching, and rate limiting.

## When to Invoke

- Scraping a single page or multiple pages with wavexis
- Needing stealth mode to bypass anti-bot detection
- Crawling an entire site or section of a site
- Using natural language selectors instead of CSS/XPath
- Scraping Shadow DOM content
- Processing a list of URLs in batch
- Scraping behind authentication (login required)
- Setting up polite crawling with rate limiting

## Prerequisites

- `pip install wavexis[cdp]` or `pip install wavexis[bidi]`
- Chrome or Edge installed (for CDP backend)
- Basic familiarity with wavexis CLI (see `wavexis-cli-automation` skill)

## Stealth Mode

Stealth mode hides automation indicators to avoid detection by anti-bot systems.

### Basic stealth

```bash
wavexis scrape https://example.com --stealth
```

### What stealth mode hides

| Indicator | What it does |
|-----------|-------------|
| `navigator.webdriver` | Removes the `webdriver` property |
| Chrome plugins | Fakes `navigator.plugins` array |
| WebGL vendor | Spoofs WebGL renderer and vendor |
| Chrome runtime | Hides `window.chrome` object |
| Languages | Sets realistic `navigator.languages` |
| Permissions | Overrides `navigator.permissions.query` |
| User agent | Removes `HeadlessChrome` from UA string |
| CDP detection | Patches `Runtime.enable` leak |

### Stealth with custom user agent

```bash
wavexis scrape https://example.com \
    --stealth \
    --user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
```

### Stealth with extra args

```bash
wavexis scrape https://example.com \
    --stealth \
    --extra-args "--disable-blink-features=AutomationControlled,--window-size=1920,1080"
```

### Limitations

- Stealth mode is not a guarantee against all anti-bot systems
- Advanced bot detection (Cloudflare, Datadome, PerimeterX) may still detect automation
- CAPTCHA challenges require manual solving or third-party services
- Stealth patches are browser-specific and may break with browser updates

## Scrape Command

### Basic scrape

```bash
wavexis scrape https://example.com
```

Returns page content as markdown by default.

### Scrape with CSS selector

```bash
wavexis scrape https://example.com --selector "article.content"
```

### Scrape with multiple selectors

```bash
wavexis scrape https://example.com \
    --selector "h1" \
    --selector ".price" \
    --selector ".description"
```

### Output formats

```bash
# Markdown (default)
wavexis scrape https://example.com --format markdown

# HTML
wavexis scrape https://example.com --format html

# Text
wavexis scrape https://example.com --format text

# JSON (structured)
wavexis scrape https://example.com --format json --selector "article"
```

### Scrape with wait

```bash
# Wait for a selector to appear
wavexis scrape https://example.com --wait-for ".dynamic-content" --timeout 10000

# Wait for network idle
wavexis scrape https://example.com --wait-until networkidle
```

### Scrape to file

```bash
wavexis scrape https://example.com --output result.md
```

## Crawl Command

Crawl an entire site or section by following links.

### Basic crawl

```bash
wavexis crawl https://example.com --depth 2
```

### Crawl with URL filter

```bash
# Only crawl URLs matching a pattern
wavexis crawl https://example.com \
    --depth 3 \
    --url-filter "*/products/*"
```

### Crawl with output directory

```bash
wavexis crawl https://example.com \
    --depth 2 \
    --output-dir ./scraped/
```

### Crawl with rate limiting

```bash
wavexis crawl https://example.com \
    --depth 3 \
    --delay 2 \
    --concurrent 1
```

### Crawl options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--depth` | `int` | `1` | Maximum crawl depth |
| `--url-filter` | `str` | None | Only follow URLs matching pattern |
| `--url-exclude` | `str` | None | Skip URLs matching pattern |
| `--output-dir` | `str` | `./scraped/` | Directory for scraped pages |
| `--delay` | `float` | `0` | Delay between requests (seconds) |
| `--concurrent` | `int` | `1` | Concurrent requests |
| `--format` | `str` | `markdown` | Output format per page |
| `--stealth` | `flag` | off | Enable stealth mode |
| `--same-domain` | `flag` | on | Only crawl same domain |

## Natural Language Selectors

Use natural language instead of CSS/XPath to describe what you want to extract.

### Basic NL selector

```bash
wavexis nl https://example.com "the main article title and its publication date"
```

### NL with output format

```bash
wavexis nl https://example.com "all product names and prices" --format json
```

### NL with stealth

```bash
wavexis nl https://example.com "user reviews with ratings" --stealth --format json
```

### How NL selectors work

1. The page is scraped and sent to an LLM
2. The LLM identifies the relevant elements based on the description
3. The extracted content is returned in the requested format
4. Requires `WAVEXIS_LLM_API_KEY` environment variable

### NL configuration

```bash
export WAVEXIS_LLM_API_KEY="your-api-key"
export WAVEXIS_LLM_MODEL="gpt-4o"
wavexis nl https://example.com "product specifications table"
```

## Shadow DOM Scraping

Scrape content inside Shadow DOM roots that standard selectors can't reach.

### Basic shadow scrape

```bash
wavexis shadow https://example.com --selector "my-web-component::shadow(.content)"
```

### Shadow with pierce notation

```bash
wavexis shadow https://example.com --selector ">>> .shadow-content"
```

### Multiple shadow roots

```bash
wavexis shadow https://example.com \
    --selector "my-card::shadow(my-list::shadow(.item))"
```

### Shadow with output

```bash
wavexis shadow https://example.com \
    --selector "my-widget::shadow(.data)" \
    --format json \
    --output shadow-data.json
```

## Batch Processing

Process multiple URLs from a file.

### Basic batch

```bash
wavexis batch urls.txt --format markdown --output-dir ./results/
```

### Batch with stealth

```bash
wavexis batch urls.txt --stealth --delay 1 --output-dir ./results/
```

### Batch with selectors

```bash
wavexis batch urls.txt --selector "article.content" --format json
```

### URL list format

```
# urls.txt — one URL per line, # for comments
https://example.com/page1
https://example.com/page2
https://example.com/page3
# This line is a comment
https://example.com/page4
```

### Batch options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--format` | `str` | `markdown` | Output format |
| `--output-dir` | `str` | `./batch-results/` | Output directory |
| `--delay` | `float` | `0` | Delay between URLs |
| `--concurrent` | `int` | `1` | Concurrent requests |
| `--stealth` | `flag` | off | Enable stealth mode |
| `--selector` | `str` | None | CSS selector to extract |
| `--timeout` | `int` | `30000` | Per-URL timeout (ms) |

## Auth Context

Scrape pages behind authentication by reusing a browser session.

### Login then scrape

```bash
# Step 1: Login and save session
wavexis navigate https://example.com/login
wavexis fill "#username" "myuser"
wavexis fill "#password" "mypass"
wavexis click "#login-button"
wavexis session save --name authenticated

# Step 2: Scrape with saved session
wavexis scrape https://example.com/dashboard --session authenticated
```

### Auth with multi-action YAML

```yaml
# auth-scrape.yml
actions:
  - navigate:
      url: https://example.com/login
      wait_until: networkidle
  - fill:
      selector: "#username"
      text: "myuser"
  - fill:
      selector: "#password"
      text: "mypass"
  - click:
      selector: "#login-button"
  - wait_for:
      selector: ".dashboard"
      visible: true
      timeout: 10000
  - scrape:
      format: markdown
      selector: ".dashboard-content"
```

```bash
wavexis run auth-scrape.yml --output dashboard.md
```

### Cookie-based auth

```bash
# Export cookies from an authenticated session
wavexis cookies export --output cookies.json

# Use cookies for scraping
wavexis scrape https://example.com/private --cookies cookies.json
```

## Action Caching

Avoid re-analyzing pages you've already scraped.

### Cache with TTL

```bash
wavexis scrape https://example.com --cache-ttl 3600
```

### Cache directory

```bash
wavexis scrape https://example.com --cache-dir ./cache/
```

### Clear cache

```bash
wavexis cache clear
```

### Cache behavior

- Cached pages are stored as HTML in the cache directory
- `--cache-ttl` specifies seconds before re-fetch (default: 3600)
- Cache key is based on URL + selector + format
- Stealth mode bypasses cache by default

## Rate Limiting and Polite Crawling

### Delay between requests

```bash
wavexis crawl https://example.com --depth 3 --delay 2
```

### Concurrent request limit

```bash
wavexis crawl https://example.com --depth 3 --concurrent 2 --delay 1
```

### Respect robots.txt

```bash
wavexis crawl https://example.com --depth 3 --respect-robots
```

### Polite crawling best practices

- Use `--delay` of at least 1-2 seconds between requests
- Keep `--concurrent` low (1-2) to avoid overwhelming the server
- Use `--respect-robots` to honor robots.txt
- Set a reasonable `--timeout` (30s default)
- Use `--url-exclude` to skip non-content pages (e.g., `/print/`, `/share/`)
- Limit `--depth` to avoid crawling too deep

## Multi-Action YAML for Scraping

### SPA scraping template

```yaml
actions:
  - navigate:
      url: https://spa.example.com
      wait_until: networkidle
  - wait_for:
      selector: ".app-loaded"
      visible: true
      timeout: 15000
  - scrape:
      format: markdown
      selector: "main"
```

### Infinite scroll scraping

```yaml
actions:
  - navigate:
      url: https://example.com/feed
      wait_until: networkidle
  - repeat:
      times: 5
      actions:
        - scroll:
            delta_y: 1000
        - wait:
            duration: 2000
  - scrape:
      format: json
      selector: ".post"
```

### Paginated scraping

```yaml
actions:
  - navigate:
      url: https://example.com/products?page=1
      wait_until: networkidle
  - scrape:
      format: json
      selector: ".product"
      output: page-1.json
  - click:
      selector: ".next-page"
  - wait_for:
      selector: ".product-list"
      visible: true
  - scrape:
      format: json
      selector: ".product"
      output: page-2.json
```

## Best Practices

- **Use stealth only when needed** — adds overhead; skip for sites without anti-bot.
- **Cache aggressively** — `--cache-ttl` avoids redundant requests during development.
- **Be polite** — use `--delay` and low `--concurrent` to avoid rate limiting.
- **Use specific selectors** — `article.content` is better than scraping the whole page.
- **Wait for content** — use `--wait-for` for dynamic content before scraping.
- **Use YAML for complex flows** — multi-action YAML handles login + scrape in one run.
- **Export to JSON for data** — structured output is easier to process downstream.
- **Test with `--depth 1`** — verify crawl config before running deep crawls.
- **Save sessions for auth** — reuse authenticated sessions across multiple scrapes.
- **Use `--url-filter`** — restrict crawls to relevant sections of the site.

## Common Pitfalls

- **Forgetting `--wait-for`** — dynamic content may not be present when scraping starts.
- **Stealth not enough** — advanced anti-bot may still detect; consider proxy services.
- **Crawling too fast** — servers may rate-limit or block; use `--delay`.
- **Missing `--same-domain`** — crawling may follow external links; enabled by default.
- **Shadow DOM invisible** — standard CSS selectors can't pierce shadow roots; use `shadow` command.
- **NL requires API key** — natural language selectors need `WAVEXIS_LLM_API_KEY`.
- **Cache stale data** — long `--cache-ttl` may serve outdated content for dynamic sites.
- **Auth session expired** — saved sessions may expire; re-login if scraping fails.

## References

- `references/stealth-techniques.md` — What stealth mode does and limitations
- `references/selector-strategies.md` — CSS, XPath, NL, Shadow DOM selectors
- `references/crawl-patterns.md` — Crawling strategies and rate limiting
- `assets/templates/scrape-spa.yml` — SPA scraping template
- `assets/templates/crawl-site.yml` — Site crawl template
- `assets/templates/stealth-scrape.yml` — Stealth scraping template
- `assets/templates/batch-urls.txt` — Batch URL list template
- [wavexis on GitHub](https://github.com/MathiasPaulenko/wavexis)
- [wavexis documentation](https://mathiaspaulenko.github.io/wavexis/)

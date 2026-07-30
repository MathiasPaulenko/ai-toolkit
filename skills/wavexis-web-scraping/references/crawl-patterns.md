# Crawl Patterns — Strategies and Rate Limiting

> Guide to crawling strategies, URL filtering, and polite rate limiting with wavexis.

## Crawl Overview

The `crawl` command follows links from a starting URL to discover and scrape multiple pages.

```bash
wavexis crawl https://example.com --depth 2
```

## Crawl Depth

Depth controls how many link-hops from the start URL to follow.

| Depth | What it crawls |
|-------|---------------|
| 0 | Only the start URL |
| 1 | Start URL + its direct links |
| 2 | Start URL + links + links from those pages |
| 3 | Start URL + 2 levels of links |
| N | N levels deep from start URL |

```bash
# Shallow crawl — just the start page and its direct links
wavexis crawl https://example.com --depth 1

# Deep crawl — 3 levels
wavexis crawl https://example.com --depth 3
```

## URL Filtering

### Include filter

Only crawl URLs matching a pattern:

```bash
wavexis crawl https://example.com \
    --depth 3 \
    --url-filter "*/products/*"
```

### Exclude filter

Skip URLs matching a pattern:

```bash
wavexis crawl https://example.com \
    --depth 3 \
    --url-exclude "*/print/*" \
    --url-exclude "*/share/*"
```

### Multiple filters

```bash
wavexis crawl https://example.com \
    --depth 3 \
    --url-filter "*/blog/*" \
    --url-exclude "*/blog/page/*" \
    --url-exclude "*/blog/tag/*"
```

### Same-domain restriction

By default, crawl only follows links on the same domain:

```bash
# Same domain only (default)
wavexis crawl https://example.com --depth 2 --same-domain

# Allow cross-domain
wavexis crawl https://example.com --depth 2 --no-same-domain
```

## Rate Limiting

### Delay between requests

```bash
# 2-second delay between requests
wavexis crawl https://example.com --depth 3 --delay 2

# 500ms delay
wavexis crawl https://example.com --depth 3 --delay 0.5
```

### Concurrency control

```bash
# Sequential (default)
wavexis crawl https://example.com --depth 3 --concurrent 1

# 2 concurrent requests
wavexis crawl https://example.com --depth 3 --concurrent 2 --delay 1
```

### Respect robots.txt

```bash
wavexis crawl https://example.com --depth 3 --respect-robots
```

## Output Management

### Output directory

```bash
wavexis crawl https://example.com \
    --depth 2 \
    --output-dir ./scraped-site/
```

### Output format

```bash
# Markdown per page
wavexis crawl https://example.com --depth 2 --format markdown

# JSON per page
wavexis crawl https://example.com --depth 2 --format json

# HTML per page
wavexis crawl https://example.com --depth 2 --format html
```

### File naming

Crawled pages are saved as files named by their URL path:

```
scraped-site/
  index.md           — https://example.com/
  products.md        — https://example.com/products
  products_1.md      — https://example.com/products?page=1
  about.md           — https://example.com/about
```

## Crawling Strategies

### Section-only crawl

Crawl only a specific section of a site:

```bash
wavexis crawl https://example.com \
    --depth 5 \
    --url-filter "*/docs/*" \
    --url-exclude "*/docs/archive/*" \
    --delay 1
```

### Blog crawl

Crawl all blog posts but skip pagination and tag pages:

```bash
wavexis crawl https://example.com \
    --depth 3 \
    --url-filter "*/blog/*" \
    --url-exclude "*/blog/page/*" \
    --url-exclude "*/blog/tag/*" \
    --url-exclude "*/blog/category/*" \
    --delay 2 \
    --format markdown
```

### Product catalog crawl

Crawl product pages with stealth:

```bash
wavexis crawl https://example.com \
    --depth 4 \
    --url-filter "*/products/*" \
    --url-exclude "*/products/*review*" \
    --stealth \
    --delay 3 \
    --concurrent 1 \
    --format json \
    --selector "[data-product-id]"
```

### Sitemap-based crawl

Use a sitemap to discover URLs, then scrape each:

```bash
# Extract URLs from sitemap
wavexis scrape https://example.com/sitemap.xml --format text > urls.txt

# Process with batch
wavexis batch urls.txt --format markdown --output-dir ./sitemap-scrape/
```

## Polite Crawling Best Practices

### Do

- **Use delays** — at least 1-2 seconds between requests
- **Keep concurrency low** — 1-2 concurrent requests max
- **Respect robots.txt** — use `--respect-robots`
- **Limit depth** — avoid crawling too deep (3-5 is usually enough)
- **Filter URLs** — use `--url-filter` and `--url-exclude` to stay focused
- **Set timeouts** — don't let slow pages hang the crawl
- **Cache results** — use `--cache-ttl` during development to avoid re-crawling
- **Identify yourself** — set a custom user agent with contact info

### Don't

- **Don't crawl too fast** — high request rates can trigger rate limiting or bans
- **Don't crawl too deep** — depth > 5 is rarely useful and wastes resources
- **Don't ignore errors** — check the crawl log for failed pages
- **Don't scrape copyrighted content** — respect terms of service and copyright
- **Don't overload small sites** — use longer delays for small or personal sites

## Custom User Agent for Crawling

```bash
wavexis crawl https://example.com \
    --depth 3 \
    --user-agent "MyBot/1.0 (contact: admin@example.com)" \
    --delay 2
```

## Crawl with Stealth

```bash
wavexis crawl https://example.com \
    --depth 3 \
    --stealth \
    --delay 3 \
    --concurrent 1
```

## Monitoring Crawl Progress

### Verbose output

```bash
wavexis crawl https://example.com --depth 3 --verbose
```

### Log to file

```bash
wavexis crawl https://example.com --depth 3 --log crawl.log
```

## Common Crawl Patterns

### Pattern: Scrape all product pages

```bash
wavexis crawl https://shop.example.com \
    --depth 4 \
    --url-filter "*/product/*" \
    --format json \
    --selector "[data-product-json]" \
    --output-dir ./products/ \
    --delay 2
```

### Pattern: Scrape documentation

```bash
wavexis crawl https://docs.example.com \
    --depth 5 \
    --url-filter "*/docs/*" \
    --format markdown \
    --output-dir ./docs/ \
    --delay 1
```

### Pattern: Scrape news articles

```bash
wavexis crawl https://news.example.com \
    --depth 2 \
    --url-filter "*/article/*" \
    --format markdown \
    --selector "article" \
    --output-dir ./articles/ \
    --delay 2 \
    --stealth
```

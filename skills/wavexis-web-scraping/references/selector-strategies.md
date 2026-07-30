# Selector Strategies — CSS, XPath, NL, Shadow DOM

> Complete guide to selector strategies for web scraping with wavexis.

## CSS Selectors

The most common and performant selector type.

### Basic CSS

```bash
wavexis scrape https://example.com --selector "article"
wavexis scrape https://example.com --selector ".content"
wavexis scrape https://example.com --selector "#main-content"
```

### Combinators

```bash
# Descendant
wavexis scrape https://example.com --selector "div.article p"

# Child
wavexis scrape https://example.com --selector "ul > li"

# Adjacent sibling
wavexis scrape https://example.com --selector "h2 + p"

# General sibling
wavexis scrape https://example.com --selector "h2 ~ p"
```

### Attribute selectors

```bash
# Has attribute
wavexis scrape https://example.com --selector "[data-id]"

# Exact match
wavexis scrape https://example.com --selector "[role='button']"

# Contains
wavexis scrape https://example.com --selector "[href*='example']"

# Starts with
wavexis scrape https://example.com --selector "[href^='https']"

# Ends with
wavexis scrape https://example.com --selector "[href$='.pdf']"
```

### Pseudo-classes

```bash
# First child
wavexis scrape https://example.com --selector "li:first-child"

# Nth child
wavexis scrape https://example.com --selector "tr:nth-child(odd)"

# Not
wavexis scrape https://example.com --selector "a:not(.external)"

# Contains text (via JS eval)
wavexis eval https://example.com "Array.from(document.querySelectorAll('a')).filter(a => a.textContent.includes('Download'))"
```

### Multiple selectors

```bash
wavexis scrape https://example.com \
    --selector "h1" \
    --selector ".price" \
    --selector ".description"
```

## XPath Selectors

Use XPath for more complex traversal patterns.

### Basic XPath

```bash
wavexis scrape https://example.com --selector "//article" --selector-type xpath
wavexis scrape https://example.com --selector "//div[@class='content']" --selector-type xpath
```

### XPath axes

```bash
# Ancestor
wavexis scrape https://example.com --selector "//h1/ancestor::section" --selector-type xpath

# Following sibling
wavexis scrape https://example.com --selector "//h2/following-sibling::p" --selector-type xpath

# Contains text
wavexis scrape https://example.com --selector "//a[contains(text(), 'Download')]" --selector-type xpath
```

### XPath with conditions

```bash
# Element with specific attribute value
wavexis scrape https://example.com \
    --selector "//input[@type='email']" \
    --selector-type xpath

# Last element
wavexis scrape https://example.com \
    --selector "//ul/li[last()]" \
    --selector-type xpath

# Position-based
wavexis scrape https://example.com \
    --selector "//table/tr[position() > 1]" \
    --selector-type xpath
```

## Natural Language Selectors

Describe what you want in natural language and let the LLM find it.

### Basic NL

```bash
wavexis nl https://example.com "the main article title"
wavexis nl https://example.com "all product names and their prices"
wavexis nl https://example.com "user reviews with star ratings"
```

### NL with format

```bash
wavexis nl https://example.com "product specifications" --format json
wavexis nl https://example.com "table of contents" --format markdown
```

### NL with stealth

```bash
wavexis nl https://example.com "pricing tiers" --stealth --format json
```

### NL configuration

```bash
export WAVEXIS_LLM_API_KEY="your-key"
export WAVEXIS_LLM_MODEL="gpt-4o"
wavexis nl https://example.com "extract all FAQ questions and answers"
```

### When to use NL selectors

| Scenario | NL vs CSS |
|----------|-----------|
| Known structure, stable selectors | CSS is faster and more reliable |
| Unknown or changing structure | NL adapts to layout changes |
| Complex extraction (tables, nested data) | NL understands context |
| Quick prototyping | NL is faster to describe |
| Production scraping | CSS is more deterministic |
| Multi-language sites | NL can understand semantics |

## Shadow DOM Selectors

Standard CSS selectors cannot pierce Shadow DOM boundaries. Use the `shadow` command.

### Basic shadow

```bash
wavexis shadow https://example.com --selector "my-component::shadow(.content)"
```

### Pierce notation

```bash
# Pierce all shadow roots
wavexis shadow https://example.com --selector ">>> .target-element"

# Pierce specific component
wavexis shadow https://example.com --selector "my-card >>> .card-title"
```

### Nested shadow roots

```bash
wavexis shadow https://example.com \
    --selector "my-app::shadow(my-header::shadow(.nav-item))"
```

### Shadow with format

```bash
wavexis shadow https://example.com \
    --selector "my-widget::shadow(.data-grid)" \
    --format json \
    --output widget-data.json
```

### Detecting Shadow DOM

```bash
# Check if an element has a shadow root
wavexis eval https://example.com \
    "document.querySelector('my-component')?.shadowRoot ? 'has shadow' : 'no shadow'"
```

## Selector Comparison

| Type | Performance | Reliability | Setup | Use Case |
|------|-------------|------------|-------|----------|
| CSS | Fast | High | Easy | Known structure, production scraping |
| XPath | Medium | High | Medium | Complex traversal, XML-like structure |
| NL | Slow (LLM) | Medium | Easy | Unknown structure, prototyping |
| Shadow DOM | Fast | High | Medium | Web components, Shadow DOM content |

## Tips for Resilient Selectors

### Prefer semantic selectors

```bash
# Bad — breaks if class changes
wavexis scrape https://example.com --selector ".css-1a2b3c"

# Good — semantic and stable
wavexis scrape https://example.com --selector "article"
wavexis scrape https://example.com --selector "[data-testid='product-card']"
wavexis scrape https://example.com --selector "main h1"
```

### Use data attributes

```bash
wavexis scrape https://example.com --selector "[data-product-id]"
wavexis scrape https://example.com --selector "[data-role='price']"
```

### Combine selectors for specificity

```bash
wavexis scrape https://example.com --selector "article.product h2.title"
wavexis scrape https://example.com --selector "div[data-id='main'] > .content"
```

### Fallback strategy

```bash
# Try primary selector, fall back to alternative
wavexis scrape https://example.com \
    --selector "[data-testid='title']" \
    --fallback-selector "h1.article-title" \
    --fallback-selector "article h1"
```

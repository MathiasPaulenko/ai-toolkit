# Stealth Techniques — What Stealth Mode Does and Limitations

> Detailed reference of wavexis stealth mode: what it hides, how it works, and its limitations.

## Overview

Stealth mode in wavexis patches the browser to hide common automation indicators that anti-bot systems check. It is enabled with the `--stealth` flag.

```bash
wavexis scrape https://example.com --stealth
```

## What Stealth Mode Hides

### navigator.webdriver

The most common automation indicator. Browsers set `navigator.webdriver = true` when controlled by automation.

**Without stealth:**
```javascript
navigator.webdriver  // true
```

**With stealth:**
```javascript
navigator.webdriver  // false (undefined)
```

### navigator.plugins

Headless browsers report an empty plugins array. Stealth fakes a realistic plugins list.

**Without stealth:**
```javascript
navigator.plugins.length  // 0
```

**With stealth:**
```javascript
navigator.plugins.length  // 3 (PDF Viewer, Chrome PDF Viewer, Chromium PDF Viewer)
```

### navigator.languages

Headless browsers may report a default language. Stealth sets realistic language preferences.

**Without stealth:**
```javascript
navigator.languages  // ["en-US"]
```

**With stealth:**
```javascript
navigator.languages  // ["en-US", "en"]
```

### WebGL renderer and vendor

Headless browsers report software WebGL implementations. Stealth spoofs hardware GPU strings.

**Without stealth:**
```javascript
WebGLRenderingContext.getParameter(UNMASKED_VENDOR_WEBGL)  // "Google Inc. (Google)"
WebGLRenderingContext.getParameter(UNMASKED_RENDERER_WEBGL)  // "ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device))"
```

**With stealth:**
```javascript
WebGLRenderingContext.getParameter(UNMASKED_VENDOR_WEBGL)  // "Intel Inc."
WebGLRenderingContext.getParameter(UNMASKED_RENDERER_WEBGL)  // "Intel Iris OpenGL Engine"
```

### window.chrome

Headless Chrome may not have the `window.chrome` object. Stealth restores it.

**Without stealth:**
```javascript
window.chrome  // undefined
```

**With stealth:**
```javascript
window.chrome  // { runtime: {}, ... }
```

### User agent string

Headless Chrome includes "HeadlessChrome" in the user agent string. Stealth removes it.

**Without stealth:**
```
Mozilla/5.0 (X11; Linux x86_64) HeadlessChrome/120.0.0.0 Safari/537.36
```

**With stealth:**
```
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

### Permissions API

The `navigator.permissions.query` behavior differs in headless mode. Stealth patches it to match normal browser behavior.

**Without stealth:**
```javascript
navigator.permissions.query({ name: 'notifications' }).state  // "denied" (in headless)
```

**With stealth:**
```javascript
navigator.permissions.query({ name: 'notifications' }).state  // "prompt" (normal)
```

### CDP detection

Chrome DevTools Protocol leaves traces that can be detected. Stealth patches the `Runtime.enable` leak.

## Stealth Mode Options

### Custom user agent

```bash
wavexis scrape https://example.com \
    --stealth \
    --user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
```

### Extra browser args

```bash
wavexis scrape https://example.com \
    --stealth \
    --extra-args "--disable-blink-features=AutomationControlled,--window-size=1920,1080"
```

### Stealth with non-headless mode

```bash
wavexis scrape https://example.com --stealth --no-headless
```

Running non-headless with stealth is the most realistic but requires a display.

## Detection Levels

| Level | What it detects | Stealth bypasses? |
|-------|----------------|-------------------|
| Basic | `navigator.webdriver`, UA string | Yes |
| Intermediate | Plugins, languages, WebGL, chrome object | Yes |
| Advanced | CDP traces, canvas fingerprinting, timing | Partial |
| Enterprise (Cloudflare, Datadome, PerimeterX) | TLS fingerprint, mouse behavior, IP reputation | No |

## Limitations

### Not a silver bullet

Stealth mode patches JavaScript-level indicators but cannot hide:

- **TLS fingerprint** — browser TLS handshake differs from real browsers
- **IP reputation** — datacenter IPs are flagged by anti-bot services
- **Mouse behavior** — automated mouse movements lack human-like patterns
- **Canvas fingerprinting** — headless rendering produces different canvas hashes
- **Timing analysis** — automated actions are too fast or too regular

### Browser updates

Stealth patches may break with browser updates. Always test after updating Chrome/Edge.

### Anti-bot services

Advanced anti-bot services that stealth mode may not bypass:

| Service | Difficulty | Notes |
|---------|-----------|-------|
| Cloudflare Bot Management | Hard | TLS fingerprint + JS challenge |
| Datadome | Hard | ML-based detection |
| PerimeterX (HUMAN) | Hard | Behavioral analysis |
| Akamai Bot Manager | Hard | Sensor data collection |
| reCAPTCHA | N/A | Requires CAPTCHA solving |
| hCaptcha | N/A | Requires CAPTCHA solving |

### Recommendations for advanced anti-bot

- Use residential proxies with `--proxy` flag
- Run non-headless (`--no-headless`) for more realistic fingerprinting
- Add human-like delays between actions
- Consider third-party CAPTCHA solving services
- Use `--extra-args` for additional browser flags
- Rotate user agents across requests

## Testing Stealth Effectiveness

### Check with bot detection sites

```bash
# Sannysoft bot detection
wavexis screenshot https://bot.sannysoft.com/ --stealth --output bot-test.png

# Pixelscan
wavexis screenshot https://pixelscan.net/ --stealth --output pixelscan.png

# CreepJS
wavexis screenshot https://abrahamjuliot.github.io/creepjs/ --stealth --output creepjs.png
```

### Verify with JavaScript

```bash
wavexis eval https://example.com --stealth \
    "JSON.stringify({
        webdriver: navigator.webdriver,
        plugins: navigator.plugins.length,
        languages: navigator.languages,
        chrome: !!window.chrome,
        ua: navigator.userAgent
    })"
```

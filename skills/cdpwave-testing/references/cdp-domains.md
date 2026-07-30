# CDP Domains Reference — All 60 Domains

> Complete reference of all 60 Chrome DevTools Protocol domains implemented in cdpwave with 689 typed methods.

## How Domains Work in cdpwave

Each `Session` exposes CDP domains as properties:

```python
session.runtime    # Runtime
session.page       # Page
session.network    # Network
session.dom        # DOM
session.emulation  # Emulation
session.target     # Target
```

For domains without a typed property, use the escape hatch:

```python
result = await session.send("DomainName.methodName", {"param": "value"})
```

## Domain Catalog

### Core Domains

| Domain | Property | Methods | Description |
|--------|----------|---------|-------------|
| `Runtime` | `session.runtime` | 30 | JavaScript execution, remote objects, exceptions |
| `Page` | `session.page` | 35 | Navigation, screenshots, PDF, frames |
| `Network` | `session.network` | 42 | Requests, responses, headers, cookies, throttling |
| `DOM` | `session.dom` | 38 | DOM tree, queries, attributes, modifications |
| `CSS` | `session.css` | 20 | CSS rules, stylesheets, computed styles |
| `Emulation` | `session.emulation` | 18 | Device, viewport, geolocation, timezone, network |
| `Target` | `session.target` | 12 | Tabs, workers, targets, sessions |
| `Overlay` | `session.overlay` | 10 | Highlights, inspect mode, screenshots |
| `Security` | `session.security` | 6 | Certificate errors, security state |

### Debugging Domains

| Domain | Property | Methods | Description |
|--------|----------|---------|-------------|
| `Debugger` | `session.debugger` | 28 | Breakpoints, stepping, scopes, callstack |
| `Console` | — | 4 | Console messages (deprecated, use Runtime) |
| `Profiler` | `session.profiler` | 16 | CPU profiling, samples |
| `HeapProfiler` | `session.heap_profiler` | 12 | Heap snapshots, allocation tracking |
| `Performance` | `session.performance` | 4 | Metrics, timeline |

### Input Domains

| Domain | Property | Methods | Description |
|--------|----------|---------|-------------|
| `Input` | `session.input` | 8 | Mouse, keyboard, touch, IME |
| `Input.dispatchKeyEvent` | — | — | Key events |
| `Input.dispatchMouseEvent` | — | — | Mouse events |
| `Input.dispatchTouchEvent` | — | — | Touch events |
| `Input.insertText` | — | — | Text input |

### Storage Domains

| Domain | Property | Methods | Description |
|--------|----------|---------|-------------|
| `Storage` | `session.storage` | 16 | Cookies, local/session storage, IndexedDB |
| `CacheStorage` | `session.cache_storage` | 10 | HTTP cache, Cache API |
| `IndexedDB` | `session.indexed_db` | 12 | IndexedDB databases, object stores |

### Media Domains

| Domain | Property | Methods | Description |
|--------|----------|---------|-------------|
| `Media` | — | 4 | HTML media elements |
| `WebAudio` | — | 8 | Web Audio API |
| `WebAuthn` | — | 6 | Virtual authenticators |
| `MediaAnalytics` | — | 2 | Media analytics state |

### Service Worker Domains

| Domain | Property | Methods | Description |
|--------|----------|---------|-------------|
| `ServiceWorker` | — | 8 | Service worker registration, control |
| `BackgroundService` | — | 4 | Background services events |
| `Fetch` | `session.fetch` | 14 | Request interception, modification |
| `WebAuthn` | — | 6 | Web Authentication API |

### Device Domains

| Domain | Property | Methods | Description |
|--------|----------|---------|-------------|
| `DeviceOrientation` | — | 2 | Device orientation sensors |
| `Sensor` | — | 6 | Generic sensor API |
| `Geolocation` | — | 2 | Geolocation override |
| `DeviceAccess` | — | 4 | Device access requests |

### Browser Domains

| Domain | Property | Methods | Description |
|--------|----------|---------|-------------|
| `Browser` | — | 10 | Browser-level commands, permissions |
| `Tracing` | — | 8 | Performance tracing, data collection |
| `Tethering` | — | 2 | Port forwarding |
| `SystemInfo` | — | 4 | CPU, GPU, process info |

### Accessibility & Animation

| Domain | Property | Methods | Description |
|--------|----------|---------|-------------|
| `Accessibility` | `session.accessibility` | 8 | Accessibility tree, node properties |
| `Animation` | — | 10 | Animations, playback rate, screenshots |
| `DOMDebugger` | `session.dom_debugger` | 10 | DOM breakpoints, event listeners |

### Application Domains

| Domain | Property | Methods | Description |
|--------|----------|---------|-------------|
| `ApplicationCache` | — | 4 | Application cache status |
| `DOMStorage` | — | 6 | DOM storage (localStorage, sessionStorage) |
| `Database` | — | 4 | WebSQL databases (deprecated) |
| `FileSystem` | — | 6 | File system API |

### Audits & Extensions

| Domain | Property | Methods | Description |
|--------|----------|---------|-------------|
| `Audits` | — | 4 | Lighthouse-style audits |
| `Extensions` | — | 4 | Browser extensions |
| `Cast` | — | 4 | Cast targets |
| `PWA` | — | 4 | Progressive Web App installation |

### Logging & Schema

| Domain | Property | Methods | Description |
|--------|----------|---------|-------------|
| `Log` | `session.log` | 6 | Log entries, violation tracking |
| `Schema` | — | 2 | Type definitions |
| `IO` | — | 4 | Stream operations |

## Common Method Examples

### Runtime.evaluate

```python
result = await session.runtime.evaluate(
    expression="document.title",
    return_by_value=True,
    await_promise=False,
    user_gesture=False,
)
# Returns: {"result": {"type": "string", "value": "Example Domain"}}
```

### Page.captureScreenshot

```python
screenshot = await session.page.capture_screenshot(
    format="png",       # "png" | "jpeg"
    quality=80,         # For jpeg only
    clip=None,          # {x, y, width, height, scale} for region
    from_surface=True,
    capture_beyond_viewport=False,
)
# Returns: {"data": "base64-encoded-image-data"}
```

### Page.printToPDF

```python
pdf = await session.page.print_to_pdf(
    paper_width=8.5,
    paper_height=11,
    landscape=False,
    scale=1.0,
    margin_top=0.4,
    margin_bottom=0.4,
    margin_left=0.4,
    margin_right=0.4,
    print_background=True,
)
# Returns: {"data": "base64-encoded-pdf-data"}
```

### Network.setExtraHTTPHeaders

```python
await session.network.set_extra_http_headers({
    "Authorization": "Bearer token123",
    "X-Custom-Header": "value",
})
```

### DOM.querySelector

```python
doc = await session.dom.get_document(depth=1)
node = await session.dom.query_selector(
    node_id=doc["root"]["nodeId"],
    selector="#my-element",
)
```

### Emulation.setDeviceMetricsOverride

```python
await session.emulation.set_device_metrics_override(
    width=375,
    height=667,
    device_scale_factor=2,
    mobile=True,
)
```

## Domain Enable/Disable

Most domains must be enabled before they emit events:

```python
await session.network.enable()
await session.page.enable()
await session.runtime.enable()
await session.dom.enable()

# ... use domain ...

await session.network.disable()
```

| Domain | Enable Method | Required For |
|--------|--------------|--------------|
| `Page` | `page.enable()` | Navigation events |
| `Network` | `network.enable()` | Request/response events |
| `Runtime` | `runtime.enable()` | Console, exceptions |
| `DOM` | `dom.enable()` | DOM tree access |
| `Debugger` | `debugger.enable()` | Breakpoints, stepping |
| `Profiler` | `profiler.enable()` | CPU profiling |
| `Log` | `log.enable()` | Log entries |
| `Overlay` | `overlay.enable()` | Highlights |
| `Performance` | `performance.enable()` | Metrics |
| `Security` | `security.enable()` | Security state |

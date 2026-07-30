# Tool Catalog — Complete 220-Tool Reference

> Full catalog of all wavexis-mcp tools organized by tier, with parameters and return types.

## Core Tier (72 tools — always enabled)

### Session Management

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_session_open` | `headless?: bool`, `backend?: str` | `session_id: str` | Open a new browser session |
| `wavexis_session_close` | `session_id: str` | `ok: bool` | Close a session |
| `wavexis_session_list` | — | `sessions: list` | List active sessions |
| `wavexis_session_info` | `session_id: str` | `info: dict` | Get session details |

### Tab Management

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_tabs_new` | `session_id: str`, `url?: str` | `tab_id: str` | Open a new tab |
| `wavexis_tabs_close` | `session_id: str`, `tab_id: str` | `ok: bool` | Close a tab |
| `wavexis_tabs_list` | `session_id: str` | `tabs: list` | List tabs in session |
| `wavexis_tabs_switch` | `session_id: str`, `tab_id: str` | `ok: bool` | Switch to a tab |

### Navigation

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_navigate` | `session_id: str`, `url: str`, `wait_until?: str` | `ok: bool` | Navigate to URL |
| `wavexis_navigate_back` | `session_id: str` | `ok: bool` | Go back |
| `wavexis_navigate_forward` | `session_id: str` | `ok: bool` | Go forward |
| `wavexis_navigate_reload` | `session_id: str` | `ok: bool` | Reload page |
| `wavexis_navigate_stop` | `session_id: str` | `ok: bool` | Stop loading |

### Capture

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_screenshot` | `session_id: str`, `full_page?: bool`, `selector?: str`, `format?: str`, `quality?: int` | `image: base64` | Take a screenshot |
| `wavexis_pdf` | `session_id: str`, `paper?: str`, `landscape?: bool`, `scale?: float` | `pdf: base64` | Generate a PDF |
| `wavexis_scrape` | `session_id: str`, `selector?: str`, `format?: str` | `content: str` | Scrape page content |
| `wavexis_dom` | `session_id: str`, `selector?: str`, `depth?: int` | `dom: str` | Get DOM tree |

### Evaluate

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_eval` | `session_id: str`, `expression: str`, `return_by_value?: bool` | `result: any` | Evaluate JavaScript |
| `wavexis_call_function` | `session_id: str`, `function: str`, `args?: list` | `result: any` | Call a JS function |

### Input

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_click` | `session_id: str`, `selector: str`, `delay?: int` | `ok: bool` | Click an element |
| `wavexis_type` | `session_id: str`, `selector: str`, `text: str`, `delay?: int` | `ok: bool` | Type text |
| `wavexis_fill` | `session_id: str`, `selector: str`, `text: str` | `ok: bool` | Fill a field |
| `wavexis_press_key` | `session_id: str`, `key: str`, `modifiers?: list` | `ok: bool` | Press a key |
| `wavexis_hover` | `session_id: str`, `selector: str` | `ok: bool` | Hover over element |
| `wavexis_select_option` | `session_id: str`, `selector: str`, `value: str` | `ok: bool` | Select dropdown option |
| `wavexis_scroll` | `session_id: str`, `x?: int`, `y?: int` | `ok: bool` | Scroll the page |
| `wavexis_scroll_to` | `session_id: str`, `selector: str` | `ok: bool` | Scroll to element |

### Cookies

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_cookies_get` | `session_id: str`, `urls?: list` | `cookies: list` | Get cookies |
| `wavexis_cookies_set` | `session_id: str`, `name: str`, `value: str`, `domain: str`, `path?: str` | `ok: bool` | Set a cookie |
| `wavexis_cookies_delete` | `session_id: str`, `name: str` | `ok: bool` | Delete a cookie |
| `wavexis_cookies_clear` | `session_id: str` | `ok: bool` | Clear all cookies |

### Natural Language

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_act` | `session_id: str`, `action: str`, `description: str`, `text?: str` | `result: dict` | NL browser interaction |
| `wavexis_find` | `session_id: str`, `description: str` | `element: dict` | Find element by NL |

### Shadow DOM

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_shadow_click` | `session_id: str`, `host: str`, `selector: str` | `ok: bool` | Click in shadow DOM |
| `wavexis_shadow_fill` | `session_id: str`, `host: str`, `selector: str`, `text: str` | `ok: bool` | Fill in shadow DOM |
| `wavexis_shadow_eval` | `session_id: str`, `host: str`, `expression: str` | `result: any` | Eval in shadow DOM |

### Iframe

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_iframe_eval` | `session_id: str`, `frame: str`, `expression: str` | `result: any` | Eval in iframe |
| `wavexis_iframe_click` | `session_id: str`, `frame: str`, `selector: str` | `ok: bool` | Click in iframe |

### Events

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_events_listen` | `session_id: str`, `types: list` | `events: list` | Listen for events |
| `wavexis_events_wait` | `session_id: str`, `type: str`, `timeout?: int` | `event: dict` | Wait for an event |

### Console

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_console_get` | `session_id: str` | `logs: list` | Get console logs |
| `wavexis_console_clear` | `session_id: str` | `ok: bool` | Clear console |

### Browser Info

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_url` | `session_id: str` | `url: str` | Get current URL |
| `wavexis_title` | `session_id: str` | `title: str` | Get page title |
| `wavexis_user_agent` | `session_id: str`, `ua?: str` | `ua: str` | Get/set user agent |
| `wavexis_headers` | `session_id: str` | `headers: dict` | Get response headers |

### Wait

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_wait_for` | `session_id: str`, `selector: str`, `visible?: bool`, `timeout?: int` | `ok: bool` | Wait for element |
| `wavexis_wait` | `session_id: str`, `duration: int` | `ok: bool` | Wait for duration |

### Download & Dialog

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_download` | `session_id: str`, `selector: str` | `path: str` | Download a file |
| `wavexis_dialog` | `session_id: str`, `action: str`, `text?: str` | `ok: bool` | Handle a dialog |

### Permissions

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_permissions` | `session_id: str`, `name: str`, `state: str` | `ok: bool` | Set permissions |

### Security

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_security` | `session_id: str` | `state: dict` | Get security state |

### Misc

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_backends` | — | `backends: list` | List available backends |
| `wavexis_devices` | — | `devices: list` | List device presets |
| `wavexis_install_check` | — | `status: dict` | Check installation |

---

## Network Tier (20 tools)

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_headers_set` | `session_id`, `headers: dict` | `ok: bool` | Set request headers |
| `wavexis_headers_get` | `session_id` | `headers: dict` | Get response headers |
| `wavexis_user_agent_set` | `session_id`, `ua: str` | `ok: bool` | Set custom UA |
| `wavexis_block` | `session_id`, `pattern: str` | `ok: bool` | Block requests |
| `wavexis_throttle` | `session_id`, `download?: int`, `upload?: int`, `latency?: int` | `ok: bool` | Throttle network |
| `wavexis_cache_clear` | `session_id` | `ok: bool` | Clear cache |
| `wavexis_har` | `session_id`, `timeout?: int` | `har: dict` | Capture HAR |
| `wavexis_intercept` | `session_id`, `pattern: str`, `block?: bool` | `ok: bool` | Intercept requests |
| `wavexis_mock` | `session_id`, `pattern: str`, `body: str`, `status?: int` | `ok: bool` | Mock response |
| `wavexis_modify_request` | `session_id`, `pattern: str`, `headers?: dict` | `ok: bool` | Modify request |
| `wavexis_modify_response` | `session_id`, `pattern: str`, `body: str`, `status?: int` | `ok: bool` | Modify response |
| `wavexis_request_body` | `session_id`, `request_id: str` | `body: str` | Get response body |
| `wavexis_har_replay` | `session_id`, `har: str`, `url: str` | `ok: bool` | Replay HAR |
| `wavexis_request_list` | `session_id` | `requests: list` | List requests |
| `wavexis_websocket_intercept` | `session_id`, `url: str` | `ok: bool` | Intercept WebSocket |
| `wavexis_websocket_send` | `session_id`, `url: str`, `data: str` | `ok: bool` | Send WS message |
| `wavexis_network_conditions` | `session_id`, `offline?: bool`, `download?: int`, `upload?: int`, `latency?: int` | `ok: bool` | Set network conditions |
| `wavexis_extra_headers` | `session_id`, `headers: dict` | `ok: bool` | Set extra headers |
| `wavexis_auth_challenge` | `session_id`, `username: str`, `password: str` | `ok: bool` | Handle auth challenge |
| `wavexis_request_log` | `session_id`, `filter?: str` | `log: list` | Get request log |

---

## Storage Tier (18 tools)

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_storage_get` | `session_id`, `type: str`, `key: str` | `value: str` | Get storage item |
| `wavexis_storage_set` | `session_id`, `type: str`, `key: str`, `value: str` | `ok: bool` | Set storage item |
| `wavexis_storage_delete` | `session_id`, `type: str`, `key: str` | `ok: bool` | Delete storage item |
| `wavexis_storage_clear` | `session_id`, `type: str` | `ok: bool` | Clear storage |
| `wavexis_storage_list` | `session_id`, `type: str` | `items: dict` | List storage items |
| `wavexis_cache_storage_keys` | `session_id` | `keys: list` | List cache storage keys |
| `wavexis_cache_storage_open` | `session_id`, `cache_name: str` | `cache: dict` | Open a cache |
| `wavexis_cache_storage_delete` | `session_id`, `cache_name: str` | `ok: bool` | Delete a cache |
| `wavexis_cache_storage_match` | `session_id`, `cache_name: str`, `request: str` | `response: dict` | Match in cache |
| `wavexis_indexeddb_list` | `session_id` | `databases: list` | List IndexedDB databases |
| `wavexis_indexeddb_get` | `session_id`, `db: str`, `store: str`, `key: str` | `value: any` | Get IndexedDB item |
| `wavexis_indexeddb_put` | `session_id`, `db: str`, `store: str`, `key: str`, `value: any` | `ok: bool` | Put IndexedDB item |
| `wavexis_indexeddb_delete` | `session_id`, `db: str`, `store: str`, `key: str` | `ok: bool` | Delete IndexedDB item |
| `wavexis_indexeddb_clear` | `session_id`, `db: str`, `store: str` | `ok: bool` | Clear IndexedDB store |
| `wavexis_state_save` | `session_id` | `state: dict` | Save browser state |
| `wavexis_state_restore` | `session_id`, `state: dict` | `ok: bool` | Restore browser state |
| `wavexis_state_clear` | `session_id` | `ok: bool` | Clear browser state |
| `wavexis_service_worker_list` | `session_id` | `workers: list` | List service workers |

---

## Emulation Tier (9 tools)

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_emulate_device` | `session_id`, `device: str` | `ok: bool` | Emulate a device |
| `wavexis_emulate_viewport` | `session_id`, `width: int`, `height: int` | `ok: bool` | Set viewport |
| `wavexis_emulate_geolocation` | `session_id`, `lat: float`, `lon: float` | `ok: bool` | Set geolocation |
| `wavexis_emulate_timezone` | `session_id`, `timezone: str` | `ok: bool` | Set timezone |
| `wavexis_emulate_dark_mode` | `session_id`, `enabled: bool` | `ok: bool` | Toggle dark mode |
| `wavexis_emulate_locale` | `session_id`, `locale: str` | `ok: bool` | Set locale |
| `wavexis_emulate_cpu` | `session_id`, `cores: int` | `ok: bool` | Set CPU cores |
| `wavexis_emulate_touch` | `session_id`, `enabled: bool` | `ok: bool` | Toggle touch |
| `wavexis_emulate_sensors` | `session_id`, `sensors: dict` | `ok: bool` | Set sensor values |

---

## A11y Tier (4 tools)

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_a11y_tree` | `session_id`, `node_id?: str` | `tree: dict` | Get accessibility tree |
| `wavexis_a11y_node` | `session_id`, `node_id: str` | `node: dict` | Get a11y node details |
| `wavexis_a11y_traverse` | `session_id`, `node_id: str`, `direction: str` | `node: dict` | Traverse a11y tree |
| `wavexis_axe_audit` | `session_id`, `tags?: list` | `report: dict` | Run axe-core audit |

---

## Interactions Tier (5 tools)

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_dialog_handle` | `session_id`, `action: str`, `text?: str` | `ok: bool` | Handle dialog |
| `wavexis_download_wait` | `session_id`, `timeout?: int` | `path: str` | Wait for download |
| `wavexis_permissions_set` | `session_id`, `name: str`, `state: str` | `ok: bool` | Set permissions |
| `wavexis_permissions_clear` | `session_id`, `name: str` | `ok: bool` | Clear permissions |
| `wavexis_file_chooser` | `session_id`, `files: list` | `ok: bool` | Handle file chooser |

---

## DevTools Tier (31 tools)

### Performance

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_perf_metrics` | `session_id` | `metrics: dict` | Get performance metrics |
| `wavexis_perf_trace` | `session_id`, `action: str`, `duration?: int` | `trace: str` | CPU trace |
| `wavexis_perf_profile` | `session_id`, `action: str`, `duration?: int` | `profile: str` | CPU profile |
| `wavexis_perf_coverage` | `session_id` | `coverage: dict` | JS code coverage |
| `wavexis_perf_css_coverage` | `session_id` | `coverage: dict` | CSS coverage |
| `wavexis_perf_heap_snapshot` | `session_id` | `snapshot: str` | Heap snapshot |

### CSS

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_css_get_styles` | `session_id`, `selector: str` | `styles: str` | Get inline styles |
| `wavexis_css_get_computed` | `session_id`, `selector: str` | `styles: dict` | Get computed styles |
| `wavexis_css_get_rules` | `session_id`, `selector: str` | `rules: list` | Get matching CSS rules |

### Debugging

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_debug_break` | `session_id`, `url: str`, `line: int`, `col?: int` | `breakpoint_id: str` | Set breakpoint |
| `wavexis_debug_step` | `session_id`, `action: str` | `ok: bool` | Step over/into/out |
| `wavexis_debug_pause` | `session_id` | `ok: bool` | Pause execution |
| `wavexis_debug_resume` | `session_id` | `ok: bool` | Resume execution |
| `wavexis_debug_scopes` | `session_id` | `scopes: list` | Get scopes |
| `wavexis_debug_callstack` | `session_id` | `callstack: list` | Get call stack |

### Overlay

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_overlay_highlight` | `session_id`, `selector: str` | `ok: bool` | Highlight element |
| `wavexis_overlay_inspect` | `session_id` | `ok: bool` | Enable inspect mode |
| `wavexis_overlay_screenshot` | `session_id`, `selector?: str` | `image: base64` | Annotated screenshot |
| `wavexis_set_overlay` | `session_id`, `type: str` | `ok: bool` | Set overlay grid |
| `wavexis_clear_overlay` | `session_id` | `ok: bool` | Clear overlays |

### Console

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_console_enable` | `session_id` | `ok: bool` | Enable console capture |
| `wavexis_console_disable` | `session_id` | `ok: bool` | Disable console capture |

### Security

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_security_state` | `session_id` | `state: dict` | Get security state |
| `wavexis_security_cert` | `session_id` | `cert: dict` | Get certificate details |

### Window

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_window_bounds` | `session_id`, `bounds?: dict` | `bounds: dict` | Get/set window bounds |
| `wavexis_window_maximize` | `session_id` | `ok: bool` | Maximize window |
| `wavexis_window_minimize` | `session_id` | `ok: bool` | Minimize window |

### Tracing

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_trace_start` | `session_id`, `categories?: list` | `ok: bool` | Start tracing |
| `wavexis_trace_stop` | `session_id` | `trace: str` | Stop tracing |
| `wavexis_trace_combined` | `session_id`, `url: str` | `trace: str` | Combined trace with screenshots |
| `wavexis_annotate_screenshot` | `session_id`, `selector?: str` | `image: base64` | Screenshot with annotations |

---

## Vision Tier (7 tools)

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_mouse_move` | `session_id`, `x: int`, `y: int` | `ok: bool` | Move mouse to coordinates |
| `wavexis_mouse_click` | `session_id`, `x: int`, `y: int`, `button?: str` | `ok: bool` | Click at coordinates |
| `wavexis_mouse_down` | `session_id`, `x: int`, `y: int` | `ok: bool` | Mouse down at coordinates |
| `wavexis_mouse_up` | `session_id`, `x: int`, `y: int` | `ok: bool` | Mouse up at coordinates |
| `wavexis_mouse_drag` | `session_id`, `from_x: int`, `from_y: int`, `to_x: int`, `to_y: int` | `ok: bool` | Drag between coordinates |
| `wavexis_screenshot_region` | `session_id`, `x: int`, `y: int`, `width: int`, `height: int` | `image: base64` | Screenshot a region |
| `wavexis_element_at` | `session_id`, `x: int`, `y: int` | `element: dict` | Get element at coordinates |

---

## Video Tier (4 tools)

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_video_start` | `session_id`, `format?: str`, `fps?: int` | `recording_id: str` | Start video recording |
| `wavexis_video_stop` | `session_id`, `recording_id: str` | `video: base64` | Stop and get video |
| `wavexis_video_chapter` | `session_id`, `recording_id: str`, `title: str` | `ok: bool` | Add a chapter marker |
| `wavexis_video_overlay` | `session_id`, `recording_id: str`, `text: str` | `ok: bool` | Add action overlay text |

---

## Testing Tier (6 tools)

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_assert` | `session_id`, `expression: str`, `expected: str`, `op: str` | `result: dict` | Assert a condition |
| `wavexis_assert_visible` | `session_id`, `selector: str` | `result: dict` | Assert element visible |
| `wavexis_assert_text` | `session_id`, `selector: str`, `expected: str` | `result: dict` | Assert element text |
| `wavexis_assert_url` | `session_id`, `expected: str`, `op: str` | `result: dict` | Assert current URL |
| `wavexis_assert_title` | `session_id`, `expected: str`, `op: str` | `result: dict` | Assert page title |
| `wavexis_locator` | `session_id`, `selector: str` | `locator: dict` | Generate robust locator |

---

## Workflows Tier (6 tools)

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_multi` | `session_id`, `config: str` | `results: list` | Execute multi-action YAML |
| `wavexis_raw_cdp` | `session_id`, `method: str`, `params?: dict` | `result: any` | Raw CDP method call |
| `wavexis_raw_bidi` | `session_id`, `method: str`, `params?: dict` | `result: any` | Raw BiDi method call |
| `wavexis_browser_context_create` | `session_id` | `context_id: str` | Create browser context |
| `wavexis_browser_context_list` | `session_id` | `contexts: list` | List browser contexts |
| `wavexis_browser_context_close` | `session_id`, `context_id: str` | `ok: bool` | Close browser context |

---

## Data Tier (7 tools)

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_codegen` | `session_id`, `language?: str` | `code: str` | Generate code from actions |
| `wavexis_lighthouse` | `session_id`, `categories?: list`, `form_factor?: str` | `report: dict` | Run Lighthouse audit |
| `wavexis_extract` | `session_id`, `schema: dict` | `data: dict` | Extract structured data |
| `wavexis_websocket_intercept_data` | `session_id`, `url: str` | `data: list` | Intercept WebSocket data |
| `wavexis_crawl` | `session_id`, `url: str`, `depth?: int` | `results: list` | Crawl a website |
| `wavexis_visual_diff` | `session_id`, `baseline: str`, `threshold?: float` | `diff: dict` | Visual regression |
| `wavexis_cwv` | `session_id`, `budget?: dict` | `metrics: dict` | Core Web Vitals |

---

## Experimental Tier (31 tools)

### Service Workers

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_sw_list` | `session_id` | `workers: list` | List service workers |
| `wavexis_sw_unregister` | `session_id`, `id: str` | `ok: bool` | Unregister service worker |
| `wavexis_sw_update` | `session_id`, `id: str` | `ok: bool` | Update service worker |

### Animations

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_animation_playback_rate` | `session_id`, `rate: float` | `ok: bool` | Set playback rate |
| `wavexis_animation_screenshot` | `session_id`, `id: str` | `image: base64` | Screenshot animation frame |

### WebAuthn

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_webauthn_add` | `session_id`, `protocol: str`, `transport: str` | `auth_id: str` | Add virtual authenticator |
| `wavexis_webauthn_remove` | `session_id`, `auth_id: str` | `ok: bool` | Remove authenticator |
| `wavexis_webauthn_credential` | `session_id`, `auth_id: str`, `rp_id: str` | `credential: dict` | Create credential |

### Media

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_media_play` | `session_id`, `selector: str` | `ok: bool` | Play media element |
| `wavexis_media_pause` | `session_id`, `selector: str` | `ok: bool` | Pause media element |
| `wavexis_media_seek` | `session_id`, `selector: str`, `time: float` | `ok: bool` | Seek media element |

### Cast

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_cast_start` | `session_id`, `sink_name: str` | `ok: bool` | Start casting |
| `wavexis_cast_stop` | `session_id` | `ok: bool` | Stop casting |

### Bluetooth

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_bluetooth_emulate` | `session_id`, `manufacturer: str` | `ok: bool` | Emulate Bluetooth adapter |

### Extensions

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_extension_install` | `session_id`, `path: str` | `ok: bool` | Install extension |
| `wavexis_extension_uninstall` | `session_id`, `id: str` | `ok: bool` | Uninstall extension |
| `wavexis_extension_list` | `session_id` | `extensions: list` | List extensions |

### Preferences

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_pref_get` | `session_id`, `key: str` | `value: any` | Get preference |
| `wavexis_pref_set` | `session_id`, `key: str`, `value: any` | `ok: bool` | Set preference |

### Additional Experimental

| Tool | Parameters | Returns | Description |
|------|-----------|---------|-------------|
| `wavexis_fedcm_status` | `session_id` | `status: dict` | FedCM status |
| `wavexis_fedcm_select` | `session_id`, `account: str` | `ok: bool` | FedCM account selection |
| `wavexis_database_execute` | `session_id`, `db: str`, `sql: str` | `result: any` | Execute WebSQL |
| `wavexis_layer_tree` | `session_id` | `layers: list` | Get layer tree |
| `wavexis_dom_storage_items` | `session_id`, `origin: str` | `items: list` | Get DOM storage items |
| `wavexis_dom_storage_set` | `session_id`, `origin: str`, `key: str`, `value: str` | `ok: bool` | Set DOM storage item |
| `wavexis_headless_enable` | `session_id` | `ok: bool` | Enable headless frame control |
| `wavexis_headless_disable` | `session_id` | `ok: bool` | Disable headless frame control |
| `wavexis_sensor_override` | `session_id`, `type: str`, `value: dict` | `ok: bool` | Override sensor reading |
| `wavexis_device_orientation` | `session_id`, `alpha: float`, `beta: float`, `gamma: float` | `ok: bool` | Override device orientation |
| `wavexis_pwa_install` | `session_id`, `url: str` | `ok: bool` | Install PWA |
| `wavexis_pwa_uninstall` | `session_id`, `id: str` | `ok: bool` | Uninstall PWA |

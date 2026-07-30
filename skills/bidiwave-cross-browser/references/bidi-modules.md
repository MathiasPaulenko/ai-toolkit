# BiDi Modules Reference — All 12 Modules

> Complete reference of all 12 WebDriver BiDi modules implemented in bidiwave.

## How Modules Work in bidiwave

Each `BiDiClient` exposes modules as properties:

```python
client.browsing      # Browsing contexts, navigation, screenshots
client.script        # Script evaluation, RemoteValue, preload
client.input         # Mouse, keyboard, scroll, drag, file upload
client.network       # Interception, headers, auth, cache
client.storage       # Cookies, partition keys
client.emulation     # Geolocation, locale, timezone, UA, network
client.permissions   # Grant/deny browser permissions
client.preload       # Preload scripts with channels
client.log           # Console log entries
client.web_extension # Install/uninstall extensions
client.cdp           # CDP bridge for Chrome-specific features
client.session       # Session management, subscriptions
```

## Module Catalog

### Browsing (`client.browsing`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `open()` | `url: str` | `Page` | Open a new browsing context |
| `navigate()` | `context: str`, `url: str` | `NavigationInfo` | Navigate to URL |
| `reload()` | `context: str` | `NavigationInfo` | Reload current page |
| `traverse_history()` | `context: str`, `direction: str` | `HistoryResult` | Go back/forward |
| `screenshot()` | `context: str` | `bytes` | Take screenshot |
| `set_viewport()` | `context: str`, `viewport: ViewportSize`, `device_pixel_ratio?: float` | `None` | Set viewport size |
| `print_to_pdf()` | `context: str` | `bytes` | Print page to PDF |
| `handle_user_prompt()` | `context: str`, `accept: bool`, `user_text?: str` | `None` | Handle dialog |
| `close()` | `context: str` | `None` | Close browsing context |
| `get_tree()` | `root?: str` | `list[ContextInfo]` | Get context tree |
| `wait_for_element()` | `context: str`, `selector: str`, `locator?: str`, `timeout?: float` | `ElementInfo` | Wait for element |

### Script (`client.script`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `evaluate()` | `expression: str`, `target: str`, `await_promise?: bool`, `return_by_value?: bool` | `RemoteValue` | Evaluate JS expression |
| `call_function()` | `function_declaration: str`, `args?: list`, `target: str`, `await_promise?: bool` | `RemoteValue` | Call JS function |
| `get_realms()` | `filter?: RealmFilter` | `list[RealmInfo]` | Get all realms |
| `disown()` | `handles: list[str]`, `target: str` | `None` | Disown remote handles |
| `add_preload_script()` | `function_declaration: str`, `arguments?: list`, `sandbox?: str` | `PreloadScript` | Add preload script |
| `remove_preload_script()` | `script: str` | `None` | Remove preload script |

### Input (`client.input`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `click()` | `context: str`, `x: int`, `y: int`, `button?: str` | `None` | Click at coordinates |
| `type_text()` | `context: str`, `text: str` | `None` | Type text |
| `press_key()` | `context: str`, `key: str` | `None` | Press a key |
| `scroll()` | `context: str`, `delta_x?: int`, `delta_y?: int`, `origin?: str` | `None` | Scroll page |
| `drag_and_drop()` | `context: str`, `x1: int`, `y1: int`, `x2: int`, `y2: int` | `None` | Drag and drop |
| `set_files()` | `context: str`, `paths: list[str]` | `None` | Set file input |

### Network (`client.network`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_intercept()` | `phases: list[str]`, `url_patterns?: list[str]` | `Intercept` | Add network intercept |
| `remove_intercept()` | `intercept_id: str` | `None` | Remove intercept |
| `continue_request()` | `request_id: str`, `url?: str`, `method?: str`, `headers?: list` | `None` | Continue with modifications |
| `fail_request()` | `request_id: str`, `error: str` | `None` | Fail a request |
| `provide_response()` | `request_id: str`, `status_code: int`, `headers?: list`, `body?: str` | `None` | Provide mock response |
| `continue_with_auth()` | `request_id: str`, `credentials: dict` | `None` | Continue with auth |
| `set_extra_headers()` | `headers: dict`, `contexts?: list[str]` | `None` | Set extra headers |
| `get_response_body()` | `request_id: str` | `ResponseBody` | Get response body |

### Storage (`client.storage`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `get_cookies()` | `context: str`, `filter?: CookieFilter` | `list[Cookie]` | Get cookies |
| `set_cookie()` | `context: str`, `cookie: Cookie` | `None` | Set a cookie |
| `delete_cookie()` | `context: str`, `name: str`, `domain?: str` | `None` | Delete a cookie |
| `delete_cookies()` | `context: str`, `filter?: CookieFilter` | `None` | Delete matching cookies |

### Emulation (`client.emulation`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `set_geolocation_override()` | `coordinates: dict`, `contexts?: list[str]` | `None` | Override geolocation |
| `set_locale_override()` | `locale: str`, `contexts?: list[str]` | `None` | Override locale |
| `set_timezone_override()` | `timezone: str`, `contexts?: list[str]` | `None` | Override timezone |
| `set_user_agent_override()` | `user_agent: str`, `contexts?: list[str]` | `None` | Override user agent |
| `set_network_conditions()` | `network_conditions: dict`, `contexts?: list[str]` | `None` | Set network conditions |
| `set_screen_orientation_override()` | `orientation: dict`, `contexts?: list[str]` | `None` | Override orientation |

### Permissions (`client.permissions`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `set_permission()` | `descriptor: dict`, `state: str`, `contexts?: list[str]` | `None` | Set permission state |

### Preload (`client.preload`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_preload_script()` | `function_declaration: str`, `arguments?: list`, `sandbox?: str`, `user_contexts?: list[str]` | `PreloadScript` | Add preload script |
| `remove_preload_script()` | `script: str` | `None` | Remove preload script |

### Log (`client.log`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `get_log_entries()` | `filter?: LogFilter` | `list[LogEntry]` | Get log entries |

### Web Extension (`client.web_extension`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `install()` | `path: str` | `Extension` | Install extension |
| `uninstall()` | `extension: str` | `None` | Uninstall extension |

### CDP Bridge (`client.cdp`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `send_command()` | `method: str`, `params?: dict` | `dict` | Send raw CDP command |

### Session (`client.session`)

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `subscribe()` | `events: list[str]` | `None` | Subscribe to events |
| `unsubscribe()` | `events: list[str]` | `None` | Unsubscribe from events |
| `get_status()` | — | `SessionStatus` | Get session status |
| `end()` | — | `None` | End the session |

## Event Subscription

Most events require explicit subscription before they fire:

```python
await client.session.subscribe([
    "log.entryAdded",
    "network.beforeRequestSent",
    "network.responseCompleted",
    "browsingContext.load",
    "storage.cookieChanged",
])
```

## Module Independence

Each module can be used independently. You don't need to subscribe to all events — only subscribe to what you need:

```python
# Only subscribe to network events for a network-only test
await client.session.subscribe([
    "network.beforeRequestSent",
    "network.responseCompleted",
])
```

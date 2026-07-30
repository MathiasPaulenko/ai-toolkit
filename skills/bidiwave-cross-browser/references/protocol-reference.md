# W3C WebDriver BiDi Protocol Reference

> Reference for the W3C WebDriver BiDi protocol (WD 2025-07-28) as implemented in bidiwave.

## Protocol Overview

WebDriver BiDi is a W3C standard bidirectional protocol for browser automation. Unlike the classic WebDriver protocol (W3C WebDriver), BiDi uses a WebSocket connection for real-time, bidirectional communication with the browser.

### Key characteristics

- **W3C standard** — not proprietary to any browser vendor
- **Bidirectional** — WebSocket-based, supports events from browser to client
- **Cross-browser** — Chrome, Firefox, Edge (Safari when BiDi support lands)
- **JSON-based** — all messages are JSON objects
- **Session-scoped** — commands are scoped to a session

### Protocol version

bidiwave implements W3C WebDriver BiDi (WD 2025-07-28).

## Message Format

### Command

```json
{
  "type": "command",
  "id": 1,
  "method": "browsingContext.navigate",
  "params": {
    "context": "context-id",
    "url": "https://example.com"
  }
}
```

### Response

```json
{
  "type": "success",
  "id": 1,
  "result": {
    "navigation": "navigation-id",
    "url": "https://example.com"
  }
}
```

### Error

```json
{
  "type": "error",
  "id": 1,
  "error": "no such frame",
  "message": "Frame not found"
}
```

### Event

```json
{
  "type": "event",
  "method": "browsingContext.load",
  "params": {
    "context": "context-id",
    "url": "https://example.com"
  }
}
```

## Command Categories

### Session commands

| Command | Description |
|---------|-------------|
| `session.new` | Create a new session |
| `session.end` | End the session |
| `session.status` | Get session status |
| `session.subscribe` | Subscribe to events |
| `session.unsubscribe` | Unsubscribe from events |

### Browsing context commands

| Command | Description |
|---------|-------------|
| `browsingContext.create` | Create a new browsing context |
| `browsingContext.close` | Close a browsing context |
| `browsingContext.navigate` | Navigate to a URL |
| `browsingContext.reload` | Reload the page |
| `browsingContext.traverseHistory` | Go back or forward |
| `browsingContext.print` | Print to PDF |
| `browsingContext.captureScreenshot` | Take a screenshot |
| `browsingContext.setViewport` | Set viewport size |
| `browsingContext.handleUserPrompt` | Handle dialog |
| `browsingContext.getTree` | Get context tree |
| `browsingContext.locateNodes` | Locate nodes by locator |

### Script commands

| Command | Description |
|---------|-------------|
| `script.evaluate` | Evaluate JS expression |
| `script.callFunction` | Call a JS function |
| `script.getRealms` | Get all realms |
| `script.disown` | Disown remote handles |
| `script.addPreloadScript` | Add preload script |
| `script.removePreloadScript` | Remove preload script |

### Input commands

| Command | Description |
|---------|-------------|
| `input.performActions` | Perform input actions |
| `input.releaseActions` | Release input state |
| `input.setFiles` | Set file input |

### Network commands

| Command | Description |
|---------|-------------|
| `network.addIntercept` | Add network intercept |
| `network.removeIntercept` | Remove intercept |
| `network.continueRequest` | Continue with modifications |
| `network.failRequest` | Fail a request |
| `network.provideResponse` | Provide mock response |
| `network.continueWithAuth` | Continue with auth |
| `network.setExtraHeaders` | Set extra headers |
| `network.getResponseBody` | Get response body |

### Storage commands

| Command | Description |
|---------|-------------|
| `storage.getCookies` | Get cookies |
| `storage.setCookie` | Set a cookie |
| `storage.deleteCookie` | Delete a cookie |
| `storage.deleteCookies` | Delete matching cookies |

### Emulation commands

| Command | Description |
|---------|-------------|
| `emulation.setGeolocationOverride` | Override geolocation |
| `emulation.setLocaleOverride` | Override locale |
| `emulation.setTimezoneOverride` | Override timezone |
| `emulation.setUserAgentOverride` | Override user agent |
| `emulation.setNetworkConditions` | Set network conditions |
| `emulation.setScreenOrientationOverride` | Override orientation |

### Permissions commands

| Command | Description |
|---------|-------------|
| `permissions.setPermission` | Set permission state |

### Preload commands

| Command | Description |
|---------|-------------|
| `script.addPreloadScript` | Add preload script |
| `script.removePreloadScript` | Remove preload script |

### Log commands

| Command | Description |
|---------|-------------|
| `log.getEntries` | Get log entries |

### Web extension commands

| Command | Description |
|---------|-------------|
| `webExtension.install` | Install extension |
| `webExtension.uninstall` | Uninstall extension |

### CDP bridge commands

| Command | Description |
|---------|-------------|
| `cdp.sendCommand` | Send raw CDP command |
| `cdp.getSession` | Get CDP session |

## Event Types

### Browsing context events

| Event | Description |
|-------|-------------|
| `browsingContext.contextCreated` | New context created |
| `browsingContext.contextDestroyed` | Context destroyed |
| `browsingContext.navigationStarted` | Navigation started |
| `browsingContext.fragmentNavigated` | Fragment navigation |
| `browsingContext.domContentLoaded` | DOM content loaded |
| `browsingContext.load` | Page fully loaded |
| `browsingContext.navigationAborted` | Navigation aborted |
| `browsingContext.navigationFailed` | Navigation failed |
| `browsingContext.userPromptOpened` | Dialog opened |
| `browsingContext.userPromptClosed` | Dialog closed |
| `browsingContext.downloadWillBegin` | Download starting |

### Network events

| Event | Description |
|---------|-------------|
| `network.beforeRequestSent` | Request about to be sent |
| `network.requestSent` | Request sent |
| `network.responseStarted` | Response started |
| `network.responseCompleted` | Response completed |
| `network.fetchError` | Fetch error |
| `network.authRequired` | Authentication required |
| `network.dataReceived` | Data received |

### Script events

| Event | Description |
|---------|-------------|
| `script.realmCreated` | New realm created |
| `script.realmDestroyed` | Realm destroyed |
| `script.message` | Channel message |

### Storage events

| Event | Description |
|---------|-------------|
| `storage.cookieChanged` | Cookie changed |

### Log events

| Event | Description |
|---------|-------------|
| `log.entryAdded` | Log entry added |

### Input events

| Event | Description |
|---------|-------------|
| `input.fileDialogOpened` | File dialog opened |

### Preload events

| Event | Description |
|---------|-------------|
| `script.preloadScriptAdded` | Preload script added |
| `script.preloadScriptRemoved` | Preload script removed |

## Error Codes

| Error | Description |
|-------|-------------|
| `invalid argument` | Invalid command parameters |
| `invalid session id` | Session not found |
| `no such frame` | Frame not found |
| `no such window` | Window not found |
| `no such element` | Element not found |
| `no such alert` | No alert present |
| `no such cookie` | Cookie not found |
| `no such intercept` | Intercept not found |
| `no such node` | Node not found |
| `no such realm` | Realm not found |
| `no such preload script` | Preload script not found |
| `no such request` | Request not found |
| `no such user context` | User context not found |
| `unable to capture screen` | Screenshot failed |
| `unable to close browser` | Close failed |
| `unable to set cookie` | Cookie set failed |
| `unable to set viewport` | Viewport set failed |
| `unexpected alert open` | Alert is open |
| `unknown command` | Command not recognized |
| `unknown error` | Unknown error |
| `unsupported operation` | Operation not supported |

## RemoteValue Serialization

BiDi serializes JavaScript values using a typed RemoteValue format:

### Primitive types

```json
{"type": "string", "value": "hello"}
{"type": "number", "value": 42}
{"type": "boolean", "value": true}
{"type": "null"}
{"type": "undefined"}
{"type": "bigint", "value": "9007199254740993"}
{"type": "symbol", "value": "Symbol(foo)"}
```

### Complex types

```json
{"type": "array", "value": [{"type": "number", "value": 1}]}
{"type": "object", "value": [["key", {"type": "string", "value": "val"}]]}
{"type": "date", "value": "2024-01-01T00:00:00.000Z"}
{"type": "regexp", "value": {"pattern": "foo", "flags": "g"}}
{"type": "map", "value": [["key", {"type": "string", "value": "val"}]]}
{"type": "set", "value": [{"type": "string", "value": "a"}]}
{"type": "error", "value": {"message": "msg", "stack": "..."}}
```

### DOM types

```json
{"type": "node", "sharedId": "node-id", "value": {"nodeType": 1, "localName": "div"}}
{"type": "nodelist", "value": [{"type": "node", ...}]}
{"type": "htmlcollection", "value": [{"type": "node", ...}]}
```

### Internal types

```json
{"type": "function", "value": "function() { ... }"}
{"type": "promise", "value": {"state": "pending"}}
{"type": "proxy", "value": "..."}
{"type": "typedarray", "value": [{"type": "number", "value": 1}]}
{"type": "arraybuffer", "value": "base64-data"}
{"type": "window", "value": {"context": "context-id"}}
```

## Comparison with CDP

| Feature | WebDriver BiDi | Chrome DevTools Protocol |
|---------|---------------|------------------------|
| Standard | W3C standard | Chromium-specific |
| Browsers | Chrome, Firefox, Edge | Chrome, Edge only |
| Transport | WebSocket | WebSocket |
| Events | Subscribe-based | Always-on |
| Serialization | RemoteValue | Chrome-specific |
| Preload scripts | Yes (with channels) | Yes (Page.addScriptToEvaluateOnNewDocument) |
| Network interception | Yes (BiDi spec) | Yes (Fetch domain) |
| Permissions | Yes (standard) | Yes (Browser domain) |
| Web extensions | Yes (BiDi spec) | No |
| CDP bridge | Yes (for Chrome features) | N/A |

## References

- [W3C WebDriver BiDi Specification](https://w3c.github.io/webdriver-bidi/)
- [WebDriver BiDi on MDN](https://developer.mozilla.org/en-US/docs/Web/WebDriver/WebDriver_BiDi)
- [bidiwave documentation](https://mathiaspaulenko.github.io/bidiwave/)
- [bidiwave on GitHub](https://github.com/MathiasPaulenko/bidiwave)

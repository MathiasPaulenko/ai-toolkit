# CDP Debugger Domain Reference

> Complete reference for the Chrome DevTools Protocol Debugger domain as implemented in cdpwave.

## Overview

The Debugger domain exposes JavaScript debugging capabilities: breakpoints, stepping, call frame inspection, scope chains, and script tracking.

## Enabling the Debugger

```python
await session.Debugger.enable()
```

Must be called before any other Debugger method. Disables with `Debugger.disable()`.

## Breakpoints

### set_breakpoint_by_url

Set a breakpoint at a specific line in a script identified by URL.

```python
result = await session.Debugger.set_breakpoint_by_url(
    url="https://example.com/app.js",
    line_number=42,        # 0-indexed
    column_number=0,       # optional
    condition="x > 100"    # optional
)
# Returns: { "breakpointId": "...", "locations": [...] }
```

### set_breakpoint

Set a breakpoint at a specific location in a script.

```python
result = await session.Debugger.set_breakpoint(
    location={
        "scriptId": "script123",
        "lineNumber": 10,
        "columnNumber": 0
    },
    condition="y === null"  # optional
)
# Returns: { "breakpointId": "...", "actualLocation": {...} }
```

### set_breakpoint_by_function

Set a breakpoint at the start of a function.

```python
result = await session.Debugger.set_breakpoint_by_function(
    function_name="handleClick"
)
```

### set_breakpoint_on_function_call

Set a breakpoint on a function call by object ID.

```python
result = await session.Debugger.set_breakpoint_on_function_call(
    object_id="object123"
)
```

### remove_breakpoint

Remove a breakpoint by ID.

```python
await session.Debugger.remove_breakpoint(
    breakpoint_id=breakpoint_id
)
```

### set_skip_all_breakpoints

Skip all breakpoints without removing them.

```python
await session.Debugger.set_skip_all_breakpoints(skip=True)
```

### set_breakpoints_active

Activate or deactivate all breakpoints.

```python
await session.Debugger.set_breakpoints_active(active=True)
```

## Pausing and Resuming

### pause

Pause JavaScript execution.

```python
await session.Debugger.pause()
```

### resume

Resume execution after a pause.

```python
await session.Debugger.resume()
```

### step_over

Step over the next function call.

```python
await session.Debugger.step_over()
```

### step_into

Step into the next function call.

```python
await session.Debugger.step_into()
```

### step_out

Step out of the current function.

```python
await session.Debugger.step_out()
```

## Call Frames and Scope

### get_possible_breakpoints

Get possible breakpoint locations in a range.

```python
result = await session.Debugger.get_possible_breakpoints(
    start={
        "scriptId": "script123",
        "lineNumber": 0,
        "columnNumber": 0
    },
    end={
        "scriptId": "script123",
        "lineNumber": 100,
        "columnNumber": 0
    }
)
# Returns: { "locations": [...] }
```

### get_script_source

Get the source code of a script.

```python
result = await session.Debugger.get_script_source(
    script_id="script123"
)
# Returns: { "scriptSource": "..." }
```

### get_stack_trace

Get a stack trace for a specific stack trace ID.

```python
result = await session.Debugger.get_stack_trace(
    stack_trace_id="trace123"
)
```

## Paused Event

When execution pauses, the `Debugger.paused` event fires:

```python
async def on_paused(event):
    print(f"Reason: {event['reason']}")
    # Reasons: breakpoint, step, exception, other, assert, DOM, etc.

    print(f"Call frames: {len(event['callFrames'])}")
    for frame in event["callFrames"]:
        print(f"  {frame['functionName']} at {frame['url']}:{frame['location']['lineNumber']}")

    if "hitBreakpoints" in event:
        print(f"Hit breakpoints: {event['hitBreakpoints']}")

session.Debugger.on("paused", on_paused)
```

### CallFrame object

| Field | Type | Description |
|-------|------|-------------|
| `callFrameId` | `str` | Unique call frame identifier |
| `functionName` | `str` | Function name |
| `functionLocation` | `object` | Location of the function |
| `location` | `object` | Current execution location |
| `url` | `str` | Script URL |
| `scopeChain` | `array` | Scope chain |
| `this` | `object` | `this` object |

### Scope object

| Field | Type | Description |
|-------|------|-------------|
| `type` | `str` | Scope type: `global`, `local`, `closure`, `catch`, `block`, `script`, `with`, `eval` |
| `object` | `object` | Scope object (RemoteObject) |
| `name` | `str` | Scope name (optional) |
| `startLocation` | `object` | Start location (optional) |
| `endLocation` | `object` | End location (optional) |

## Script Events

### scriptParsed

Fired when a script is parsed:

```python
async def on_script_parsed(event):
    print(f"Script: {event['url']}")
    print(f"Script ID: {event['scriptId']}")
    print(f"Lines: {event['endLine'] - event['startLine']}")

session.Debugger.on("scriptParsed", on_script_parsed)
```

### scriptFailedToParse

Fired when a script fails to parse:

```python
async def on_script_failed(event):
    print(f"Parse error: {event['exceptionDetails']}")

session.Debugger.on("scriptFailedToParse", on_script_failed)
```

## Methods Reference

| Method | Description |
|--------|-------------|
| `enable` | Enable the Debugger domain |
| `disable` | Disable the Debugger domain |
| `set_breakpoint_by_url` | Set breakpoint by URL and line |
| `set_breakpoint` | Set breakpoint by location |
| `set_breakpoint_by_function` | Set breakpoint by function name |
| `set_breakpoint_on_function_call` | Set breakpoint on function call |
| `remove_breakpoint` | Remove breakpoint by ID |
| `set_skip_all_breakpoints` | Skip all breakpoints |
| `set_breakpoints_active` | Activate/deactivate all breakpoints |
| `pause` | Pause execution |
| `resume` | Resume execution |
| `step_over` | Step over |
| `step_into` | Step into |
| `step_out` | Step out |
| `get_possible_breakpoints` | Get possible breakpoint locations |
| `get_script_source` | Get script source code |
| `get_stack_trace` | Get stack trace |
| `search_in_content` | Search script content |
| `set_pause_on_exceptions` | Pause on exceptions |
| `set_async_call_stack_depth` | Set async call stack depth |

## References

- [CDP Debugger domain](https://chromedevtools.github.io/devtools-protocol/tot/Debugger/)
- `references/heap-profiler.md` — HeapProfiler domain reference
- `references/profiler-domain.md` — Profiler domain reference

---
name: CDPWave Debugging
version: 1.0.0
author: Mathias Paulenko Echeverz
description: "Advanced debugging with cdpwave. Breakpoints, step debugging, CPU profiling, heap snapshots, code coverage, DOM debugger."
tags: [debugging, breakpoints, profiling, heap-snapshot]
trigger: When the user asks about debugging with cdpwave, needs breakpoints or step debugging, wants CPU profiling, needs heap snapshots, wants code coverage, or needs DOM debugger.
---

# CDPWave Debugging

## Description

Advanced debugging with cdpwave — set breakpoints, step through JavaScript, capture CPU profiles, take heap snapshots, measure code coverage, and use the DOM debugger for event-level debugging.

## When to Invoke

- Setting breakpoints and step debugging JavaScript
- Capturing and analyzing CPU profiles
- Taking heap snapshots for memory leak detection
- Measuring JS and CSS code coverage
- Setting DOM and event breakpoints
- Debugging JavaScript execution in automated tests

## Prerequisites

- `pip install cdpwave`
- Chrome or Edge launched with `--remote-debugging-port=9222`
- Basic familiarity with cdpwave (see `cdpwave-testing` skill)
- Python 3.11+ with `asyncio`

## Debugger Domain

The CDP Debugger domain provides full step-debugging capabilities over the DevTools Protocol.

### Setting breakpoints

#### debug_set_breakpoint

Set a breakpoint by URL, function, or script:

```python
import asyncio
from cdpwave import CDPSession

async def set_breakpoint():
    session = await CDPSession.connect("ws://localhost:9222")

    # Enable the Debugger domain
    await session.Debugger.enable()

    # Set breakpoint by URL and line number
    result = await session.Debugger.set_breakpoint_by_url(
        url="https://example.com/app.js",
        line_number=42,
        column_number=0
    )
    breakpoint_id = result["breakpointId"]

    # Set breakpoint by function name
    result = await session.Debugger.set_breakpoint_by_function(
        function_name="handleClick"
    )

    # Set breakpoint by script ID and line
    result = await session.Debugger.set_breakpoint(
        location={
            "scriptId": "script123",
            "lineNumber": 10,
            "columnNumber": 0
        }
    )

    await session.close()
```

#### Conditional breakpoints

```python
await session.Debugger.set_breakpoint_by_url(
    url="https://example.com/app.js",
    line_number=42,
    condition="x > 100"
)
```

#### Logpoints (breakpoints that log without pausing)

```python
await session.Debugger.set_breakpoint_by_url(
    url="https://example.com/app.js",
    line_number=42,
    condition="console.log('hit line 42, x=', x); false"
)
```

### Pausing and resuming

#### debug_pause

Pause JavaScript execution:

```python
await session.Debugger.pause()
```

#### debug_resume

Resume execution after a pause:

```python
await session.Debugger.resume()
```

### Step debugging

| Method | Description |
|--------|-------------|
| `Debugger.step_over` | Step over the next function call |
| `Debugger.step_into` | Step into the next function call |
| `Debugger.step_out` | Step out of the current function |
| `Debugger.resume` | Resume execution until next breakpoint |

```python
async def step_debug(session):
    # Wait for pause event
    paused = await session.Debugger.wait_for_pause()

    print(f"Paused at: {paused['callFrames'][0]['url']}")
    print(f"Line: {paused['callFrames'][0]['location']['lineNumber']}")

    # Step over
    await session.Debugger.step_over()
    paused = await session.Debugger.wait_for_pause()

    # Step into
    await session.Debugger.step_into()
    paused = await session.Debugger.wait_for_pause()

    # Step out
    await session.Debugger.step_out()
    paused = await session.Debugger.wait_for_pause()

    # Resume
    await session.Debugger.resume()
```

### Removing breakpoints

```python
# Remove a specific breakpoint
await session.Debugger.remove_breakpoint(breakpoint_id=breakpoint_id)

# Remove all breakpoints
await session.Debugger.set_skip_all_breakpoints(skip=True)
```

### Call frames and scope

When paused, inspect call frames and scope chains:

```python
async def inspect_pause(session):
    paused = await session.Debugger.wait_for_pause()

    for frame in paused["callFrames"]:
        print(f"Function: {frame['functionName']}")
        print(f"URL: {frame['url']}")
        print(f"Line: {frame['location']['lineNumber']}")

        for scope in frame["scopeChain"]:
            print(f"  Scope: {scope['type']}")  # global, local, closure, catch, block, script, with
            obj = await session.Runtime.get_properties(
                object_id=scope["object"]["objectId"],
                own_properties=True
            )
            for prop in obj["result"]:
                print(f"    {prop['name']} = {prop.get('value', {}).get('value', 'N/A')}")
```

## HeapProfiler Domain

Capture heap snapshots for memory leak detection and analysis.

### Taking a heap snapshot

```python
async def heap_snapshot(session):
    await session.HeapProfiler.enable()

    # Capture heap snapshot
    snapshot_data = []
    async for event in session.HeapProfiler.take_heap_snapshot():
        snapshot_data.append(event)

    # Save snapshot
    with open("heap.heapsnapshot", "w") as f:
        json.dump(snapshot_data, f)
```

### Heap sampling

```python
async def heap_sampling(session):
    await session.HeapProfiler.enable()

    # Start sampling
    await session.HeapProfiler.start_sampling()

    # ... run page interactions ...

    # Stop sampling and get results
    profile = await session.HeapProfiler.stop_sampling()

    with open("heap-sampling.json", "w") as f:
        json.dump(profile, f)
```

### Tracking heap object allocations

```python
async def track_allocations(session):
    await session.HeapProfiler.enable()

    # Start tracking
    await session.HeapProfiler.start_tracking_heap_objects()

    # ... run page interactions ...

    # Stop tracking and get snapshot
    await session.HeapProfiler.stop_tracking_heap_objects()

    # Get tracked objects
    objects = await session.HeapProfiler.get_heap_object_id()
```

### Heap snapshot analysis

```python
import json

def analyze_heap(snapshot_path):
    with open(snapshot_path) as f:
        snapshot = json.load(f)

    nodes = snapshot["nodes"]
    strings = snapshot["strings"]

    # Count nodes by type
    type_counts = {}
    for i in range(0, len(nodes), 7):
        type_idx = nodes[i]
        type_name = strings[type_idx]
        type_counts[type_name] = type_counts.get(type_name, 0) + 1

    for type_name, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"{type_name}: {count}")
```

## Profiler Domain

Capture CPU profiles to identify performance bottlenecks.

### CPU profiling

```python
async def cpu_profile(session):
    await session.Profiler.enable()

    # Start profiling
    await session.Profiler.start()

    # ... run page interactions ...

    # Stop profiling and get profile
    profile = await session.Profiler.stop()

    with open("cpu-profile.json", "w") as f:
        json.dump(profile, f)
```

### Profiling with precision

```python
async def precise_profile(session):
    await session.Profiler.enable()

    # Set sampling interval (default is 1000us = 1ms)
    await session.Profiler.set_sampling_interval(interval=100)  # 100us = 0.1ms

    await session.Profiler.start()

    # ... run interactions ...

    profile = await session.Profiler.stop()
```

### CPU profile analysis

```python
import json

def analyze_cpu_profile(profile_path):
    with open(profile_path) as f:
        profile = json.load(f)

    nodes = profile["profile"]["nodes"]
    samples = profile["profile"]["samples"]
    time_deltas = profile["profile"]["timeDeltas"]

    # Find hot functions (most samples)
    sample_counts = {}
    for sample in samples:
        sample_counts[sample] = sample_counts.get(sample, 0) + 1

    # Map node IDs to function names
    node_map = {n["id"]: n for n in nodes}

    for node_id, count in sorted(sample_counts.items(), key=lambda x: -x[1])[:10]:
        node = node_map[node_id]
        func = node["callFrame"]["functionName"] or "(anonymous)"
        url = node["callFrame"]["url"]
        line = node["callFrame"]["lineNumber"]
        print(f"{func} at {url}:{line} — {count} samples")
```

## DOMDebugger Domain

Set breakpoints on DOM events and DOM modifications.

### Event breakpoints

```python
async def event_breakpoints(session):
    await session.DOMDebugger.enable()

    # Break on all click events
    await session.DOMDebugger.set_event_breakpoint(
        event_name="click"
    )

    # Break on XHR load
    await session.DOMDebugger.set_event_breakpoint(
        event_name="load",
        target_name="XMLHttpRequest"
    )

    # Break on specific event
    await session.DOMDebugger.set_event_breakpoint(
        event_name="submit"
    )
```

### DOM breakpoints

```python
async def dom_breakpoints(session):
    await session.DOMDebugger.enable()

    # Get a DOM node first
    document = await session.DOM.get_document()
    node_id = document["root"]["children"][1]["children"][0]["nodeId"]

    # Break on subtree modification
    await session.DOMDebugger.set_dom_breakpoint(
        node_id=node_id,
        type="subtree-modified"  # subtree-modified, attribute-modified, node-removed
    )

    # Break on attribute modification
    await session.DOMDebugger.set_dom_breakpoint(
        node_id=node_id,
        type="attribute-modified"
    )

    # Break on node removal
    await session.DOMDebugger.set_dom_breakpoint(
        node_id=node_id,
        type="node-removed"
    )
```

### Removing DOM breakpoints

```python
# Remove specific DOM breakpoint
await session.DOMDebugger.remove_dom_breakpoint(
    node_id=node_id,
    type="subtree-modified"
)

# Remove event breakpoint
await session.DOMDebugger.remove_event_breakpoint(
    event_name="click"
)
```

## Code Coverage

Measure JS and CSS code coverage to find unused code.

### JS coverage

```python
async def js_coverage(session):
    await session.Profiler.enable()
    await session.Profiler.start_precise_coverage(
        call_count=True,
        detailed=True
    )

    # ... run page interactions ...

    # Get coverage results
    result = await session.Profiler.take_precise_coverage()

    for script in result["result"]:
        url = script["url"]
        functions = script["functions"]
        for func in functions:
            func_name = func["functionName"] or "(anonymous)"
            for range in func["ranges"]:
                start = range["startOffset"]
                end = range["endOffset"]
                count = range["count"]
                if count == 0:
                    print(f"UNUSED: {func_name} in {url} [{start}:{end}]")

    await session.Profiler.stop_precise_coverage()
```

### CSS coverage

```python
async def css_coverage(session):
    await session.CSS.enable()
    await session.CSS.start_rule_usage_tracking()

    # ... run page interactions ...

    # Get coverage results
    result = await session.CSS.stop_rule_usage_tracking()

    for rule in result["ruleUsage"]:
        style_sheet_id = rule["styleSheetId"]
        start = rule["startOffset"]
        end = rule["endOffset"]
        used = rule["used"]
        if not used:
            print(f"UNUSED CSS: sheet={style_sheet_id} [{start}:{end}]")
```

## Combined Debug Session

A complete debug session combining breakpoints, profiling, and heap analysis:

```python
import asyncio
import json
from cdpwave import CDPSession

async def debug_session():
    session = await CDPSession.connect("ws://localhost:9222")

    # Enable all required domains
    await session.Debugger.enable()
    await session.Profiler.enable()
    await session.HeapProfiler.enable()

    # Set breakpoint
    bp = await session.Debugger.set_breakpoint_by_url(
        url="https://example.com/app.js",
        line_number=42,
        condition="x > 100"
    )

    # Start CPU profiling
    await session.Profiler.start()

    # Navigate to trigger the breakpoint
    await session.Page.enable()
    await session.Page.navigate(url="https://example.com")

    # Wait for pause
    paused = await session.Debugger.wait_for_pause()
    print(f"Paused at line {paused['callFrames'][0]['location']['lineNumber']}")

    # Inspect call frames
    for frame in paused["callFrames"][:3]:
        print(f"  {frame['functionName']} at {frame['url']}:{frame['location']['lineNumber']}")

    # Resume
    await session.Debugger.resume()

    # Wait for page load
    await session.Page.wait_for_load()

    # Stop CPU profiling
    cpu_profile = await session.Profiler.stop()
    with open("cpu-profile.json", "w") as f:
        json.dump(cpu_profile, f)

    # Take heap snapshot
    snapshot = []
    async for chunk in session.HeapProfiler.take_heap_snapshot():
        snapshot.append(chunk)
    with open("heap.heapsnapshot", "w") as f:
        json.dump(snapshot, f)

    # Clean up
    await session.Debugger.remove_breakpoint(breakpoint_id=bp["breakpointId"])
    await session.close()

asyncio.run(debug_session())
```

## Best Practices

- **Enable domains before use** — `Debugger.enable()`, `Profiler.enable()`, etc.
- **Use conditional breakpoints** — avoid pausing on every hit; filter by condition.
- **Set sampling interval for precision** — lower intervals give more detail but more overhead.
- **Capture heap snapshots before and after** — compare to find memory leaks.
- **Run coverage with realistic interactions** — navigate and interact to exercise code paths.
- **Clean up breakpoints** — remove breakpoints after debugging to avoid side effects.
- **Save profiles as files** — CPU and heap profiles are large; save to disk for analysis.
- **Use logpoints for non-intrusive logging** — `condition="console.log(...); false"` doesn't pause.
- **Disable domains when done** — `Debugger.disable()` etc. to reduce overhead.
- **Use `wait_for_pause()` in async code** — avoids polling for pause events.

## Common Pitfalls

- **Not enabling domains** — methods fail silently if the domain isn't enabled.
- **Breakpoint line numbers are 0-indexed** — line 42 in the editor is line 41 in CDP.
- **Heap snapshots are large** — can be 50-200 MB for complex pages; save to disk.
- **CPU profiling overhead** — profiling slows execution; use for diagnosis, not benchmarking.
- **Coverage without interactions** — only code that executes is measured; interact with the page.
- **DOM breakpoints need node IDs** — get them from `DOM.get_document()` or `DOM.query_selector()`.
- **Event breakpoints pause on all instances** — `set_event_breakpoint("click")` pauses on every click.
- **Forgetting to stop profiling** — `Profiler.stop()` must be called to get results.

## References

- `references/debugger-domain.md` — CDP Debugger domain reference
- `references/heap-profiler.md` — CDP HeapProfiler domain reference
- `references/profiler-domain.md` — CDP Profiler domain reference
- `assets/templates/debug-session.py` — Debug session template
- `assets/templates/heap-analysis.py` — Heap analysis template
- [Chrome DevTools Protocol — Debugger](https://chromedevtools.github.io/devtools-protocol/tot/Debugger/)
- [Chrome DevTools Protocol — HeapProfiler](https://chromedevtools.github.io/devtools-protocol/tot/HeapProfiler/)
- [Chrome DevTools Protocol — Profiler](https://chromedevtools.github.io/devtools-protocol/tot/Profiler/)
- [Chrome DevTools Protocol — DOMDebugger](https://chromedevtools.github.io/devtools-protocol/tot/DOMDebugger/)

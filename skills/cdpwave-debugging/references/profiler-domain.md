# CDP Profiler Domain Reference

> Complete reference for the Chrome DevTools Protocol Profiler domain as implemented in cdpwave.

## Overview

The Profiler domain provides CPU profiling and code coverage capabilities for performance analysis.

## Enabling the Profiler

```python
await session.Profiler.enable()
```

## CPU Profiling

### start

Start CPU profiling:

```python
await session.Profiler.start()
```

### stop

Stop profiling and get the profile:

```python
profile = await session.Profiler.stop()
# Returns: { "profile": { "nodes": [...], "startTime": ..., "endTime": ..., "samples": [...], "timeDeltas": [...] } }

with open("cpu-profile.json", "w") as f:
    json.dump(profile, f)
```

### set_sampling_interval

Set the CPU sampling interval (in microseconds). Must be called before `start()`:

```python
await session.Profiler.set_sampling_interval(
    interval=100  # 100us = 0.1ms (higher precision, more overhead)
)
```

Default is 1000us (1ms). Lower values give more detail but more overhead.

### Sampling interval guide

| Interval | Precision | Overhead | Use case |
|----------|-----------|----------|----------|
| 100us | Very high | High | Micro-optimization, hot path analysis |
| 500us | High | Medium | Function-level analysis |
| 1000us (default) | Standard | Low | General profiling |
| 5000us | Low | Very low | Long-running sessions, overview |

## CPU Profile Format

### Profile object

| Field | Type | Description |
|-------|------|-------------|
| `nodes` | `array` | Profile nodes (call tree) |
| `startTime` | `int` | Profile start timestamp (microseconds) |
| `endTime` | `int` | Profile end timestamp (microseconds) |
| `samples` | `array` | Sampled node IDs |
| `timeDeltas` | `array` | Time between samples (microseconds) |

### ProfileNode object

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Unique node ID |
| `callFrame` | `object` | Function call frame |
| `hitCount` | `int` | Number of samples hitting this node |
| `children` | `array` | Child node IDs |
| `positionTicks` | `array` | Position ticks (optional) |

### CallFrame object

| Field | Type | Description |
|-------|------|-------------|
| `functionName` | `str` | Function name |
| `scriptId` | `str` | Script ID |
| `url` | `str` | Script URL |
| `lineNumber` | `int` | Line number (0-indexed) |
| `columnNumber` | `int` | Column number |

## CPU Profile Analysis

### Finding hot functions

```python
import json

def find_hot_functions(profile_path):
    with open(profile_path) as f:
        data = json.load(f)

    profile = data["profile"]
    nodes = profile["nodes"]
    samples = profile["samples"]
    time_deltas = profile["timeDeltas"]

    # Count samples per node
    sample_counts = {}
    for i, sample in enumerate(samples):
        delta = time_deltas[i] if i < len(time_deltas) else 0
        if sample not in sample_counts:
            sample_counts[sample] = {"count": 0, "time": 0}
        sample_counts[sample]["count"] += 1
        sample_counts[sample]["time"] += delta

    # Map node IDs to call frames
    node_map = {n["id"]: n for n in nodes}

    # Sort by time (descending)
    hot = sorted(sample_counts.items(), key=lambda x: -x[1]["time"])

    print("Hot functions (by CPU time):")
    for node_id, stats in hot[:20]:
        node = node_map[node_id]
        func = node["callFrame"]["functionName"] or "(anonymous)"
        url = node["callFrame"]["url"]
        line = node["callFrame"]["lineNumber"]
        time_ms = stats["time"] / 1000  # microseconds to milliseconds
        print(f"  {time_ms:.1f}ms — {func} at {url}:{line} ({stats['count']} samples)")
```

### Building a flame graph

```python
def build_call_tree(profile_path):
    with open(profile_path) as f:
        data = json.load(f)

    nodes = data["profile"]["nodes"]
    node_map = {n["id"]: n for n in nodes}

    # Find root node (no parent)
    child_ids = set()
    for n in nodes:
        child_ids.update(n.get("children", []))
    root_ids = [n["id"] for n in nodes if n["id"] not in child_ids]

    def print_tree(node_id, depth=0):
        node = node_map[node_id]
        func = node["callFrame"]["functionName"] or "(anonymous)"
        hits = node.get("hitCount", 0)
        print(f"{'  ' * depth}{func} (hits: {hits})")
        for child_id in node.get("children", []):
            print_tree(child_id, depth + 1)

    for root_id in root_ids:
        print_tree(root_id)
```

## Code Coverage

### start_precise_coverage

Start precise JS code coverage:

```python
await session.Profiler.start_precise_coverage(
    call_count=True,    # Track call counts per function
    detailed=True       # Track per-block coverage (not just per-function)
)
```

### take_precise_coverage

Get current coverage results:

```python
result = await session.Profiler.take_precise_coverage()
# Returns: { "result": [ { "scriptId": ..., "url": ..., "functions": [...] } ] }

for script in result["result"]:
    url = script["url"]
    for func in script["functions"]:
        func_name = func["functionName"] or "(anonymous)"
        for range in func["ranges"]:
            start = range["startOffset"]
            end = range["endOffset"]
            count = range["count"]
            status = "USED" if count > 0 else "UNUSED"
            print(f"{status}: {func_name} in {url} [{start}:{end}] (count={count})")
```

### stop_precise_coverage

Stop precise coverage:

```python
await session.Profiler.stop_precise_coverage()
```

### Best effort coverage

For lower-overhead coverage without precise counts:

```python
await session.Profiler.start_coverage()
# ... run interactions ...
result = await session.Profiler.take_coverage()
await session.Profiler.stop_coverage()
```

## CSS Coverage

CSS coverage uses the CSS domain, not the Profiler domain:

### start_rule_usage_tracking

```python
await session.CSS.enable()
await session.CSS.start_rule_usage_tracking()
```

### stop_rule_usage_tracking

```python
result = await session.CSS.stop_rule_usage_tracking()
# Returns: { "ruleUsage": [ { "styleSheetId": ..., "startOffset": ..., "endOffset": ..., "used": bool } ] }

for rule in result["ruleUsage"]:
    status = "USED" if rule["used"] else "UNUSED"
    print(f"{status}: sheet={rule['styleSheetId']} [{rule['startOffset']}:{rule['endOffset']}]")
```

## Events

### consoleProfileStarted

```python
async def on_profile_started(event):
    print(f"Profile started: {event['title']}")

session.Profiler.on("consoleProfileStarted", on_profile_started)
```

### consoleProfileFinished

```python
async def on_profile_finished(event):
    print(f"Profile finished: {event['title']}")
    profile = event["profile"]
    with open(f"{event['title']}.json", "w") as f:
        json.dump(profile, f)

session.Profiler.on("consoleProfileFinished", on_profile_finished)
```

## Methods Reference

| Method | Description |
|--------|-------------|
| `enable` | Enable Profiler domain |
| `disable` | Disable Profiler domain |
| `start` | Start CPU profiling |
| `stop` | Stop CPU profiling and get profile |
| `set_sampling_interval` | Set sampling interval (microseconds) |
| `start_precise_coverage` | Start precise JS coverage |
| `take_precise_coverage` | Get coverage results |
| `stop_precise_coverage` | Stop precise coverage |
| `start_coverage` | Start best-effort coverage |
| `take_coverage` | Get best-effort coverage |
| `stop_coverage` | Stop best-effort coverage |
| `get_best_effort_coverage` | Get coverage without starting |

## References

- [CDP Profiler domain](https://chromedevtools.github.io/devtools-protocol/tot/Profiler/)
- `references/debugger-domain.md` — Debugger domain reference
- `references/heap-profiler.md` — HeapProfiler domain reference

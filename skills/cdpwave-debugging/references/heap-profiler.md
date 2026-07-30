# CDP HeapProfiler Domain Reference

> Complete reference for the Chrome DevTools Protocol HeapProfiler domain as implemented in cdpwave.

## Overview

The HeapProfiler domain provides heap snapshot and sampling capabilities for memory analysis and leak detection.

## Enabling the HeapProfiler

```python
await session.HeapProfiler.enable()
```

## Heap Snapshots

### take_heap_snapshot

Capture a full heap snapshot. This is an async generator that yields chunks of the serialized snapshot:

```python
snapshot_chunks = []
async for chunk in session.HeapProfiler.take_heap_snapshot():
    snapshot_chunks.append(chunk)

# Save as .heapsnapshot file (loadable in Chrome DevTools)
with open("heap.heapsnapshot", "w") as f:
    json.dump(snapshot_chunks, f)
```

### Heap snapshot format

The heap snapshot contains:

| Section | Description |
|---------|-------------|
| `snapshot` | Meta information (node count, edge count, types) |
| `nodes` | Array of node data (flat array, 7 fields per node) |
| `edges` | Array of edge data (flat array, 3 fields per edge) |
| `strings` | String table referenced by nodes and edges |

### Node fields (7 per node)

| Index | Field | Description |
|-------|-------|-------------|
| 0 | `type` | Index into `snapshot.meta.node_types[0]` → `strings` |
| 1 | `name` | Index into `strings` |
| 2 | `id` | Unique node ID |
| 3 | `self_size` | Size in bytes |
| 4 | `edge_count` | Number of outgoing edges |
| 5 | `trace_node_id` | Trace node ID (for allocation tracking) |
| 6 | `detachedness` | Detached state |

### Node types

| Type | Description |
|------|-------------|
| `hidden` | Hidden node (internal) |
| `array` | Array |
| `string` | String |
| `object` | Generic object |
| `code` | Compiled code |
| `closure` | Closure |
| `regexp` | Regular expression |
| `number` | Number |
| `native` | Native object |
| `synthetic` | Synthetic object |
| `concatenated string` | Concatenated string |
| `sliced string` | Sliced string |
| `symbol` | Symbol |
| `bigint` | BigInt |

## Heap Sampling

### start_sampling

Start heap sampling profiling:

```python
await session.HeapProfiler.start_sampling(
    sampling_interval=32768  # bytes, default 32768
)
```

### stop_sampling

Stop sampling and get the sampling profile:

```python
profile = await session.HeapProfiler.stop_sampling()
# Returns: { "profile": { "samples": [...], "samples": [...] } }

with open("heap-sampling.json", "w") as f:
    json.dump(profile, f)
```

## Allocation Tracking

### start_tracking_heap_objects

Start tracking heap object allocations:

```python
await session.HeapProfiler.start_tracking_heap_objects(
    track_allocations=True
)
```

### stop_tracking_heap_objects

Stop tracking and get the snapshot:

```python
await session.HeapProfiler.stop_tracking_heap_objects(
    report_progress=True
)
```

### take_heap_snapshot with progress

```python
async for event in session.HeapProfiler.take_heap_snapshot(report_progress=True):
    if "progress" in event:
        print(f"Progress: {event['progress']}%")
    else:
        # Snapshot data chunk
        pass
```

## Object Inspection

### get_heap_object_id

Get the heap object ID for a RemoteObject:

```python
result = await session.HeapProfiler.get_heap_object_id(
    object_id="object123"
)
# Returns: { "heapSnapshotObjectId": "..." }
```

### get_object_by_heap_object_id

Get a RemoteObject by heap object ID:

```python
result = await session.HeapProfiler.get_object_by_heap_object_id(
    object_id="heap123",
    object_group="console"  # optional
)
# Returns: { "result": RemoteObject, "preview": ... }
```

### inspect_heap_object

Request inspection of a heap object:

```python
await session.HeapProfiler.inspect_heap_object(
    object_id="heap123"
)
```

## Events

### addHeapSnapshotChunk

Fired during `take_heap_snapshot`:

```python
async def on_chunk(event):
    print(f"Chunk: {len(event['chunk'])} bytes")

session.HeapProfiler.on("addHeapSnapshotChunk", on_chunk)
```

### reportHeapSnapshotProgress

Fired during snapshot capture with progress:

```python
async def on_progress(event):
    print(f"Progress: {event['done']}/{event['total']}")

session.HeapProfiler.on("reportHeapSnapshotProgress", on_progress)
```

### lastSeenObjectId

Fired periodically with the last object ID and timestamp:

```python
async def on_last_seen(event):
    print(f"Last ID: {event['lastSeenObjectId']}")
    print(f"Timestamp: {event['timestamp']}")

session.HeapProfiler.on("lastSeenObjectId", on_last_seen)
```

## Heap Analysis Patterns

### Finding memory leaks

```python
import json

def find_leaks(snapshot_path):
    with open(snapshot_path) as f:
        data = json.load(f)

    # Merge all chunks
    snapshot = data[0] if isinstance(data, list) else data
    nodes = snapshot["nodes"]
    strings = snapshot["strings"]

    # Find large objects
    large_objects = []
    for i in range(0, len(nodes), 7):
        type_idx = nodes[i]
        name_idx = nodes[i + 1]
        node_id = nodes[i + 2]
        self_size = nodes[i + 3]

        type_name = strings[type_idx]
        name = strings[name_idx]

        if self_size > 10000:  # > 10KB
            large_objects.append({
                "type": type_name,
                "name": name,
                "id": node_id,
                "size": self_size
            })

    large_objects.sort(key=lambda x: -x["size"])
    for obj in large_objects[:20]:
        print(f"{obj['type']} '{obj['name']}' — {obj['size']} bytes (id={obj['id']})")
```

### Comparing snapshots

```python
def compare_snapshots(before_path, after_path):
    with open(before_path) as f:
        before = json.load(f)
    with open(after_path) as f:
        after = json.load(f)

    before_nodes = {}
    after_nodes = {}

    snapshot = before[0] if isinstance(before, list) else before
    nodes = snapshot["nodes"]
    strings = snapshot["strings"]
    for i in range(0, len(nodes), 7):
        node_id = nodes[i + 2]
        name = strings[nodes[i + 1]]
        size = nodes[i + 3]
        before_nodes[node_id] = {"name": name, "size": size}

    snapshot = after[0] if isinstance(after, list) else after
    nodes = snapshot["nodes"]
    strings = snapshot["strings"]
    for i in range(0, len(nodes), 7):
        node_id = nodes[i + 2]
        name = strings[nodes[i + 1]]
        size = nodes[i + 3]
        after_nodes[node_id] = {"name": name, "size": size}

    # Find new objects
    new_ids = set(after_nodes.keys()) - set(before_nodes.keys())
    print(f"New objects: {len(new_ids)}")
    for nid in list(new_ids)[:20]:
        print(f"  {after_nodes[nid]['name']} — {after_nodes[nid]['size']} bytes")

    # Find grown objects
    common_ids = set(before_nodes.keys()) & set(after_nodes.keys())
    grown = [(nid, after_nodes[nid]["size"] - before_nodes[nid]["size"])
             for nid in common_ids
             if after_nodes[nid]["size"] > before_nodes[nid]["size"]]
    grown.sort(key=lambda x: -x[1])
    print(f"\nGrown objects: {len(grown)}")
    for nid, delta in grown[:20]:
        print(f"  {after_nodes[nid]['name']} — +{delta} bytes")
```

## Methods Reference

| Method | Description |
|--------|-------------|
| `enable` | Enable HeapProfiler domain |
| `disable` | Disable HeapProfiler domain |
| `take_heap_snapshot` | Capture full heap snapshot |
| `start_sampling` | Start heap sampling |
| `stop_sampling` | Stop sampling and get profile |
| `start_tracking_heap_objects` | Start allocation tracking |
| `stop_tracking_heap_objects` | Stop allocation tracking |
| `get_heap_object_id` | Get heap object ID for RemoteObject |
| `get_object_by_heap_object_id` | Get RemoteObject by heap ID |
| `inspect_heap_object` | Inspect heap object |

## References

- [CDP HeapProfiler domain](https://chromedevtools.github.io/devtools-protocol/tot/HeapProfiler/)
- `references/debugger-domain.md` — Debugger domain reference
- `references/profiler-domain.md` — Profiler domain reference

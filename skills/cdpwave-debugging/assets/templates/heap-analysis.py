"""CDPWave heap analysis template.

Take before/after heap snapshots and compare them to find memory leaks.

Usage:
    python heap-analysis.py --url https://example.com --port 9222
"""

import argparse
import asyncio
import json

from cdpwave import CDPSession


async def take_snapshot(session: CDPSession, path: str) -> None:
    """Take a heap snapshot and save it to a file."""
    chunks = []
    async for chunk in session.HeapProfiler.take_heap_snapshot():
        chunks.append(chunk)
    with open(path, "w") as f:
        json.dump(chunks, f)
    print(f"Snapshot saved: {path}")


async def run_interactions(session: CDPSession, url: str) -> None:
    """Run page interactions that may cause memory leaks."""
    await session.Page.enable()
    await session.Page.navigate(url=url)
    await session.Page.wait_for_load()

    await session.Runtime.evaluate(expression="document.querySelector('#load-data').click()")
    await asyncio.sleep(2)

    await session.Runtime.evaluate(expression="document.querySelector('#clear-data').click()")
    await asyncio.sleep(1)

    for _ in range(10):
        await session.Runtime.evaluate(expression="document.querySelector('#load-data').click()")
        await asyncio.sleep(1)
        await session.Runtime.evaluate(expression="document.querySelector('#clear-data').click()")
        await asyncio.sleep(0.5)


async def heap_analysis(url: str, port: int) -> None:
    session = await CDPSession.connect(f"ws://localhost:{port}")

    await session.HeapProfiler.enable()

    print("Taking before snapshot...")
    await take_snapshot(session, "heap-before.heapsnapshot")

    print("Running interactions...")
    await run_interactions(session, url)

    print("Taking after snapshot...")
    await take_snapshot(session, "heap-after.heapsnapshot")

    await session.HeapProfiler.disable()
    await session.close()

    compare_snapshots("heap-before.heapsnapshot", "heap-after.heapsnapshot")


def parse_snapshot(path: str) -> dict:
    """Parse a heap snapshot file into a node dict keyed by node ID."""
    with open(path) as f:
        data = json.load(f)

    snapshot = data[0] if isinstance(data, list) else data
    nodes = snapshot["nodes"]
    strings = snapshot["strings"]

    node_dict = {}
    for i in range(0, len(nodes), 7):
        type_idx = nodes[i]
        name_idx = nodes[i + 1]
        node_id = nodes[i + 2]
        self_size = nodes[i + 3]

        node_dict[node_id] = {
            "type": strings[type_idx],
            "name": strings[name_idx],
            "size": self_size,
        }

    return node_dict


def compare_snapshots(before_path: str, after_path: str) -> None:
    """Compare two heap snapshots and report new/grown objects."""
    before = parse_snapshot(before_path)
    after = parse_snapshot(after_path)

    before_ids = set(before.keys())
    after_ids = set(after.keys())

    new_ids = after_ids - before_ids
    removed_ids = before_ids - after_ids
    common_ids = before_ids & after_ids

    print(f"\n{'=' * 60}")
    print(f"Heap Snapshot Comparison")
    print(f"{'=' * 60}")
    print(f"Before: {len(before_ids)} objects")
    print(f"After:  {len(after_ids)} objects")
    print(f"New:     {len(new_ids)} objects")
    print(f"Removed: {len(removed_ids)} objects")

    new_objects = [(nid, after[nid]) for nid in new_ids]
    new_objects.sort(key=lambda x: -x[1]["size"])

    print(f"\nTop 20 new objects by size:")
    for nid, obj in new_objects[:20]:
        print(f"  {obj['type']:20s} '{obj['name'][:30]:30s}' — {obj['size']:>10,} bytes")

    grown = []
    for nid in common_ids:
        delta = after[nid]["size"] - before[nid]["size"]
        if delta > 0:
            grown.append((nid, after[nid], delta))

    grown.sort(key=lambda x: -x[2])

    print(f"\nTop 20 grown objects:")
    for nid, obj, delta in grown[:20]:
        print(f"  {obj['type']:20s} '{obj['name'][:30]:30s}' — +{delta:>10,} bytes")

    total_before = sum(n["size"] for n in before.values())
    total_after = sum(n["size"] for n in after.values())
    print(f"\nTotal heap: {total_before:,} -> {total_after:,} bytes ({total_after - total_before:+,} delta)")


def main():
    parser = argparse.ArgumentParser(description="CDPWave heap analysis template")
    parser.add_argument("--url", default="https://example.com", help="URL to analyze")
    parser.add_argument("--port", type=int, default=9222, help="CDP remote debugging port")
    args = parser.parse_args()

    asyncio.run(heap_analysis(url=args.url, port=args.port))


if __name__ == "__main__":
    main()

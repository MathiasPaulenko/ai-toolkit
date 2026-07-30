"""CDPWave debug session template.

Run a complete debug session: set breakpoints, step through code,
capture CPU profile, and take a heap snapshot.

Usage:
    python debug-session.py --url https://example.com --port 9222
"""

import argparse
import asyncio
import json

from cdpwave import CDPSession


async def debug_session(url: str, port: int, breakpoint_url: str, breakpoint_line: int, condition: str | None):
    session = await CDPSession.connect(f"ws://localhost:{port}")

    await session.Debugger.enable()
    await session.Profiler.enable()
    await session.HeapProfiler.enable()
    await session.Page.enable()

    bp = await session.Debugger.set_breakpoint_by_url(
        url=breakpoint_url,
        line_number=breakpoint_line,
        condition=condition,
    )
    print(f"Breakpoint set: {bp['breakpointId']}")

    await session.Profiler.start()

    await session.Page.navigate(url=url)
    print(f"Navigated to: {url}")

    try:
        paused = await asyncio.wait_for(
            session.Debugger.wait_for_pause(),
            timeout=30,
        )
        print(f"Paused at line {paused['callFrames'][0]['location']['lineNumber']}")
        for frame in paused["callFrames"][:3]:
            print(f"  {frame['functionName']} at {frame['url']}:{frame['location']['lineNumber']}")

        await session.Debugger.step_over()
        paused = await session.Debugger.wait_for_pause()
        print(f"Step over -> line {paused['callFrames'][0]['location']['lineNumber']}")

        await session.Debugger.step_into()
        paused = await session.Debugger.wait_for_pause()
        print(f"Step into -> line {paused['callFrames'][0]['location']['lineNumber']}")

        await session.Debugger.resume()
        print("Resumed execution")
    except asyncio.TimeoutError:
        print("No breakpoint hit within timeout")

    await session.Page.wait_for_load()

    cpu_profile = await session.Profiler.stop()
    with open("cpu-profile.json", "w") as f:
        json.dump(cpu_profile, f)
    print("CPU profile saved: cpu-profile.json")

    snapshot_chunks = []
    async for chunk in session.HeapProfiler.take_heap_snapshot():
        snapshot_chunks.append(chunk)
    with open("heap.heapsnapshot", "w") as f:
        json.dump(snapshot_chunks, f)
    print("Heap snapshot saved: heap.heapsnapshot")

    await session.Debugger.remove_breakpoint(breakpoint_id=bp["breakpointId"])
    await session.Debugger.disable()
    await session.Profiler.disable()
    await session.HeapProfiler.disable()
    await session.close()
    print("Debug session complete")


def main():
    parser = argparse.ArgumentParser(description="CDPWave debug session template")
    parser.add_argument("--url", default="https://example.com", help="URL to navigate to")
    parser.add_argument("--port", type=int, default=9222, help="CDP remote debugging port")
    parser.add_argument("--bp-url", default="https://example.com/app.js", help="Breakpoint script URL")
    parser.add_argument("--bp-line", type=int, default=42, help="Breakpoint line number (0-indexed)")
    parser.add_argument("--condition", default=None, help="Conditional breakpoint expression")
    args = parser.parse_args()

    asyncio.run(debug_session(
        url=args.url,
        port=args.port,
        breakpoint_url=args.bp_url,
        breakpoint_line=args.bp_line,
        condition=args.condition,
    ))


if __name__ == "__main__":
    main()

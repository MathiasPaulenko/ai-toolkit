"""BiDiWave header modification template.

Add, remove, and modify request headers for testing.

Usage:
    python modify-headers.py --url https://example.com --port 9222
"""

import argparse
import asyncio
import os

from bidiwave import BiDiSession


async def modify_headers(url: str, port: int) -> None:
    session = await BiDiSession.connect(f"ws://localhost:{port}")

    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*"],
    )

    token = os.environ.get("TEST_API_TOKEN", "test-token-default")
    request_id_header = "test-run-001"

    modified_count = 0

    async for event in session.network.stream_intercepted_requests():
        headers = event["request"]["headers"]
        request_url = event["request"]["url"]

        if "/api/" in request_url:
            headers["Authorization"] = f"Bearer {token}"
            headers["X-Test-Environment"] = "true"
            headers["X-Request-ID"] = request_id_header

            modified_count += 1
            print(f"Modified [{modified_count}]: {request_url}")
            print(f"  Added: Authorization, X-Test-Environment, X-Request-ID")

            if "Cookie" in headers:
                del headers["Cookie"]
                print("  Removed: Cookie")

            await session.network.continue_request(
                request_id=event["requestId"],
                headers=headers,
            )
        else:
            await session.network.continue_request(
                request_id=event["requestId"],
            )

    await session.network.remove_intercept(intercept_id=intercept["interceptId"])
    await session.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="BiDiWave header modification template")
    parser.add_argument("--url", default="https://example.com", help="URL to navigate to")
    parser.add_argument("--port", type=int, default=9222, help="BiDi WebSocket port")
    args = parser.parse_args()

    asyncio.run(modify_headers(url=args.url, port=args.port))


if __name__ == "__main__":
    main()

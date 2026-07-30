"""BiDiWave API mocking template.

Mock API endpoints with custom responses for testing.

Usage:
    python mock-api.py --url https://example.com --port 9222
"""

import argparse
import asyncio
import fnmatch
import json

from bidiwave import BiDiSession

MOCK_RESPONSES = {
    "*/api/users": {
        "status": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
            ],
        }),
    },
    "*/api/products": {
        "status": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "products": [
                {"id": 1, "name": "Widget", "price": 9.99},
                {"id": 2, "name": "Gadget", "price": 19.99},
            ],
        }),
    },
    "*/api/error": {
        "status": 500,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": "Internal Server Error"}),
    },
    "*/api/notfound": {
        "status": 404,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": "Not Found"}),
    },
    "*/api/rate-limited": {
        "status": 429,
        "headers": {"Content-Type": "application/json", "Retry-After": "60"},
        "body": json.dumps({"error": "Too Many Requests"}),
    },
}


async def mock_api(url: str, port: int) -> None:
    session = await BiDiSession.connect(f"ws://localhost:{port}")

    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=["*/api/*"],
    )

    mocked_count = 0
    passed_count = 0

    async for event in session.network.stream_intercepted_requests():
        request_url = event["request"]["url"]
        matched = False

        for pattern, mock in MOCK_RESPONSES.items():
            if fnmatch.fnmatch(request_url, f"*{pattern}*"):
                mocked_count += 1
                print(f"Mock [{mocked_count}]: {mock['status']} {request_url}")

                await session.network.provide_response(
                    request_id=event["requestId"],
                    status_code=mock["status"],
                    headers=mock["headers"],
                    body=mock["body"],
                )
                matched = True
                break

        if not matched:
            passed_count += 1
            print(f"Pass [{passed_count}]: {request_url}")

            await session.network.continue_request(
                request_id=event["requestId"],
            )

    await session.network.remove_intercept(intercept_id=intercept["interceptId"])
    await session.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="BiDiWave API mocking template")
    parser.add_argument("--url", default="https://example.com", help="URL to navigate to")
    parser.add_argument("--port", type=int, default=9222, help="BiDi WebSocket port")
    args = parser.parse_args()

    asyncio.run(mock_api(url=args.url, port=args.port))


if __name__ == "__main__":
    main()

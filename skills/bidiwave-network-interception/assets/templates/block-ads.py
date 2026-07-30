"""BiDiWave ad blocking template.

Block common ad and tracking domains during a browsing session.

Usage:
    python block-ads.py --url https://example.com --port 9222
"""

import argparse
import asyncio

from bidiwave import BiDiSession

AD_DOMAINS = [
    "*/google-analytics.com/*",
    "*/googletagmanager.com/*",
    "*/doubleclick.net/*",
    "*/facebook.net/*",
    "*/facebook.com/tr*",
    "*/amazon-adsystem.com/*",
    "*/criteo.com/*",
    "*/hotjar.com/*",
    "*/segment.com/*",
    "*/mixpanel.com/*",
    "*/adservice.google.com/*",
    "*/ads.yahoo.com/*",
    "*/bing.com/ads/*",
    "*/taboola.com/*",
    "*/outbrain.com/*",
    "*/scorecardresearch.com/*",
    "*/quantserve.com/*",
    "*/adnxs.com/*",
    "*/pubmatic.com/*",
    "*/rubiconproject.com/*",
]


async def block_ads(url: str, port: int) -> None:
    session = await BiDiSession.connect(f"ws://localhost:{port}")

    intercept = await session.network.add_intercept(
        phases=["beforeRequestSent"],
        url_patterns=AD_DOMAINS,
    )

    blocked_count = 0

    async for event in session.network.stream_intercepted_requests():
        blocked_count += 1
        print(f"Blocked [{blocked_count}]: {event['request']['url']}")

        await session.network.continue_response(
            request_id=event["requestId"],
            status_code=403,
        )

    await session.network.remove_intercept(intercept_id=intercept["interceptId"])
    await session.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="BiDiWave ad blocking template")
    parser.add_argument("--url", default="https://example.com", help="URL to navigate to")
    parser.add_argument("--port", type=int, default=9222, help="BiDi WebSocket port")
    args = parser.parse_args()

    asyncio.run(block_ads(url=args.url, port=args.port))


if __name__ == "__main__":
    main()

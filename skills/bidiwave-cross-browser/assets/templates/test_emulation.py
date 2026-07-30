"""Emulation test template for bidiwave with pytest-asyncio."""

import pytest
from bidiwave import BiDiClient, ViewportSize, StringValue


@pytest.mark.asyncio
async def test_viewport():
    """Set a mobile viewport and verify dimensions."""
    async with await BiDiClient.connect("ws://localhost:9515/session") as client:
        async with await client.browsing.open("https://example.com") as page:
            await client.browsing.set_viewport(
                page.id,
                viewport=ViewportSize(width=375, height=812),
                device_pixel_ratio=3.0,
            )
            result = await page.evaluate("window.innerWidth")
            match result:
                case StringValue(value=width):
                    assert int(width) == 375


@pytest.mark.asyncio
async def test_geolocation():
    """Override geolocation and grant permission."""
    async with await BiDiClient.connect("ws://localhost:9515/session") as client:
        async with await client.browsing.open("https://example.com") as page:
            ctx = page.id

            await client.permissions.set_permission(
                descriptor={"name": "geolocation"},
                state="granted",
                contexts=[ctx],
            )

            await client.emulation.set_geolocation_override(
                coordinates={
                    "latitude": 35.6762,
                    "longitude": 139.6503,
                    "accuracy": 1.0,
                },
                contexts=[ctx],
            )


@pytest.mark.asyncio
async def test_user_agent_override():
    """Override user agent string."""
    async with await BiDiClient.connect("ws://localhost:9515/session") as client:
        async with await client.browsing.open("https://example.com") as page:
            await client.emulation.set_user_agent_override(
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
                contexts=[page.id],
            )
            result = await page.evaluate("navigator.userAgent")
            match result:
                case StringValue(value=ua):
                    assert "iPhone" in ua


@pytest.mark.asyncio
async def test_timezone_override():
    """Override timezone."""
    async with await BiDiClient.connect("ws://localhost:9515/session") as client:
        async with await client.browsing.open("https://example.com") as page:
            await client.emulation.set_timezone_override(
                timezone="Asia/Tokyo",
                contexts=[page.id],
            )
            result = await page.evaluate("Intl.DateTimeFormat().resolvedOptions().timeZone")
            match result:
                case StringValue(value=tz):
                    assert tz == "Asia/Tokyo"

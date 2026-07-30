"""Screenshot test template for cdpwave with pytest-asyncio."""

import pytest
from cdpwave import CDPClient


@pytest.mark.asyncio
async def test_screenshot():
    """Take a screenshot and verify it's a valid PNG."""
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.wait_for_event("Page.loadEventFired")

        screenshot = await session.page.capture_screenshot()
        assert screenshot["data"], "Screenshot data should not be empty"

        # Save to file
        with open("screenshot.png", "wb") as f:
            f.write(bytes.fromhex(screenshot["data"]))

        await session.close()


@pytest.mark.asyncio
async def test_full_page_screenshot():
    """Take a full-page screenshot."""
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.wait_for_event("Page.loadEventFired")

        screenshot = await session.page.capture_screenshot(
            capture_beyond_viewport=True,
        )
        assert screenshot["data"]

        with open("full_page.png", "wb") as f:
            f.write(bytes.fromhex(screenshot["data"]))

        await session.close()


@pytest.mark.asyncio
async def test_screenshot_region():
    """Take a screenshot of a specific region."""
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("https://example.com")
        await session.wait_for_event("Page.loadEventFired")

        screenshot = await session.page.capture_screenshot(
            clip={
                "x": 0,
                "y": 0,
                "width": 400,
                "height": 300,
                "scale": 1,
            },
        )
        assert screenshot["data"]

        with open("region.png", "wb") as f:
            f.write(bytes.fromhex(screenshot["data"]))

        await session.close()

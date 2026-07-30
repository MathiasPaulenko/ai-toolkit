"""Cross-browser test template for bidiwave with pytest-asyncio."""

import pytest
from bidiwave import BiDiClient, StringValue

ENDPOINTS = {
    "chrome": "ws://localhost:9515/session",
    "firefox": "ws://localhost:9223/session",
    "edge": "ws://localhost:9516/session",
}


@pytest.mark.parametrize("browser", list(ENDPOINTS.keys()))
@pytest.mark.asyncio
async def test_page_title(browser):
    """Verify page title across all browsers."""
    url = ENDPOINTS[browser]
    async with await BiDiClient.connect(url) as client:
        async with await client.browsing.open("https://example.com") as page:
            result = await page.evaluate("document.title")
            match result:
                case StringValue(value=title):
                    assert title == "Example Domain"
                case _:
                    pytest.fail(f"Unexpected RemoteValue type: {type(result)}")


@pytest.mark.parametrize("browser", list(ENDPOINTS.keys()))
@pytest.mark.asyncio
async def test_screenshot(browser):
    """Take a screenshot in each browser."""
    url = ENDPOINTS[browser]
    async with await BiDiClient.connect(url) as client:
        async with await client.browsing.open("https://example.com") as page:
            screenshot = await page.screenshot()
            assert screenshot
            with open(f"screenshot_{browser}.png", "wb") as f:
                f.write(screenshot)


@pytest.mark.parametrize("browser", list(ENDPOINTS.keys()))
@pytest.mark.asyncio
async def test_navigation(browser):
    """Test navigation and history traversal."""
    url = ENDPOINTS[browser]
    async with await BiDiClient.connect(url) as client:
        async with await client.browsing.open("https://example.com") as page:
            await page.navigate("https://example.org")
            result = await page.evaluate("document.title")
            match result:
                case StringValue(value=title):
                    assert "IANA" in title

            await page.traverse_history("back")
            result = await page.evaluate("document.title")
            match result:
                case StringValue(value=title):
                    assert title == "Example Domain"

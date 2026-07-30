"""Multi-tab test template for cdpwave with pytest-asyncio."""

import asyncio

import pytest
from cdpwave import CDPClient


@pytest.mark.asyncio
async def test_multi_tab_titles():
    """Open multiple tabs and verify each has the correct title."""
    async with await CDPClient.launch(headless=True) as client:
        tab1 = await client.new_page("https://example.com")
        tab2 = await client.new_page("https://example.org")

        await tab1.wait_for_event("Page.loadEventFired")
        await tab2.wait_for_event("Page.loadEventFired")

        result1 = await tab1.runtime.evaluate("document.title", return_by_value=True)
        result2 = await tab2.runtime.evaluate("document.title", return_by_value=True)

        assert result1["result"]["value"] == "Example Domain"
        assert result2["result"]["value"] == "IANA-managed domains"

        await tab1.close()
        await tab2.close()


@pytest.mark.asyncio
async def test_multi_tab_concurrent_eval():
    """Run evaluations concurrently across multiple tabs."""
    async with await CDPClient.launch(headless=True) as client:
        tabs = []
        urls = [
            "https://example.com",
            "https://example.org",
            "https://example.net",
        ]

        for url in urls:
            tab = await client.new_page(url)
            tabs.append(tab)

        # Wait for all tabs to load
        await asyncio.gather(*[tab.wait_for_event("Page.loadEventFired") for tab in tabs])

        # Evaluate concurrently
        results = await asyncio.gather(
            *[tab.runtime.evaluate("document.title", return_by_value=True) for tab in tabs]
        )

        titles = [r["result"]["value"] for r in results]
        assert len(titles) == 3
        assert all(titles), "All titles should be non-empty"

        for tab in tabs:
            await tab.close()


@pytest.mark.asyncio
async def test_session_tracking():
    """Verify client.sessions tracks all active sessions."""
    async with await CDPClient.launch(headless=True) as client:
        tab1 = await client.new_page("https://example.com")
        tab2 = await client.new_page("https://example.org")

        assert len(client.sessions) >= 2

        await tab1.close()
        await tab2.close()

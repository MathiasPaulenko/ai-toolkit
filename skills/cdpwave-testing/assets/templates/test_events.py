"""Event handling test template for cdpwave with pytest-asyncio."""

import pytest
from cdpwave import CDPClient


@pytest.mark.asyncio
async def test_page_load_event():
    """Verify Page.loadEventFired fires after navigation."""
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("about:blank")
        await session.page.enable()

        await session.page.navigate("https://example.com")
        await session.wait_for_event("Page.loadEventFired")

        result = await session.runtime.evaluate("document.title", return_by_value=True)
        assert result["result"]["value"] == "Example Domain"

        await session.close()


@pytest.mark.asyncio
async def test_console_events():
    """Capture console messages via Runtime.consoleAPICalled."""
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("about:blank")
        await session.runtime.enable()

        console_messages = []
        session.on("Runtime.consoleAPICalled", lambda msg: console_messages.append(msg))

        await session.runtime.evaluate("console.log('test message')")
        await session.runtime.evaluate("console.warn('warning message')")

        # Allow events to propagate
        import asyncio
        await asyncio.sleep(0.1)

        assert len(console_messages) >= 2
        assert any("test message" in str(m.get("args", "")) for m in console_messages)

        await session.close()


@pytest.mark.asyncio
async def test_network_events():
    """Capture network request and response events."""
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("about:blank")
        await session.network.enable()

        requests = []
        responses = []

        session.on("Network.requestWillBeSent", lambda e: requests.append(e))
        session.on("Network.responseReceived", lambda e: responses.append(e))

        await session.page.navigate("https://example.com")
        await session.wait_for_event("Page.loadEventFired")

        assert len(requests) > 0, "Should have captured at least one request"
        assert len(responses) > 0, "Should have captured at least one response"

        # Verify the main request
        main_request = requests[0]
        assert "example.com" in main_request["request"]["url"]

        await session.close()


@pytest.mark.asyncio
async def test_exception_event():
    """Capture JavaScript exceptions via Runtime.exceptionThrown."""
    async with await CDPClient.launch(headless=True) as client:
        session = await client.new_page("about:blank")
        await session.runtime.enable()

        exceptions = []
        session.on("Runtime.exceptionThrown", lambda e: exceptions.append(e))

        await session.runtime.evaluate("undefinedVariable.foo")

        import asyncio
        await asyncio.sleep(0.1)

        assert len(exceptions) == 1
        assert "undefinedVariable" in exceptions[0]["exceptionDetails"]["text"]

        await session.close()

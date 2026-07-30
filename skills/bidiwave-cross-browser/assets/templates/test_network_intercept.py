"""Network interception test template for bidiwave with pytest-asyncio."""

import asyncio

import pytest
from bidiwave import BiDiClient, StringValue


@pytest.mark.asyncio
async def test_block_requests():
    """Block requests to a specific domain."""
    async with await BiDiClient.connect("ws://localhost:9515/session") as client:
        intercept = await client.network.add_intercept(
            phases=["beforeRequestSent"],
            url_patterns=["*ads.example.com*"],
        )

        async with await client.browsing.open("https://example.com") as page:
            await asyncio.sleep(2)
            result = await page.evaluate("document.title")
            match result:
                case StringValue(value=title):
                    assert title == "Example Domain"

        await client.network.remove_intercept(intercept.intercept_id)


@pytest.mark.asyncio
async def test_mock_response():
    """Mock an API response."""
    async with await BiDiClient.connect("ws://localhost:9515/session") as client:
        intercept = await client.network.add_intercept(
            phases=["responseStarted"],
            url_patterns=["*api.example.com/data*"],
        )

        async with await client.browsing.open("https://example.com") as page:
            await client.network.provide_response(
                intercept_id=intercept.intercept_id,
                status_code=200,
                headers={"Content-Type": "application/json"},
                body='{"mocked": true}',
            )
            await asyncio.sleep(2)

        await client.network.remove_intercept(intercept.intercept_id)


@pytest.mark.asyncio
async def test_extra_headers():
    """Set extra HTTP headers on all requests."""
    async with await BiDiClient.connect("ws://localhost:9515/session") as client:
        async with await client.browsing.open("https://example.com") as page:
            await client.network.set_extra_headers(
                headers={"X-Test-Header": "bidiwave-test"},
                contexts=[page.id],
            )
            await page.navigate("https://example.com")
            result = await page.evaluate("document.title")
            match result:
                case StringValue(value=title):
                    assert title == "Example Domain"

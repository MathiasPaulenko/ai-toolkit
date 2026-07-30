"""pytest-asyncio fixtures for bidiwave cross-browser testing."""

import pytest
from bidiwave import BiDiClient

DEFAULT_ENDPOINT = "ws://localhost:9515/session"


@pytest.fixture
async def client():
    """Connect to a BiDi endpoint for the test session."""
    async with await BiDiClient.connect(DEFAULT_ENDPOINT) as client:
        yield client


@pytest.fixture
async def page(client):
    """Open a browsing context for each test."""
    async with await client.browsing.open("https://example.com") as page:
        yield page


@pytest.fixture
async def blank_page(client):
    """Open a blank page for tests that navigate manually."""
    async with await client.browsing.open("about:blank") as page:
        yield page


@pytest.fixture(scope="session")
async def shared_client():
    """Shared BiDi connection across all tests in the session."""
    client = await BiDiClient.connect(
        DEFAULT_ENDPOINT,
        reconnect=True,
        max_retries=5,
        backoff_base=0.5,
    )
    yield client
    await client.close()


@pytest.fixture
async def isolated_page(shared_client):
    """Isolated browsing context per test using a shared connection."""
    async with await shared_client.browsing.open("about:blank") as page:
        yield page

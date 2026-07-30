"""pytest-asyncio fixtures for cdpwave browser testing."""

import pytest
from cdpwave import CDPClient


@pytest.fixture
async def client():
    """Launch a headless browser for the test session."""
    async with await CDPClient.launch(
        headless=True,
        extra_args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
    ) as client:
        yield client


@pytest.fixture
async def session(client):
    """Create a new page session for each test."""
    session = await client.new_page("about:blank")
    yield session
    await session.close()


@pytest.fixture
async def example_page(session):
    """Navigate to example.com and wait for load."""
    await session.page.enable()
    await session.page.navigate("https://example.com")
    await session.wait_for_event("Page.loadEventFired")
    yield session


@pytest.fixture(scope="session")
async def shared_client():
    """Shared browser instance across all tests in the session."""
    client = await CDPClient.launch(
        headless=True,
        extra_args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
    )
    yield client
    await client.close()


@pytest.fixture
async def isolated_session(shared_client):
    """Isolated tab per test using a shared browser instance."""
    session = await shared_client.new_page("about:blank")
    yield session
    await session.close()

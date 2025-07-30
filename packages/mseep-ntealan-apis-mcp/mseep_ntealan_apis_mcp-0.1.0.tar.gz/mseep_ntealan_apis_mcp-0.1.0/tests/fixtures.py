import asyncio

import pytest
from fastmcp import Client
from fastmcp.client.transports import SSETransport


@pytest.fixture(scope="session")
def event_loop():
    """
    Create an instance of the default event loop for the session.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def sse_client():
    """
    Fixture for an SSE client connected to the running MCP server.
    """
    sse_url = "http://127.0.0.1:8000/sse"
    headers = {"Authorization": "Bearer mytoken"}
    client = Client(SSETransport(url=sse_url, headers=headers))
    return client

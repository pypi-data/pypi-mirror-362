import pytest


@pytest.mark.asyncio
async def test_list_tools(sse_client):
    """
    Test listing all available tools from the MCP server.
    """
    async with sse_client:
        assert sse_client.is_connected()
        tools = await sse_client.list_tools()
        assert isinstance(tools, list)


@pytest.mark.asyncio
async def test_list_resources(sse_client):
    """
    Test listing all available resources from the MCP server.
    """
    async with sse_client:
        assert sse_client.is_connected()
        resources = await sse_client.list_resources()
        assert isinstance(resources, list)


@pytest.mark.asyncio
async def test_list_resource_templates(sse_client):
    """
    Test listing all available resource templates from the MCP server.
    """
    async with sse_client:
        assert sse_client.is_connected()
        resources = await sse_client.get_resource_templates()
        assert isinstance(resources, list)

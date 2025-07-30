from json import loads as json_loads

import pytest
from mcp.types import TextResourceContents

# Test tool -- Dictionary metadata calls (TO COMPLETE LATER) --
# Thiw will need NTeALan API token: get it from NTeALan API admin

# @pytest.mark.asyncio
# async def test_create_dictionary_tool(sse_client):
#     """
#     Test creating a new dictionary.
#     """
#     async with sse_client:
#         assert sse_client.is_connected()
#         payload = {
#             "data": {
#                 "name": "Test Dictionary",
#                 "description": "A test dictionary",
#                 "created_at": "2023-01-01T00:00:00Z",
#                 "updated_at": "2023-01-01T00:00:00Z"
#             }
#         }
#         result = await sse_client.call_tool("create_dictionary", payload)
#         assert type(result) is list

# @pytest.mark.asyncio
# async def test_update_dictionary_tool(sse_client):
#     """
#     Test updating an existing dictionary.
#     """
#     async with sse_client:
#         assert sse_client.is_connected()
#         payload = {
#             "dictionary_id": "yb_fr_3031",
#             "data": {
#                 "name": "Updated Dictionary",
#                 "description": "Updated description"
#             }
#         }
#         result = await sse_client.call_tool("update_dictionary", payload)
#         assert type(result) is list

# @pytest.mark.asyncio
# async def test_delete_dictionary_tool(sse_client):
#     """
#     Test deleting a dictionary.
#     """
#     async with sse_client:
#         assert sse_client.is_connected()
#         payload = {"dictionary_id": "yb_fr_3031"}
#         result = await sse_client.call_tool("delete_dictionary", payload)
#         assert type(result) is list


# Test resource -- Dictionary metadata --


@pytest.mark.asyncio
async def test_read_all_dictionaries_with_limit(sse_client):
    """
    Test reading all dictionaries with a limit parameter.
    """
    async with sse_client:
        assert sse_client.is_connected()
        uri = "ntealan-apis://dictionaries?limit=2"
        result = await sse_client.read_resource(uri)
        assert isinstance(result[0], TextResourceContents)
        assert "status" in result[0].text
        assert json_loads(result[0].text).get("status") == "OK"


@pytest.mark.asyncio
async def test_read_dictionaries_statistics_by_id(sse_client):
    """
    Test reading dictionaries statistics for a specific dictionary.
    """
    async with sse_client:
        assert sse_client.is_connected()
        uri = "ntealan-apis://dictionaries/statistics/yb_fr_3031"
        result = await sse_client.read_resource(uri)
        assert isinstance(result[0], TextResourceContents)
        assert "status" in result[0].text
        assert json_loads(result[0].text).get("status") == "OK"


@pytest.mark.asyncio
async def test_read_dictionaries_statistics(sse_client):
    """
    Test reading statistics for all dictionaries.
    """
    async with sse_client:
        assert sse_client.is_connected()
        uri = "ntealan-apis://dictionaries/statistics"
        result = await sse_client.read_resource(uri)
        assert isinstance(result[0], TextResourceContents)
        assert "status" in result[0].text
        assert json_loads(result[0].text).get("status") == "OK"

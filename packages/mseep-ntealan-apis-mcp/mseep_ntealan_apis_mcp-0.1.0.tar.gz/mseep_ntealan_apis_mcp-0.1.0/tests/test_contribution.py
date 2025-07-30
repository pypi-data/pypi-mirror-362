from json import loads as json_loads

import pytest
from mcp.types import TextResourceContents

# Test tool -- Contribution calls (TO COMPLETE LATER) --
# This will need NTeALan API token: get it from NTeALan API admin


# @pytest.mark.asyncio
# async def test_create_contribution_tool(sse_client):
#     """
#     Test creating a new contribution.
#     """
#     async with sse_client:
#         assert sse_client.is_connected()
#         payload = {
#             "dictionary_id": "yb_fr_3031",
#             "article_id": "0facf001-cb58-42c5-82b8-cd2dd2099967",
#             "data": {
#                 "user_id": 1,
#                 "content": "Contribution content"
#             }
#         }
#         result = await sse_client.call_tool("create_contribution", payload)
#         assert type(result) is list

# @pytest.mark.asyncio
# async def test_update_contribution_tool(sse_client):
#     """
#     Test updating a contribution.
#     """
#     async with sse_client:
#         assert sse_client.is_connected()
#         payload = {
#             "dictionary_id": "yb_fr_3031",
#             "article_id": "0facf001-cb58-42c5-82b8-cd2dd2099967",
#             "contribution_id": "0facf002-ce28-4215-82b8-ad2dd2099967",
#             "data": {
#                 "content": "Updated contribution content"
#             }
#         }
#         result = await sse_client.call_tool("update_contribution", payload)
#         assert type(result) is list

# @pytest.mark.asyncio
# async def test_delete_contribution_tool(sse_client):
#     """
#     Test deleting a contribution.
#     """
#     async with sse_client:
#         assert sse_client.is_connected()
#         payload = {
#             "dictionary_id": "yb_fr_3031",
#             "article_id": "0facf001-cb58-42c5-82b8-cd2dd2099967",
#             "contribution_id": "0facf002-ce28-4215-82b8-ad2dd2099967"
#         }
#         result = await sse_client.call_tool("delete_contribution", payload)
#         assert type(result) is list

# Test resource -- Contribution resource --


@pytest.mark.asyncio
async def test_read_contribution_resource(sse_client):
    """
    Test reading a contribution resource by URI.
    """
    async with sse_client:
        assert sse_client.is_connected()
        # Replace with a valid dictionary_id and contribution_id for your test data
        uri = "ntealan-apis://contributions/yb_fr_3031/0facf001-cb58-42c5-82b8-cd2dd2099967"
        result = await sse_client.read_resource(uri)
        assert isinstance(result[0], TextResourceContents)
        assert "status" in result[0].text
        assert json_loads(result[0].text).get("status") == "OK"

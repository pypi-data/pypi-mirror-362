from json import loads as json_loads

import pytest
from mcp.types import TextResourceContents

# Test tools -- Article calls (TO COMPLETE LATER) --
# Thiw will need NTeALan API token: get it from NTeALan API admin

# @pytest.mark.asyncio
# async def test_create_article_tool(sse_client):
#     """
#     Test creating a new article.
#     """
#     async with sse_client:
#         assert sse_client.is_connected()
#         payload = {
#             "dictionary_id": "yb_fr_3031",
#             "data": {
#                 "title": "Test Article",
#                 "content": "This is a test article."
#             }
#         }
#         result = await sse_client.call_tool("create_article", payload)
#         assert type(result) is list

# @pytest.mark.asyncio
# async def test_update_article_tool(sse_client):
#     """
#     Test updating an article.
#     """
#     async with sse_client:
#         assert sse_client.is_connected()
#         payload = {
#             "dictionary_id": "yb_fr_3031",
#             "article_id": "0facf001-cb58-42c5-82b8-cd2dd2099967",
#             "data": {
#                 "title": "Updated Article",
#                 "content": "Updated content."
#             }
#         }
#         result = await sse_client.call_tool("update_article", payload)
#         assert type(result) is list

# @pytest.mark.asyncio
# async def test_delete_article_tool(sse_client):
#     """
#     Test deleting an article.
#     """
#     async with sse_client:
#         assert sse_client.is_connected()
#         payload = {
#             "dictionary_id": "yb_fr_3031",
#             "article_id": "0facf001-cb58-42c5-82b8-cd2dd2099967"
#         }
#         result = await sse_client.call_tool("delete_article", payload)
#         assert type(result) is list

# Test resource -- Article resource calls --


@pytest.mark.asyncio
async def test_read_article_resource(sse_client):
    """
    Test reading an article resource by URI.
    """
    async with sse_client:
        assert sse_client.is_connected()
        # Replace with a valid dictionary_id and article_id for your test data
        uri = "ntealan-apis://articles/yb_fr_3031/0facf001-cb58-42c5-82b8-cd2dd2099967?none"
        result = await sse_client.read_resource(uri)
        assert isinstance(result[0], TextResourceContents)
        assert "status" in result[0].text
        assert json_loads(result[0].text).get("status") == "OK"


@pytest.mark.asyncio
async def test_read_articles_with_limit(sse_client):
    """
    Test reading all articles with a limit parameter.
    """
    async with sse_client:
        assert sse_client.is_connected()
        uri = "ntealan-apis://articles?limit=2"
        result = await sse_client.read_resource(uri)
        assert isinstance(result[0], TextResourceContents)
        assert "status" in result[0].text
        assert json_loads(result[0].text).get("status") == "OK"


@pytest.mark.asyncio
async def test_read_articles_by_dictionary_id(sse_client):
    """
    Test reading all articles for a specific dictionary.
    """
    async with sse_client:
        assert sse_client.is_connected()
        uri = "ntealan-apis://articles/yb_fr_3031?limit=2"
        result = await sse_client.read_resource(uri)
        assert isinstance(result[0], TextResourceContents)
        assert "status" in result[0].text
        assert json_loads(result[0].text).get("status") == "OK"


@pytest.mark.asyncio
async def test_read_articles_statistics_by_dictionary(sse_client):
    """
    Test reading articles statistics for a specific dictionary.
    """
    async with sse_client:
        assert sse_client.is_connected()
        uri = "ntealan-apis://articles/statistics/yb_fr_3031"
        result = await sse_client.read_resource(uri)
        assert isinstance(result[0], TextResourceContents)
        assert "status" in result[0].text
        assert json_loads(result[0].text).get("status") == "OK"


@pytest.mark.asyncio
async def test_read_articles_statistics(sse_client):
    """
    Test reading articles statistics resource.
    """
    async with sse_client:
        assert sse_client.is_connected()
        uri = "ntealan-apis://articles/statistics"
        result = await sse_client.read_resource(uri)
        assert isinstance(result[0], TextResourceContents)
        assert "status" in result[0].text
        assert json_loads(result[0].text).get("status") == "OK"

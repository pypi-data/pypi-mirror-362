# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from metis import Metis, AsyncMetis
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOAuth:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_handle_callback(self, client: Metis) -> None:
        oauth = client.mcp.oauth.handle_callback()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_handle_callback(self, client: Metis) -> None:
        response = client.mcp.oauth.with_raw_response.handle_callback()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_handle_callback(self, client: Metis) -> None:
        with client.mcp.oauth.with_streaming_response.handle_callback() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncOAuth:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_handle_callback(self, async_client: AsyncMetis) -> None:
        oauth = await async_client.mcp.oauth.handle_callback()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_handle_callback(self, async_client: AsyncMetis) -> None:
        response = await async_client.mcp.oauth.with_raw_response.handle_callback()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = await response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_handle_callback(self, async_client: AsyncMetis) -> None:
        async with async_client.mcp.oauth.with_streaming_response.handle_callback() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = await response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

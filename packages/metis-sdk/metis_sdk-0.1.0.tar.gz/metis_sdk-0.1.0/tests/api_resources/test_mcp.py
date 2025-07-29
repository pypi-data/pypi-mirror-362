# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from metis import Metis, AsyncMetis
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMcp:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_debug_info(self, client: Metis) -> None:
        mcp = client.mcp.get_debug_info(
            "session_id",
        )
        assert_matches_type(object, mcp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_debug_info(self, client: Metis) -> None:
        response = client.mcp.with_raw_response.get_debug_info(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp = response.parse()
        assert_matches_type(object, mcp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_debug_info(self, client: Metis) -> None:
        with client.mcp.with_streaming_response.get_debug_info(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp = response.parse()
            assert_matches_type(object, mcp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_debug_info(self, client: Metis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.mcp.with_raw_response.get_debug_info(
                "",
            )


class TestAsyncMcp:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_debug_info(self, async_client: AsyncMetis) -> None:
        mcp = await async_client.mcp.get_debug_info(
            "session_id",
        )
        assert_matches_type(object, mcp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_debug_info(self, async_client: AsyncMetis) -> None:
        response = await async_client.mcp.with_raw_response.get_debug_info(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mcp = await response.parse()
        assert_matches_type(object, mcp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_debug_info(self, async_client: AsyncMetis) -> None:
        async with async_client.mcp.with_streaming_response.get_debug_info(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mcp = await response.parse()
            assert_matches_type(object, mcp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_debug_info(self, async_client: AsyncMetis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.mcp.with_raw_response.get_debug_info(
                "",
            )

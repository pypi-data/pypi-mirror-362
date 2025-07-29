# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from metis import Metis, AsyncMetis
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestReconnect:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_reconnect(self, client: Metis) -> None:
        reconnect = client.reconnect.reconnect()
        assert_matches_type(object, reconnect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_reconnect(self, client: Metis) -> None:
        response = client.reconnect.with_raw_response.reconnect()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        reconnect = response.parse()
        assert_matches_type(object, reconnect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_reconnect(self, client: Metis) -> None:
        with client.reconnect.with_streaming_response.reconnect() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            reconnect = response.parse()
            assert_matches_type(object, reconnect, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncReconnect:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_reconnect(self, async_client: AsyncMetis) -> None:
        reconnect = await async_client.reconnect.reconnect()
        assert_matches_type(object, reconnect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_reconnect(self, async_client: AsyncMetis) -> None:
        response = await async_client.reconnect.with_raw_response.reconnect()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        reconnect = await response.parse()
        assert_matches_type(object, reconnect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_reconnect(self, async_client: AsyncMetis) -> None:
        async with async_client.reconnect.with_streaming_response.reconnect() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            reconnect = await response.parse()
            assert_matches_type(object, reconnect, path=["response"])

        assert cast(Any, response.is_closed) is True

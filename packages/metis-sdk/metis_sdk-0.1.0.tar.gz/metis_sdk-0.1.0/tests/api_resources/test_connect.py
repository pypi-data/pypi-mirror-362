# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from metis import Metis, AsyncMetis
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestConnect:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_initialize(self, client: Metis) -> None:
        connect = client.connect.initialize()
        assert_matches_type(object, connect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_initialize(self, client: Metis) -> None:
        response = client.connect.with_raw_response.initialize()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connect = response.parse()
        assert_matches_type(object, connect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_initialize(self, client: Metis) -> None:
        with client.connect.with_streaming_response.initialize() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connect = response.parse()
            assert_matches_type(object, connect, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncConnect:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_initialize(self, async_client: AsyncMetis) -> None:
        connect = await async_client.connect.initialize()
        assert_matches_type(object, connect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_initialize(self, async_client: AsyncMetis) -> None:
        response = await async_client.connect.with_raw_response.initialize()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        connect = await response.parse()
        assert_matches_type(object, connect, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_initialize(self, async_client: AsyncMetis) -> None:
        async with async_client.connect.with_streaming_response.initialize() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            connect = await response.parse()
            assert_matches_type(object, connect, path=["response"])

        assert cast(Any, response.is_closed) is True

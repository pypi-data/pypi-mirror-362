# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from metis import Metis, AsyncMetis
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTest:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_post_message(self, client: Metis) -> None:
        test = client.test.post_message()
        assert_matches_type(object, test, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_post_message(self, client: Metis) -> None:
        response = client.test.with_raw_response.post_message()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test = response.parse()
        assert_matches_type(object, test, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_post_message(self, client: Metis) -> None:
        with client.test.with_streaming_response.post_message() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test = response.parse()
            assert_matches_type(object, test, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTest:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_post_message(self, async_client: AsyncMetis) -> None:
        test = await async_client.test.post_message()
        assert_matches_type(object, test, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_post_message(self, async_client: AsyncMetis) -> None:
        response = await async_client.test.with_raw_response.post_message()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        test = await response.parse()
        assert_matches_type(object, test, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_post_message(self, async_client: AsyncMetis) -> None:
        async with async_client.test.with_streaming_response.post_message() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            test = await response.parse()
            assert_matches_type(object, test, path=["response"])

        assert cast(Any, response.is_closed) is True

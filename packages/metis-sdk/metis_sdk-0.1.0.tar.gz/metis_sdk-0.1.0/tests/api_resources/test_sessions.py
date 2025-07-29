# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from metis import Metis, AsyncMetis
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSessions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_tools(self, client: Metis) -> None:
        session = client.sessions.list_tools(
            "session_id",
        )
        assert_matches_type(object, session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_tools(self, client: Metis) -> None:
        response = client.sessions.with_raw_response.list_tools(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(object, session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_tools(self, client: Metis) -> None:
        with client.sessions.with_streaming_response.list_tools(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(object, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list_tools(self, client: Metis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.list_tools(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_send_message(self, client: Metis) -> None:
        session = client.sessions.send_message(
            "session_id",
        )
        assert_matches_type(object, session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_send_message(self, client: Metis) -> None:
        response = client.sessions.with_raw_response.send_message(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(object, session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_send_message(self, client: Metis) -> None:
        with client.sessions.with_streaming_response.send_message(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(object, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_send_message(self, client: Metis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.send_message(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_stream_response(self, client: Metis) -> None:
        session = client.sessions.stream_response(
            "session_id",
        )
        assert_matches_type(object, session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_stream_response(self, client: Metis) -> None:
        response = client.sessions.with_raw_response.stream_response(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(object, session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_stream_response(self, client: Metis) -> None:
        with client.sessions.with_streaming_response.stream_response(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(object, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_stream_response(self, client: Metis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.stream_response(
                "",
            )


class TestAsyncSessions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_tools(self, async_client: AsyncMetis) -> None:
        session = await async_client.sessions.list_tools(
            "session_id",
        )
        assert_matches_type(object, session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_tools(self, async_client: AsyncMetis) -> None:
        response = await async_client.sessions.with_raw_response.list_tools(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(object, session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_tools(self, async_client: AsyncMetis) -> None:
        async with async_client.sessions.with_streaming_response.list_tools(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(object, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list_tools(self, async_client: AsyncMetis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.list_tools(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_send_message(self, async_client: AsyncMetis) -> None:
        session = await async_client.sessions.send_message(
            "session_id",
        )
        assert_matches_type(object, session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_send_message(self, async_client: AsyncMetis) -> None:
        response = await async_client.sessions.with_raw_response.send_message(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(object, session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_send_message(self, async_client: AsyncMetis) -> None:
        async with async_client.sessions.with_streaming_response.send_message(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(object, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_send_message(self, async_client: AsyncMetis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.send_message(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_stream_response(self, async_client: AsyncMetis) -> None:
        session = await async_client.sessions.stream_response(
            "session_id",
        )
        assert_matches_type(object, session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_stream_response(self, async_client: AsyncMetis) -> None:
        response = await async_client.sessions.with_raw_response.stream_response(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(object, session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_stream_response(self, async_client: AsyncMetis) -> None:
        async with async_client.sessions.with_streaming_response.stream_response(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(object, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_stream_response(self, async_client: AsyncMetis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.stream_response(
                "",
            )

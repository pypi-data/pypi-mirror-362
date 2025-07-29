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
    def test_method_cleanup_session(self, client: Metis) -> None:
        oauth = client.oauth.cleanup_session(
            "session_id",
        )
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_cleanup_session(self, client: Metis) -> None:
        response = client.oauth.with_raw_response.cleanup_session(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_cleanup_session(self, client: Metis) -> None:
        with client.oauth.with_streaming_response.cleanup_session(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_cleanup_session(self, client: Metis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.oauth.with_raw_response.cleanup_session(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_auth_header(self, client: Metis) -> None:
        oauth = client.oauth.get_auth_header(
            provider="provider",
            session_id="session_id",
        )
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_auth_header(self, client: Metis) -> None:
        response = client.oauth.with_raw_response.get_auth_header(
            provider="provider",
            session_id="session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_auth_header(self, client: Metis) -> None:
        with client.oauth.with_streaming_response.get_auth_header(
            provider="provider",
            session_id="session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_auth_header(self, client: Metis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.oauth.with_raw_response.get_auth_header(
                provider="provider",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider` but received ''"):
            client.oauth.with_raw_response.get_auth_header(
                provider="",
                session_id="session_id",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_handle_callback(self, client: Metis) -> None:
        oauth = client.oauth.handle_callback(
            code="code",
            state="state",
        )
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_handle_callback_with_all_params(self, client: Metis) -> None:
        oauth = client.oauth.handle_callback(
            code="code",
            state="state",
            error="error",
        )
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_handle_callback(self, client: Metis) -> None:
        response = client.oauth.with_raw_response.handle_callback(
            code="code",
            state="state",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_handle_callback(self, client: Metis) -> None:
        with client.oauth.with_streaming_response.handle_callback(
            code="code",
            state="state",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_initiate(self, client: Metis) -> None:
        oauth = client.oauth.initiate(
            body={"foo": "bar"},
        )
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_initiate(self, client: Metis) -> None:
        response = client.oauth.with_raw_response.initiate(
            body={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_initiate(self, client: Metis) -> None:
        with client.oauth.with_streaming_response.initiate(
            body={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_status(self, client: Metis) -> None:
        oauth = client.oauth.retrieve_status(
            "session_id",
        )
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_status(self, client: Metis) -> None:
        response = client.oauth.with_raw_response.retrieve_status(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_status(self, client: Metis) -> None:
        with client.oauth.with_streaming_response.retrieve_status(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_status(self, client: Metis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.oauth.with_raw_response.retrieve_status(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_test_config(self, client: Metis) -> None:
        oauth = client.oauth.test_config()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_test_config(self, client: Metis) -> None:
        response = client.oauth.with_raw_response.test_config()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_test_config(self, client: Metis) -> None:
        with client.oauth.with_streaming_response.test_config() as response:
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
    async def test_method_cleanup_session(self, async_client: AsyncMetis) -> None:
        oauth = await async_client.oauth.cleanup_session(
            "session_id",
        )
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_cleanup_session(self, async_client: AsyncMetis) -> None:
        response = await async_client.oauth.with_raw_response.cleanup_session(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = await response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_cleanup_session(self, async_client: AsyncMetis) -> None:
        async with async_client.oauth.with_streaming_response.cleanup_session(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = await response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_cleanup_session(self, async_client: AsyncMetis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.oauth.with_raw_response.cleanup_session(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_auth_header(self, async_client: AsyncMetis) -> None:
        oauth = await async_client.oauth.get_auth_header(
            provider="provider",
            session_id="session_id",
        )
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_auth_header(self, async_client: AsyncMetis) -> None:
        response = await async_client.oauth.with_raw_response.get_auth_header(
            provider="provider",
            session_id="session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = await response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_auth_header(self, async_client: AsyncMetis) -> None:
        async with async_client.oauth.with_streaming_response.get_auth_header(
            provider="provider",
            session_id="session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = await response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_auth_header(self, async_client: AsyncMetis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.oauth.with_raw_response.get_auth_header(
                provider="provider",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `provider` but received ''"):
            await async_client.oauth.with_raw_response.get_auth_header(
                provider="",
                session_id="session_id",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_handle_callback(self, async_client: AsyncMetis) -> None:
        oauth = await async_client.oauth.handle_callback(
            code="code",
            state="state",
        )
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_handle_callback_with_all_params(self, async_client: AsyncMetis) -> None:
        oauth = await async_client.oauth.handle_callback(
            code="code",
            state="state",
            error="error",
        )
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_handle_callback(self, async_client: AsyncMetis) -> None:
        response = await async_client.oauth.with_raw_response.handle_callback(
            code="code",
            state="state",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = await response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_handle_callback(self, async_client: AsyncMetis) -> None:
        async with async_client.oauth.with_streaming_response.handle_callback(
            code="code",
            state="state",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = await response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_initiate(self, async_client: AsyncMetis) -> None:
        oauth = await async_client.oauth.initiate(
            body={"foo": "bar"},
        )
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_initiate(self, async_client: AsyncMetis) -> None:
        response = await async_client.oauth.with_raw_response.initiate(
            body={"foo": "bar"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = await response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_initiate(self, async_client: AsyncMetis) -> None:
        async with async_client.oauth.with_streaming_response.initiate(
            body={"foo": "bar"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = await response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_status(self, async_client: AsyncMetis) -> None:
        oauth = await async_client.oauth.retrieve_status(
            "session_id",
        )
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_status(self, async_client: AsyncMetis) -> None:
        response = await async_client.oauth.with_raw_response.retrieve_status(
            "session_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = await response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_status(self, async_client: AsyncMetis) -> None:
        async with async_client.oauth.with_streaming_response.retrieve_status(
            "session_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = await response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_status(self, async_client: AsyncMetis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.oauth.with_raw_response.retrieve_status(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_test_config(self, async_client: AsyncMetis) -> None:
        oauth = await async_client.oauth.test_config()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_test_config(self, async_client: AsyncMetis) -> None:
        response = await async_client.oauth.with_raw_response.test_config()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        oauth = await response.parse()
        assert_matches_type(object, oauth, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_test_config(self, async_client: AsyncMetis) -> None:
        async with async_client.oauth.with_streaming_response.test_config() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            oauth = await response.parse()
            assert_matches_type(object, oauth, path=["response"])

        assert cast(Any, response.is_closed) is True

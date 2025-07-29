# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options

__all__ = ["ReconnectResource", "AsyncReconnectResource"]


class ReconnectResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ReconnectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/metis-python#accessing-raw-response-data-eg-headers
        """
        return ReconnectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ReconnectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/metis-python#with_streaming_response
        """
        return ReconnectResourceWithStreamingResponse(self)

    def reconnect(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Reconnect and reinitialize session with MCP servers (same as connect)"""
        return self._post(
            "/reconnect",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncReconnectResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncReconnectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/metis-python#accessing-raw-response-data-eg-headers
        """
        return AsyncReconnectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncReconnectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/metis-python#with_streaming_response
        """
        return AsyncReconnectResourceWithStreamingResponse(self)

    async def reconnect(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Reconnect and reinitialize session with MCP servers (same as connect)"""
        return await self._post(
            "/reconnect",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ReconnectResourceWithRawResponse:
    def __init__(self, reconnect: ReconnectResource) -> None:
        self._reconnect = reconnect

        self.reconnect = to_raw_response_wrapper(
            reconnect.reconnect,
        )


class AsyncReconnectResourceWithRawResponse:
    def __init__(self, reconnect: AsyncReconnectResource) -> None:
        self._reconnect = reconnect

        self.reconnect = async_to_raw_response_wrapper(
            reconnect.reconnect,
        )


class ReconnectResourceWithStreamingResponse:
    def __init__(self, reconnect: ReconnectResource) -> None:
        self._reconnect = reconnect

        self.reconnect = to_streamed_response_wrapper(
            reconnect.reconnect,
        )


class AsyncReconnectResourceWithStreamingResponse:
    def __init__(self, reconnect: AsyncReconnectResource) -> None:
        self._reconnect = reconnect

        self.reconnect = async_to_streamed_response_wrapper(
            reconnect.reconnect,
        )

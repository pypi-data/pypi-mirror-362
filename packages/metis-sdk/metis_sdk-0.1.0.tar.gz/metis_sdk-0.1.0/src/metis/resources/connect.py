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

__all__ = ["ConnectResource", "AsyncConnectResource"]


class ConnectResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConnectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/metis-python#accessing-raw-response-data-eg-headers
        """
        return ConnectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConnectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/metis-python#with_streaming_response
        """
        return ConnectResourceWithStreamingResponse(self)

    def initialize(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Initialize a new chat session with optional user API keys"""
        
        # Merge user API keys from client and method parameter
        body = dict(extra_body) if isinstance(extra_body, dict) else {}
        if hasattr(self._client, 'model_api_keys') and self._client.model_api_keys:
            all_api_keys = dict(self._client.model_api_keys)
            # If body already has api_keys, merge them (body takes precedence)
            if 'api_keys' in body and isinstance(body['api_keys'], dict):
                all_api_keys.update(body['api_keys'])
            # Add API keys to the request body
            if all_api_keys:
                body["api_keys"] = all_api_keys
        
        return self._post(
            "/connect",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncConnectResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConnectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/metis-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConnectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConnectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/metis-python#with_streaming_response
        """
        return AsyncConnectResourceWithStreamingResponse(self)

    async def initialize(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Initialize a new chat session with optional user API keys"""
        
        # Merge user API keys from client and method parameter
        body = dict(extra_body) if isinstance(extra_body, dict) else {}
        if hasattr(self._client, 'model_api_keys') and self._client.model_api_keys:
            all_api_keys = dict(self._client.model_api_keys)
            # If body already has api_keys, merge them (body takes precedence)
            if 'api_keys' in body and isinstance(body['api_keys'], dict):
                all_api_keys.update(body['api_keys'])
            # Add API keys to the request body
            if all_api_keys:
                body["api_keys"] = all_api_keys
        
        return await self._post(
            "/connect",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=body, timeout=timeout
            ),
            cast_to=object,
        )


class ConnectResourceWithRawResponse:
    def __init__(self, connect: ConnectResource) -> None:
        self._connect = connect

        self.initialize = to_raw_response_wrapper(
            connect.initialize,
        )


class AsyncConnectResourceWithRawResponse:
    def __init__(self, connect: AsyncConnectResource) -> None:
        self._connect = connect

        self.initialize = async_to_raw_response_wrapper(
            connect.initialize,
        )


class ConnectResourceWithStreamingResponse:
    def __init__(self, connect: ConnectResource) -> None:
        self._connect = connect

        self.initialize = to_streamed_response_wrapper(
            connect.initialize,
        )


class AsyncConnectResourceWithStreamingResponse:
    def __init__(self, connect: AsyncConnectResource) -> None:
        self._connect = connect

        self.initialize = async_to_streamed_response_wrapper(
            connect.initialize,
        )

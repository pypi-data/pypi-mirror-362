# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional

import httpx

from ..types import brain_create_params, brain_update_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.persistent_brain import PersistentBrain
from ..types.brain_list_response import BrainListResponse

__all__ = ["BrainsResource", "AsyncBrainsResource"]


class BrainsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BrainsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return BrainsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BrainsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return BrainsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        backstory: str,
        creator_id: str,
        goal: str,
        name: str,
        role: str,
        org_id: Optional[str] | NotGiven = NOT_GIVEN,
        prebuilt_tools: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PersistentBrain:
        """
        Create a new brain

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/brains",
            body=maybe_transform(
                {
                    "backstory": backstory,
                    "creator_id": creator_id,
                    "goal": goal,
                    "name": name,
                    "role": role,
                    "org_id": org_id,
                    "prebuilt_tools": prebuilt_tools,
                },
                brain_create_params.BrainCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PersistentBrain,
        )

    def update(
        self,
        brain_id: str,
        *,
        backstory: Optional[str] | NotGiven = NOT_GIVEN,
        goal: Optional[str] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        org_id: Optional[str] | NotGiven = NOT_GIVEN,
        prebuilt_tools: Optional[List[str]] | NotGiven = NOT_GIVEN,
        role: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PersistentBrain:
        """
        Update a brain

        Args:
          brain_id: ID of brain to update

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not brain_id:
            raise ValueError(f"Expected a non-empty value for `brain_id` but received {brain_id!r}")
        return self._put(
            f"/api/brains/{brain_id}",
            body=maybe_transform(
                {
                    "backstory": backstory,
                    "goal": goal,
                    "name": name,
                    "org_id": org_id,
                    "prebuilt_tools": prebuilt_tools,
                    "role": role,
                },
                brain_update_params.BrainUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PersistentBrain,
        )

    def list(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BrainListResponse:
        """
        Get all brains for a user

        Args:
          user_id: ID of user to get brains for

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._get(
            f"/api/brains/{user_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BrainListResponse,
        )

    def delete(
        self,
        brain_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a brain with given ID

        Args:
          brain_id: ID of brain to delete

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not brain_id:
            raise ValueError(f"Expected a non-empty value for `brain_id` but received {brain_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/brains/{brain_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncBrainsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBrainsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncBrainsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBrainsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return AsyncBrainsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        backstory: str,
        creator_id: str,
        goal: str,
        name: str,
        role: str,
        org_id: Optional[str] | NotGiven = NOT_GIVEN,
        prebuilt_tools: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PersistentBrain:
        """
        Create a new brain

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/brains",
            body=await async_maybe_transform(
                {
                    "backstory": backstory,
                    "creator_id": creator_id,
                    "goal": goal,
                    "name": name,
                    "role": role,
                    "org_id": org_id,
                    "prebuilt_tools": prebuilt_tools,
                },
                brain_create_params.BrainCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PersistentBrain,
        )

    async def update(
        self,
        brain_id: str,
        *,
        backstory: Optional[str] | NotGiven = NOT_GIVEN,
        goal: Optional[str] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        org_id: Optional[str] | NotGiven = NOT_GIVEN,
        prebuilt_tools: Optional[List[str]] | NotGiven = NOT_GIVEN,
        role: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PersistentBrain:
        """
        Update a brain

        Args:
          brain_id: ID of brain to update

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not brain_id:
            raise ValueError(f"Expected a non-empty value for `brain_id` but received {brain_id!r}")
        return await self._put(
            f"/api/brains/{brain_id}",
            body=await async_maybe_transform(
                {
                    "backstory": backstory,
                    "goal": goal,
                    "name": name,
                    "org_id": org_id,
                    "prebuilt_tools": prebuilt_tools,
                    "role": role,
                },
                brain_update_params.BrainUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PersistentBrain,
        )

    async def list(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BrainListResponse:
        """
        Get all brains for a user

        Args:
          user_id: ID of user to get brains for

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return await self._get(
            f"/api/brains/{user_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BrainListResponse,
        )

    async def delete(
        self,
        brain_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a brain with given ID

        Args:
          brain_id: ID of brain to delete

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not brain_id:
            raise ValueError(f"Expected a non-empty value for `brain_id` but received {brain_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/brains/{brain_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class BrainsResourceWithRawResponse:
    def __init__(self, brains: BrainsResource) -> None:
        self._brains = brains

        self.create = to_raw_response_wrapper(
            brains.create,
        )
        self.update = to_raw_response_wrapper(
            brains.update,
        )
        self.list = to_raw_response_wrapper(
            brains.list,
        )
        self.delete = to_raw_response_wrapper(
            brains.delete,
        )


class AsyncBrainsResourceWithRawResponse:
    def __init__(self, brains: AsyncBrainsResource) -> None:
        self._brains = brains

        self.create = async_to_raw_response_wrapper(
            brains.create,
        )
        self.update = async_to_raw_response_wrapper(
            brains.update,
        )
        self.list = async_to_raw_response_wrapper(
            brains.list,
        )
        self.delete = async_to_raw_response_wrapper(
            brains.delete,
        )


class BrainsResourceWithStreamingResponse:
    def __init__(self, brains: BrainsResource) -> None:
        self._brains = brains

        self.create = to_streamed_response_wrapper(
            brains.create,
        )
        self.update = to_streamed_response_wrapper(
            brains.update,
        )
        self.list = to_streamed_response_wrapper(
            brains.list,
        )
        self.delete = to_streamed_response_wrapper(
            brains.delete,
        )


class AsyncBrainsResourceWithStreamingResponse:
    def __init__(self, brains: AsyncBrainsResource) -> None:
        self._brains = brains

        self.create = async_to_streamed_response_wrapper(
            brains.create,
        )
        self.update = async_to_streamed_response_wrapper(
            brains.update,
        )
        self.list = async_to_streamed_response_wrapper(
            brains.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            brains.delete,
        )

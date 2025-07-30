# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.ontology import dashboard_list_params, dashboard_create_params, dashboard_update_params
from ...types.ontology.dashboard_model import DashboardModel
from ...types.ontology.layout_item_param import LayoutItemParam
from ...types.ontology.dashboard_list_response import DashboardListResponse

__all__ = ["DashboardsResource", "AsyncDashboardsResource"]


class DashboardsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DashboardsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return DashboardsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DashboardsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return DashboardsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        org_id: str,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        layout: Optional[Iterable[LayoutItemParam]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DashboardModel:
        """
        Create a new dashboard with metrics layout

        Args: dashboard: The dashboard data to create

        Returns: The created dashboard

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/ontology/dashboards",
            body=maybe_transform(
                {
                    "name": name,
                    "org_id": org_id,
                    "description": description,
                    "layout": layout,
                },
                dashboard_create_params.DashboardCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DashboardModel,
        )

    def retrieve(
        self,
        dashboard_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DashboardModel:
        """
        Get a dashboard by ID

        Args: dashboard_id: Dashboard ID to retrieve

        Returns: The dashboard

        Args:
          dashboard_id: Dashboard ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return self._get(
            f"/api/ontology/dashboards/{dashboard_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DashboardModel,
        )

    def update(
        self,
        dashboard_id: str,
        *,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        layout: Optional[Iterable[LayoutItemParam]] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DashboardModel:
        """
        Update a dashboard

        Args: dashboard_id: Dashboard ID to update update_data: Data to update

        Returns: The updated dashboard

        Args:
          dashboard_id: Dashboard ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return self._put(
            f"/api/ontology/dashboards/{dashboard_id}",
            body=maybe_transform(
                {
                    "description": description,
                    "layout": layout,
                    "name": name,
                },
                dashboard_update_params.DashboardUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DashboardModel,
        )

    def list(
        self,
        *,
        org_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DashboardListResponse:
        """
        Get all dashboards for an organization

        Args: org_id: Organization ID to filter by

        Returns: List of dashboards

        Args:
          org_id: Organization ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/ontology/dashboards",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"org_id": org_id}, dashboard_list_params.DashboardListParams),
            ),
            cast_to=DashboardListResponse,
        )

    def delete(
        self,
        dashboard_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DashboardModel:
        """
        Delete a dashboard

        Args: dashboard_id: Dashboard ID to delete

        Returns: The deleted dashboard

        Args:
          dashboard_id: Dashboard ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return self._delete(
            f"/api/ontology/dashboards/{dashboard_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DashboardModel,
        )


class AsyncDashboardsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDashboardsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncDashboardsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDashboardsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return AsyncDashboardsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        org_id: str,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        layout: Optional[Iterable[LayoutItemParam]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DashboardModel:
        """
        Create a new dashboard with metrics layout

        Args: dashboard: The dashboard data to create

        Returns: The created dashboard

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/ontology/dashboards",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "org_id": org_id,
                    "description": description,
                    "layout": layout,
                },
                dashboard_create_params.DashboardCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DashboardModel,
        )

    async def retrieve(
        self,
        dashboard_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DashboardModel:
        """
        Get a dashboard by ID

        Args: dashboard_id: Dashboard ID to retrieve

        Returns: The dashboard

        Args:
          dashboard_id: Dashboard ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return await self._get(
            f"/api/ontology/dashboards/{dashboard_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DashboardModel,
        )

    async def update(
        self,
        dashboard_id: str,
        *,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        layout: Optional[Iterable[LayoutItemParam]] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DashboardModel:
        """
        Update a dashboard

        Args: dashboard_id: Dashboard ID to update update_data: Data to update

        Returns: The updated dashboard

        Args:
          dashboard_id: Dashboard ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return await self._put(
            f"/api/ontology/dashboards/{dashboard_id}",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "layout": layout,
                    "name": name,
                },
                dashboard_update_params.DashboardUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DashboardModel,
        )

    async def list(
        self,
        *,
        org_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DashboardListResponse:
        """
        Get all dashboards for an organization

        Args: org_id: Organization ID to filter by

        Returns: List of dashboards

        Args:
          org_id: Organization ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/ontology/dashboards",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"org_id": org_id}, dashboard_list_params.DashboardListParams),
            ),
            cast_to=DashboardListResponse,
        )

    async def delete(
        self,
        dashboard_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DashboardModel:
        """
        Delete a dashboard

        Args: dashboard_id: Dashboard ID to delete

        Returns: The deleted dashboard

        Args:
          dashboard_id: Dashboard ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not dashboard_id:
            raise ValueError(f"Expected a non-empty value for `dashboard_id` but received {dashboard_id!r}")
        return await self._delete(
            f"/api/ontology/dashboards/{dashboard_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DashboardModel,
        )


class DashboardsResourceWithRawResponse:
    def __init__(self, dashboards: DashboardsResource) -> None:
        self._dashboards = dashboards

        self.create = to_raw_response_wrapper(
            dashboards.create,
        )
        self.retrieve = to_raw_response_wrapper(
            dashboards.retrieve,
        )
        self.update = to_raw_response_wrapper(
            dashboards.update,
        )
        self.list = to_raw_response_wrapper(
            dashboards.list,
        )
        self.delete = to_raw_response_wrapper(
            dashboards.delete,
        )


class AsyncDashboardsResourceWithRawResponse:
    def __init__(self, dashboards: AsyncDashboardsResource) -> None:
        self._dashboards = dashboards

        self.create = async_to_raw_response_wrapper(
            dashboards.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            dashboards.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            dashboards.update,
        )
        self.list = async_to_raw_response_wrapper(
            dashboards.list,
        )
        self.delete = async_to_raw_response_wrapper(
            dashboards.delete,
        )


class DashboardsResourceWithStreamingResponse:
    def __init__(self, dashboards: DashboardsResource) -> None:
        self._dashboards = dashboards

        self.create = to_streamed_response_wrapper(
            dashboards.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            dashboards.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            dashboards.update,
        )
        self.list = to_streamed_response_wrapper(
            dashboards.list,
        )
        self.delete = to_streamed_response_wrapper(
            dashboards.delete,
        )


class AsyncDashboardsResourceWithStreamingResponse:
    def __init__(self, dashboards: AsyncDashboardsResource) -> None:
        self._dashboards = dashboards

        self.create = async_to_streamed_response_wrapper(
            dashboards.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            dashboards.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            dashboards.update,
        )
        self.list = async_to_streamed_response_wrapper(
            dashboards.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            dashboards.delete,
        )

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional

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
from ...types.ontology import (
    MetricStatusEnum,
    ChartVisualizationType,
    metric_list_params,
    metric_create_params,
    metric_update_params,
)
from ...types.ontology.metric_model import MetricModel
from ...types.ontology.metric_status_enum import MetricStatusEnum
from ...types.ontology.metric_list_response import MetricListResponse
from ...types.ontology.chart_visualization_type import ChartVisualizationType

__all__ = ["MetricsResource", "AsyncMetricsResource"]


class MetricsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return MetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return MetricsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        datasource_id: str,
        org_id: str,
        query: str,
        title: str,
        vizualisation: ChartVisualizationType,
        chart_config: Optional[Dict[str, object]] | NotGiven = NOT_GIVEN,
        code: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        status: Optional[MetricStatusEnum] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricModel:
        """
        Create a new metric

        Args:
          vizualisation: Types of chart visualizations available for metrics

          status: Status of a metric

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/ontology/metrics",
            body=maybe_transform(
                {
                    "datasource_id": datasource_id,
                    "org_id": org_id,
                    "query": query,
                    "title": title,
                    "vizualisation": vizualisation,
                    "chart_config": chart_config,
                    "code": code,
                    "description": description,
                    "status": status,
                },
                metric_create_params.MetricCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MetricModel,
        )

    def retrieve(
        self,
        metric_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricModel:
        """
        Get a metric by ID

        Args:
          metric_id: Metric ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not metric_id:
            raise ValueError(f"Expected a non-empty value for `metric_id` but received {metric_id!r}")
        return self._get(
            f"/api/ontology/metrics/{metric_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MetricModel,
        )

    def update(
        self,
        metric_id: str,
        *,
        chart_config: Optional[Dict[str, object]] | NotGiven = NOT_GIVEN,
        code: Optional[str] | NotGiven = NOT_GIVEN,
        datasource_id: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        query: Optional[str] | NotGiven = NOT_GIVEN,
        status: Optional[MetricStatusEnum] | NotGiven = NOT_GIVEN,
        title: Optional[str] | NotGiven = NOT_GIVEN,
        vizualisation: Optional[ChartVisualizationType] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricModel:
        """
        Update a metric

        Args:
          metric_id: Metric ID

          status: Status of a metric

          vizualisation: Types of chart visualizations available for metrics

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not metric_id:
            raise ValueError(f"Expected a non-empty value for `metric_id` but received {metric_id!r}")
        return self._put(
            f"/api/ontology/metrics/{metric_id}",
            body=maybe_transform(
                {
                    "chart_config": chart_config,
                    "code": code,
                    "datasource_id": datasource_id,
                    "description": description,
                    "query": query,
                    "status": status,
                    "title": title,
                    "vizualisation": vizualisation,
                },
                metric_update_params.MetricUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MetricModel,
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
    ) -> MetricListResponse:
        """
        Get all metrics for an organization

        Args:
          org_id: Organization ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/ontology/metrics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"org_id": org_id}, metric_list_params.MetricListParams),
            ),
            cast_to=MetricListResponse,
        )

    def delete(
        self,
        metric_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricModel:
        """
        Delete a metric

        Args:
          metric_id: Metric ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not metric_id:
            raise ValueError(f"Expected a non-empty value for `metric_id` but received {metric_id!r}")
        return self._delete(
            f"/api/ontology/metrics/{metric_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MetricModel,
        )


class AsyncMetricsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMetricsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncMetricsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMetricsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return AsyncMetricsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        datasource_id: str,
        org_id: str,
        query: str,
        title: str,
        vizualisation: ChartVisualizationType,
        chart_config: Optional[Dict[str, object]] | NotGiven = NOT_GIVEN,
        code: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        status: Optional[MetricStatusEnum] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricModel:
        """
        Create a new metric

        Args:
          vizualisation: Types of chart visualizations available for metrics

          status: Status of a metric

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/ontology/metrics",
            body=await async_maybe_transform(
                {
                    "datasource_id": datasource_id,
                    "org_id": org_id,
                    "query": query,
                    "title": title,
                    "vizualisation": vizualisation,
                    "chart_config": chart_config,
                    "code": code,
                    "description": description,
                    "status": status,
                },
                metric_create_params.MetricCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MetricModel,
        )

    async def retrieve(
        self,
        metric_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricModel:
        """
        Get a metric by ID

        Args:
          metric_id: Metric ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not metric_id:
            raise ValueError(f"Expected a non-empty value for `metric_id` but received {metric_id!r}")
        return await self._get(
            f"/api/ontology/metrics/{metric_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MetricModel,
        )

    async def update(
        self,
        metric_id: str,
        *,
        chart_config: Optional[Dict[str, object]] | NotGiven = NOT_GIVEN,
        code: Optional[str] | NotGiven = NOT_GIVEN,
        datasource_id: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        query: Optional[str] | NotGiven = NOT_GIVEN,
        status: Optional[MetricStatusEnum] | NotGiven = NOT_GIVEN,
        title: Optional[str] | NotGiven = NOT_GIVEN,
        vizualisation: Optional[ChartVisualizationType] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricModel:
        """
        Update a metric

        Args:
          metric_id: Metric ID

          status: Status of a metric

          vizualisation: Types of chart visualizations available for metrics

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not metric_id:
            raise ValueError(f"Expected a non-empty value for `metric_id` but received {metric_id!r}")
        return await self._put(
            f"/api/ontology/metrics/{metric_id}",
            body=await async_maybe_transform(
                {
                    "chart_config": chart_config,
                    "code": code,
                    "datasource_id": datasource_id,
                    "description": description,
                    "query": query,
                    "status": status,
                    "title": title,
                    "vizualisation": vizualisation,
                },
                metric_update_params.MetricUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MetricModel,
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
    ) -> MetricListResponse:
        """
        Get all metrics for an organization

        Args:
          org_id: Organization ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/ontology/metrics",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"org_id": org_id}, metric_list_params.MetricListParams),
            ),
            cast_to=MetricListResponse,
        )

    async def delete(
        self,
        metric_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MetricModel:
        """
        Delete a metric

        Args:
          metric_id: Metric ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not metric_id:
            raise ValueError(f"Expected a non-empty value for `metric_id` but received {metric_id!r}")
        return await self._delete(
            f"/api/ontology/metrics/{metric_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MetricModel,
        )


class MetricsResourceWithRawResponse:
    def __init__(self, metrics: MetricsResource) -> None:
        self._metrics = metrics

        self.create = to_raw_response_wrapper(
            metrics.create,
        )
        self.retrieve = to_raw_response_wrapper(
            metrics.retrieve,
        )
        self.update = to_raw_response_wrapper(
            metrics.update,
        )
        self.list = to_raw_response_wrapper(
            metrics.list,
        )
        self.delete = to_raw_response_wrapper(
            metrics.delete,
        )


class AsyncMetricsResourceWithRawResponse:
    def __init__(self, metrics: AsyncMetricsResource) -> None:
        self._metrics = metrics

        self.create = async_to_raw_response_wrapper(
            metrics.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            metrics.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            metrics.update,
        )
        self.list = async_to_raw_response_wrapper(
            metrics.list,
        )
        self.delete = async_to_raw_response_wrapper(
            metrics.delete,
        )


class MetricsResourceWithStreamingResponse:
    def __init__(self, metrics: MetricsResource) -> None:
        self._metrics = metrics

        self.create = to_streamed_response_wrapper(
            metrics.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            metrics.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            metrics.update,
        )
        self.list = to_streamed_response_wrapper(
            metrics.list,
        )
        self.delete = to_streamed_response_wrapper(
            metrics.delete,
        )


class AsyncMetricsResourceWithStreamingResponse:
    def __init__(self, metrics: AsyncMetricsResource) -> None:
        self._metrics = metrics

        self.create = async_to_streamed_response_wrapper(
            metrics.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            metrics.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            metrics.update,
        )
        self.list = async_to_streamed_response_wrapper(
            metrics.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            metrics.delete,
        )

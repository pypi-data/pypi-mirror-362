# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.ontology.datasources import (
    SupportedDataSources,
    clickhouse_create_params,
    clickhouse_update_params,
)
from ....types.ontology.datasources.data_source_model import DataSourceModel
from ....types.ontology.datasources.supported_data_sources import SupportedDataSources
from ....types.ontology.datasources.clickhouse_config_param import ClickhouseConfigParam

__all__ = ["ClickhouseResource", "AsyncClickhouseResource"]


class ClickhouseResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ClickhouseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ClickhouseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ClickhouseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return ClickhouseResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        config: ClickhouseConfigParam,
        created_at: Union[str, datetime],
        edited_at: Union[str, datetime, None],
        name: str,
        org_id: str,
        type: SupportedDataSources,
        id: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        schema: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DataSourceModel:
        """
        Create a new Clickhouse datasource

        Args:
          name: Name of the data source

          org_id: Organization ID of the data source

          type: Type of the data source

          description: Guidelines to use for the data source

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/ontology/datasources/clickhouse",
            body=maybe_transform(
                {
                    "config": config,
                    "created_at": created_at,
                    "edited_at": edited_at,
                    "name": name,
                    "org_id": org_id,
                    "type": type,
                    "id": id,
                    "description": description,
                    "schema": schema,
                },
                clickhouse_create_params.ClickhouseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataSourceModel,
        )

    def update(
        self,
        datasource_id: str,
        *,
        config: clickhouse_update_params.Config,
        created_at: Union[str, datetime],
        edited_at: Union[str, datetime, None],
        name: str,
        org_id: str,
        type: SupportedDataSources,
        id: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        schema: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DataSourceModel:
        """
        Update a Clickhouse datasource

        Args:
          datasource_id: Datasource ID

          config: Configuration for the data source

          name: Name of the data source

          org_id: Organization ID of the data source

          type: Type of the data source

          description: Guidelines to use for the data source

          schema: Schema of the data source

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not datasource_id:
            raise ValueError(f"Expected a non-empty value for `datasource_id` but received {datasource_id!r}")
        return self._put(
            f"/api/ontology/datasources/clickhouse/{datasource_id}",
            body=maybe_transform(
                {
                    "config": config,
                    "created_at": created_at,
                    "edited_at": edited_at,
                    "name": name,
                    "org_id": org_id,
                    "type": type,
                    "id": id,
                    "description": description,
                    "schema": schema,
                },
                clickhouse_update_params.ClickhouseUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataSourceModel,
        )

    def delete(
        self,
        datasource_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DataSourceModel:
        """
        Delete a Clickhouse datasource

        Args:
          datasource_id: Datasource ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not datasource_id:
            raise ValueError(f"Expected a non-empty value for `datasource_id` but received {datasource_id!r}")
        return self._delete(
            f"/api/ontology/datasources/clickhouse/{datasource_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataSourceModel,
        )


class AsyncClickhouseResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncClickhouseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncClickhouseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncClickhouseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return AsyncClickhouseResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        config: ClickhouseConfigParam,
        created_at: Union[str, datetime],
        edited_at: Union[str, datetime, None],
        name: str,
        org_id: str,
        type: SupportedDataSources,
        id: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        schema: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DataSourceModel:
        """
        Create a new Clickhouse datasource

        Args:
          name: Name of the data source

          org_id: Organization ID of the data source

          type: Type of the data source

          description: Guidelines to use for the data source

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/ontology/datasources/clickhouse",
            body=await async_maybe_transform(
                {
                    "config": config,
                    "created_at": created_at,
                    "edited_at": edited_at,
                    "name": name,
                    "org_id": org_id,
                    "type": type,
                    "id": id,
                    "description": description,
                    "schema": schema,
                },
                clickhouse_create_params.ClickhouseCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataSourceModel,
        )

    async def update(
        self,
        datasource_id: str,
        *,
        config: clickhouse_update_params.Config,
        created_at: Union[str, datetime],
        edited_at: Union[str, datetime, None],
        name: str,
        org_id: str,
        type: SupportedDataSources,
        id: Optional[str] | NotGiven = NOT_GIVEN,
        description: Optional[str] | NotGiven = NOT_GIVEN,
        schema: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DataSourceModel:
        """
        Update a Clickhouse datasource

        Args:
          datasource_id: Datasource ID

          config: Configuration for the data source

          name: Name of the data source

          org_id: Organization ID of the data source

          type: Type of the data source

          description: Guidelines to use for the data source

          schema: Schema of the data source

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not datasource_id:
            raise ValueError(f"Expected a non-empty value for `datasource_id` but received {datasource_id!r}")
        return await self._put(
            f"/api/ontology/datasources/clickhouse/{datasource_id}",
            body=await async_maybe_transform(
                {
                    "config": config,
                    "created_at": created_at,
                    "edited_at": edited_at,
                    "name": name,
                    "org_id": org_id,
                    "type": type,
                    "id": id,
                    "description": description,
                    "schema": schema,
                },
                clickhouse_update_params.ClickhouseUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataSourceModel,
        )

    async def delete(
        self,
        datasource_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DataSourceModel:
        """
        Delete a Clickhouse datasource

        Args:
          datasource_id: Datasource ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not datasource_id:
            raise ValueError(f"Expected a non-empty value for `datasource_id` but received {datasource_id!r}")
        return await self._delete(
            f"/api/ontology/datasources/clickhouse/{datasource_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataSourceModel,
        )


class ClickhouseResourceWithRawResponse:
    def __init__(self, clickhouse: ClickhouseResource) -> None:
        self._clickhouse = clickhouse

        self.create = to_raw_response_wrapper(
            clickhouse.create,
        )
        self.update = to_raw_response_wrapper(
            clickhouse.update,
        )
        self.delete = to_raw_response_wrapper(
            clickhouse.delete,
        )


class AsyncClickhouseResourceWithRawResponse:
    def __init__(self, clickhouse: AsyncClickhouseResource) -> None:
        self._clickhouse = clickhouse

        self.create = async_to_raw_response_wrapper(
            clickhouse.create,
        )
        self.update = async_to_raw_response_wrapper(
            clickhouse.update,
        )
        self.delete = async_to_raw_response_wrapper(
            clickhouse.delete,
        )


class ClickhouseResourceWithStreamingResponse:
    def __init__(self, clickhouse: ClickhouseResource) -> None:
        self._clickhouse = clickhouse

        self.create = to_streamed_response_wrapper(
            clickhouse.create,
        )
        self.update = to_streamed_response_wrapper(
            clickhouse.update,
        )
        self.delete = to_streamed_response_wrapper(
            clickhouse.delete,
        )


class AsyncClickhouseResourceWithStreamingResponse:
    def __init__(self, clickhouse: AsyncClickhouseResource) -> None:
        self._clickhouse = clickhouse

        self.create = async_to_streamed_response_wrapper(
            clickhouse.create,
        )
        self.update = async_to_streamed_response_wrapper(
            clickhouse.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            clickhouse.delete,
        )

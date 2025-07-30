# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .schema import (
    SchemaResource,
    AsyncSchemaResource,
    SchemaResourceWithRawResponse,
    AsyncSchemaResourceWithRawResponse,
    SchemaResourceWithStreamingResponse,
    AsyncSchemaResourceWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from .clickhouse import (
    ClickhouseResource,
    AsyncClickhouseResource,
    ClickhouseResourceWithRawResponse,
    AsyncClickhouseResourceWithRawResponse,
    ClickhouseResourceWithStreamingResponse,
    AsyncClickhouseResourceWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.ontology import datasource_list_params
from ....types.ontology.datasource_list_response import DatasourceListResponse
from ....types.ontology.datasources.data_source_model import DataSourceModel
from ....types.ontology.datasource_test_connection_response import DatasourceTestConnectionResponse

__all__ = ["DatasourcesResource", "AsyncDatasourcesResource"]


class DatasourcesResource(SyncAPIResource):
    @cached_property
    def clickhouse(self) -> ClickhouseResource:
        return ClickhouseResource(self._client)

    @cached_property
    def schema(self) -> SchemaResource:
        return SchemaResource(self._client)

    @cached_property
    def with_raw_response(self) -> DatasourcesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return DatasourcesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DatasourcesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return DatasourcesResourceWithStreamingResponse(self)

    def retrieve(
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
        Get a datasource by ID

        Args:
          datasource_id: Datasource ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not datasource_id:
            raise ValueError(f"Expected a non-empty value for `datasource_id` but received {datasource_id!r}")
        return self._get(
            f"/api/ontology/datasources/{datasource_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataSourceModel,
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
    ) -> DatasourceListResponse:
        """
        Get all datasources for an organization

        Args:
          org_id: Organization ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/ontology/datasources",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"org_id": org_id}, datasource_list_params.DatasourceListParams),
            ),
            cast_to=DatasourceListResponse,
        )

    def test_connection(
        self,
        datasource_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasourceTestConnectionResponse:
        """
        Test the connection to a specific datasource.

        Args: datasource_id: The ID of the datasource to test.

        Returns: TestConnectionResponse: An object indicating if the connection was
        successful.

        Args:
          datasource_id: Datasource ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not datasource_id:
            raise ValueError(f"Expected a non-empty value for `datasource_id` but received {datasource_id!r}")
        return self._post(
            f"/api/ontology/datasources/{datasource_id}/test",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasourceTestConnectionResponse,
        )


class AsyncDatasourcesResource(AsyncAPIResource):
    @cached_property
    def clickhouse(self) -> AsyncClickhouseResource:
        return AsyncClickhouseResource(self._client)

    @cached_property
    def schema(self) -> AsyncSchemaResource:
        return AsyncSchemaResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDatasourcesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncDatasourcesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDatasourcesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return AsyncDatasourcesResourceWithStreamingResponse(self)

    async def retrieve(
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
        Get a datasource by ID

        Args:
          datasource_id: Datasource ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not datasource_id:
            raise ValueError(f"Expected a non-empty value for `datasource_id` but received {datasource_id!r}")
        return await self._get(
            f"/api/ontology/datasources/{datasource_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataSourceModel,
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
    ) -> DatasourceListResponse:
        """
        Get all datasources for an organization

        Args:
          org_id: Organization ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/ontology/datasources",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"org_id": org_id}, datasource_list_params.DatasourceListParams),
            ),
            cast_to=DatasourceListResponse,
        )

    async def test_connection(
        self,
        datasource_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DatasourceTestConnectionResponse:
        """
        Test the connection to a specific datasource.

        Args: datasource_id: The ID of the datasource to test.

        Returns: TestConnectionResponse: An object indicating if the connection was
        successful.

        Args:
          datasource_id: Datasource ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not datasource_id:
            raise ValueError(f"Expected a non-empty value for `datasource_id` but received {datasource_id!r}")
        return await self._post(
            f"/api/ontology/datasources/{datasource_id}/test",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DatasourceTestConnectionResponse,
        )


class DatasourcesResourceWithRawResponse:
    def __init__(self, datasources: DatasourcesResource) -> None:
        self._datasources = datasources

        self.retrieve = to_raw_response_wrapper(
            datasources.retrieve,
        )
        self.list = to_raw_response_wrapper(
            datasources.list,
        )
        self.test_connection = to_raw_response_wrapper(
            datasources.test_connection,
        )

    @cached_property
    def clickhouse(self) -> ClickhouseResourceWithRawResponse:
        return ClickhouseResourceWithRawResponse(self._datasources.clickhouse)

    @cached_property
    def schema(self) -> SchemaResourceWithRawResponse:
        return SchemaResourceWithRawResponse(self._datasources.schema)


class AsyncDatasourcesResourceWithRawResponse:
    def __init__(self, datasources: AsyncDatasourcesResource) -> None:
        self._datasources = datasources

        self.retrieve = async_to_raw_response_wrapper(
            datasources.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            datasources.list,
        )
        self.test_connection = async_to_raw_response_wrapper(
            datasources.test_connection,
        )

    @cached_property
    def clickhouse(self) -> AsyncClickhouseResourceWithRawResponse:
        return AsyncClickhouseResourceWithRawResponse(self._datasources.clickhouse)

    @cached_property
    def schema(self) -> AsyncSchemaResourceWithRawResponse:
        return AsyncSchemaResourceWithRawResponse(self._datasources.schema)


class DatasourcesResourceWithStreamingResponse:
    def __init__(self, datasources: DatasourcesResource) -> None:
        self._datasources = datasources

        self.retrieve = to_streamed_response_wrapper(
            datasources.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            datasources.list,
        )
        self.test_connection = to_streamed_response_wrapper(
            datasources.test_connection,
        )

    @cached_property
    def clickhouse(self) -> ClickhouseResourceWithStreamingResponse:
        return ClickhouseResourceWithStreamingResponse(self._datasources.clickhouse)

    @cached_property
    def schema(self) -> SchemaResourceWithStreamingResponse:
        return SchemaResourceWithStreamingResponse(self._datasources.schema)


class AsyncDatasourcesResourceWithStreamingResponse:
    def __init__(self, datasources: AsyncDatasourcesResource) -> None:
        self._datasources = datasources

        self.retrieve = async_to_streamed_response_wrapper(
            datasources.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            datasources.list,
        )
        self.test_connection = async_to_streamed_response_wrapper(
            datasources.test_connection,
        )

    @cached_property
    def clickhouse(self) -> AsyncClickhouseResourceWithStreamingResponse:
        return AsyncClickhouseResourceWithStreamingResponse(self._datasources.clickhouse)

    @cached_property
    def schema(self) -> AsyncSchemaResourceWithStreamingResponse:
        return AsyncSchemaResourceWithStreamingResponse(self._datasources.schema)

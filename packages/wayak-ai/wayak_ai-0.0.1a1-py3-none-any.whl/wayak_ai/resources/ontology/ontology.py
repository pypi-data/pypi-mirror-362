# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .agent import (
    AgentResource,
    AsyncAgentResource,
    AgentResourceWithRawResponse,
    AsyncAgentResourceWithRawResponse,
    AgentResourceWithStreamingResponse,
    AsyncAgentResourceWithStreamingResponse,
)
from ...types import ontology_execute_query_params
from .metrics import (
    MetricsResource,
    AsyncMetricsResource,
    MetricsResourceWithRawResponse,
    AsyncMetricsResourceWithRawResponse,
    MetricsResourceWithStreamingResponse,
    AsyncMetricsResourceWithStreamingResponse,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from .dashboards import (
    DashboardsResource,
    AsyncDashboardsResource,
    DashboardsResourceWithRawResponse,
    AsyncDashboardsResourceWithRawResponse,
    DashboardsResourceWithStreamingResponse,
    AsyncDashboardsResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from .datasources.datasources import (
    DatasourcesResource,
    AsyncDatasourcesResource,
    DatasourcesResourceWithRawResponse,
    AsyncDatasourcesResourceWithRawResponse,
    DatasourcesResourceWithStreamingResponse,
    AsyncDatasourcesResourceWithStreamingResponse,
)
from ...types.ontology_execute_query_response import OntologyExecuteQueryResponse

__all__ = ["OntologyResource", "AsyncOntologyResource"]


class OntologyResource(SyncAPIResource):
    @cached_property
    def dashboards(self) -> DashboardsResource:
        return DashboardsResource(self._client)

    @cached_property
    def datasources(self) -> DatasourcesResource:
        return DatasourcesResource(self._client)

    @cached_property
    def agent(self) -> AgentResource:
        return AgentResource(self._client)

    @cached_property
    def metrics(self) -> MetricsResource:
        return MetricsResource(self._client)

    @cached_property
    def with_raw_response(self) -> OntologyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return OntologyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OntologyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return OntologyResourceWithStreamingResponse(self)

    def execute_query(
        self,
        *,
        datasource_id: str,
        sql_query: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OntologyExecuteQueryResponse:
        """
        Execute Query

        Args:
          datasource_id: ID of the datasource to use

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            "/api/ontology/execute-query",
            body=maybe_transform(
                {
                    "datasource_id": datasource_id,
                    "sql_query": sql_query,
                },
                ontology_execute_query_params.OntologyExecuteQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OntologyExecuteQueryResponse,
        )


class AsyncOntologyResource(AsyncAPIResource):
    @cached_property
    def dashboards(self) -> AsyncDashboardsResource:
        return AsyncDashboardsResource(self._client)

    @cached_property
    def datasources(self) -> AsyncDatasourcesResource:
        return AsyncDatasourcesResource(self._client)

    @cached_property
    def agent(self) -> AsyncAgentResource:
        return AsyncAgentResource(self._client)

    @cached_property
    def metrics(self) -> AsyncMetricsResource:
        return AsyncMetricsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncOntologyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncOntologyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOntologyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return AsyncOntologyResourceWithStreamingResponse(self)

    async def execute_query(
        self,
        *,
        datasource_id: str,
        sql_query: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OntologyExecuteQueryResponse:
        """
        Execute Query

        Args:
          datasource_id: ID of the datasource to use

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            "/api/ontology/execute-query",
            body=await async_maybe_transform(
                {
                    "datasource_id": datasource_id,
                    "sql_query": sql_query,
                },
                ontology_execute_query_params.OntologyExecuteQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=OntologyExecuteQueryResponse,
        )


class OntologyResourceWithRawResponse:
    def __init__(self, ontology: OntologyResource) -> None:
        self._ontology = ontology

        self.execute_query = to_raw_response_wrapper(
            ontology.execute_query,
        )

    @cached_property
    def dashboards(self) -> DashboardsResourceWithRawResponse:
        return DashboardsResourceWithRawResponse(self._ontology.dashboards)

    @cached_property
    def datasources(self) -> DatasourcesResourceWithRawResponse:
        return DatasourcesResourceWithRawResponse(self._ontology.datasources)

    @cached_property
    def agent(self) -> AgentResourceWithRawResponse:
        return AgentResourceWithRawResponse(self._ontology.agent)

    @cached_property
    def metrics(self) -> MetricsResourceWithRawResponse:
        return MetricsResourceWithRawResponse(self._ontology.metrics)


class AsyncOntologyResourceWithRawResponse:
    def __init__(self, ontology: AsyncOntologyResource) -> None:
        self._ontology = ontology

        self.execute_query = async_to_raw_response_wrapper(
            ontology.execute_query,
        )

    @cached_property
    def dashboards(self) -> AsyncDashboardsResourceWithRawResponse:
        return AsyncDashboardsResourceWithRawResponse(self._ontology.dashboards)

    @cached_property
    def datasources(self) -> AsyncDatasourcesResourceWithRawResponse:
        return AsyncDatasourcesResourceWithRawResponse(self._ontology.datasources)

    @cached_property
    def agent(self) -> AsyncAgentResourceWithRawResponse:
        return AsyncAgentResourceWithRawResponse(self._ontology.agent)

    @cached_property
    def metrics(self) -> AsyncMetricsResourceWithRawResponse:
        return AsyncMetricsResourceWithRawResponse(self._ontology.metrics)


class OntologyResourceWithStreamingResponse:
    def __init__(self, ontology: OntologyResource) -> None:
        self._ontology = ontology

        self.execute_query = to_streamed_response_wrapper(
            ontology.execute_query,
        )

    @cached_property
    def dashboards(self) -> DashboardsResourceWithStreamingResponse:
        return DashboardsResourceWithStreamingResponse(self._ontology.dashboards)

    @cached_property
    def datasources(self) -> DatasourcesResourceWithStreamingResponse:
        return DatasourcesResourceWithStreamingResponse(self._ontology.datasources)

    @cached_property
    def agent(self) -> AgentResourceWithStreamingResponse:
        return AgentResourceWithStreamingResponse(self._ontology.agent)

    @cached_property
    def metrics(self) -> MetricsResourceWithStreamingResponse:
        return MetricsResourceWithStreamingResponse(self._ontology.metrics)


class AsyncOntologyResourceWithStreamingResponse:
    def __init__(self, ontology: AsyncOntologyResource) -> None:
        self._ontology = ontology

        self.execute_query = async_to_streamed_response_wrapper(
            ontology.execute_query,
        )

    @cached_property
    def dashboards(self) -> AsyncDashboardsResourceWithStreamingResponse:
        return AsyncDashboardsResourceWithStreamingResponse(self._ontology.dashboards)

    @cached_property
    def datasources(self) -> AsyncDatasourcesResourceWithStreamingResponse:
        return AsyncDatasourcesResourceWithStreamingResponse(self._ontology.datasources)

    @cached_property
    def agent(self) -> AsyncAgentResourceWithStreamingResponse:
        return AsyncAgentResourceWithStreamingResponse(self._ontology.agent)

    @cached_property
    def metrics(self) -> AsyncMetricsResourceWithStreamingResponse:
        return AsyncMetricsResourceWithStreamingResponse(self._ontology.metrics)

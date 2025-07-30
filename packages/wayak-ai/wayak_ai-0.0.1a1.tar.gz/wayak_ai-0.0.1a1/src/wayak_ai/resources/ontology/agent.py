# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional

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
from ...types.ontology import agent_chat_params
from ...types.message_param import MessageParam
from ...types.persistent_message import PersistentMessage

__all__ = ["AgentResource", "AsyncAgentResource"]


class AgentResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AgentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AgentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AgentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return AgentResourceWithStreamingResponse(self)

    def chat(
        self,
        *,
        datasource_id: str,
        messages: Iterable[MessageParam],
        org_id: str,
        thread_id: str,
        file_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[str] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        save_messages: Optional[bool] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PersistentMessage:
        """
        Start a chat session with a datasource agent that can analyze data from the
        specified datasource using natural language. The endpoint dynamically selects
        the appropriate tools based on the datasource type (Clickhouse, Postgres, etc.).

        Args: datasource_id: ID of the datasource to analyze request: Chat request
        containing messages and other parameters

        Returns: PersistentMessage: An empty message that will be updated with the
        agent's response

        Args:
          datasource_id: ID of the datasource to use

          org_id: ID of the organization to use

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/ontology/agent/chat",
            body=maybe_transform(
                {
                    "datasource_id": datasource_id,
                    "messages": messages,
                    "org_id": org_id,
                    "thread_id": thread_id,
                    "file_ids": file_ids,
                    "model": model,
                    "project_id": project_id,
                    "save_messages": save_messages,
                },
                agent_chat_params.AgentChatParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PersistentMessage,
        )


class AsyncAgentResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAgentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncAgentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAgentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return AsyncAgentResourceWithStreamingResponse(self)

    async def chat(
        self,
        *,
        datasource_id: str,
        messages: Iterable[MessageParam],
        org_id: str,
        thread_id: str,
        file_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[str] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        save_messages: Optional[bool] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PersistentMessage:
        """
        Start a chat session with a datasource agent that can analyze data from the
        specified datasource using natural language. The endpoint dynamically selects
        the appropriate tools based on the datasource type (Clickhouse, Postgres, etc.).

        Args: datasource_id: ID of the datasource to analyze request: Chat request
        containing messages and other parameters

        Returns: PersistentMessage: An empty message that will be updated with the
        agent's response

        Args:
          datasource_id: ID of the datasource to use

          org_id: ID of the organization to use

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/ontology/agent/chat",
            body=await async_maybe_transform(
                {
                    "datasource_id": datasource_id,
                    "messages": messages,
                    "org_id": org_id,
                    "thread_id": thread_id,
                    "file_ids": file_ids,
                    "model": model,
                    "project_id": project_id,
                    "save_messages": save_messages,
                },
                agent_chat_params.AgentChatParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PersistentMessage,
        )


class AgentResourceWithRawResponse:
    def __init__(self, agent: AgentResource) -> None:
        self._agent = agent

        self.chat = to_raw_response_wrapper(
            agent.chat,
        )


class AsyncAgentResourceWithRawResponse:
    def __init__(self, agent: AsyncAgentResource) -> None:
        self._agent = agent

        self.chat = async_to_raw_response_wrapper(
            agent.chat,
        )


class AgentResourceWithStreamingResponse:
    def __init__(self, agent: AgentResource) -> None:
        self._agent = agent

        self.chat = to_streamed_response_wrapper(
            agent.chat,
        )


class AsyncAgentResourceWithStreamingResponse:
    def __init__(self, agent: AsyncAgentResource) -> None:
        self._agent = agent

        self.chat = async_to_streamed_response_wrapper(
            agent.chat,
        )

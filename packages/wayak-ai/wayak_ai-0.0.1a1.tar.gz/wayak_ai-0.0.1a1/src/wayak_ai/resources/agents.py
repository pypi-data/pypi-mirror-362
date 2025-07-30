# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Mapping, Iterable, Optional, cast

import httpx

from ..types import (
    agent_get_completion_params,
    agent_extract_content_params,
    agent_send_message_to_agent_params,
    agent_send_message_to_wayak_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven, FileTypes
from .._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.message_param import MessageParam
from ..types.persistent_message import PersistentMessage
from ..types.agent_get_completion_response import AgentGetCompletionResponse
from ..types.agent_extract_content_response import AgentExtractContentResponse
from ..types.agent_list_supported_models_response import AgentListSupportedModelsResponse

__all__ = ["AgentsResource", "AsyncAgentsResource"]


class AgentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AgentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AgentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AgentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return AgentsResourceWithStreamingResponse(self)

    def extract_content(
        self,
        *,
        file: FileTypes,
        schema: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AgentExtractContentResponse:
        """Extract content from a file (PDF or image) using OCR capabilities.

        Returns a
        complete markdown document with embedded images.

        Args: file: The uploaded file (PDF or image) schema: JSON schema defining fields
        to extract (as form data). Example: { "type": "object", "properties": { "name":
        { "type": "string", "description": "The name of the person" }, "age": { "type":
        "integer", "description": "The age of the person" } }, "required": ["name",
        "age"] }

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal(
            {
                "file": file,
                "schema": schema,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/api/agents/extraction",
            body=maybe_transform(body, agent_extract_content_params.AgentExtractContentParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentExtractContentResponse,
        )

    def get_completion(
        self,
        *,
        messages: Iterable[MessageParam],
        model: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AgentGetCompletionResponse:
        """
        Get a direct completion from an LLM based on the provided messages.

        Args: request: CompletionRequest containing messages and model name

        Returns: dict: The LLM's response

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/agents/completion",
            body=maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                },
                agent_get_completion_params.AgentGetCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentGetCompletionResponse,
        )

    def list_supported_models(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AgentListSupportedModelsResponse:
        """Get all supported models"""
        return self._get(
            "/api/agents/models",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentListSupportedModelsResponse,
        )

    def send_message_to_agent(
        self,
        agent_id: str,
        *,
        messages: Iterable[MessageParam],
        thread_id: str,
        file_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[str] | NotGiven = NOT_GIVEN,
        org_id: Optional[str] | NotGiven = NOT_GIVEN,
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
        Send a message to a specific agent

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return self._post(
            f"/api/agents/agent/{agent_id}",
            body=maybe_transform(
                {
                    "messages": messages,
                    "thread_id": thread_id,
                    "file_ids": file_ids,
                    "model": model,
                    "org_id": org_id,
                    "project_id": project_id,
                    "save_messages": save_messages,
                },
                agent_send_message_to_agent_params.AgentSendMessageToAgentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PersistentMessage,
        )

    def send_message_to_wayak(
        self,
        *,
        messages: Iterable[MessageParam],
        thread_id: str,
        file_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[str] | NotGiven = NOT_GIVEN,
        org_id: Optional[str] | NotGiven = NOT_GIVEN,
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
        Send a message to a Wayak Agent

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/agents/wayak",
            body=maybe_transform(
                {
                    "messages": messages,
                    "thread_id": thread_id,
                    "file_ids": file_ids,
                    "model": model,
                    "org_id": org_id,
                    "project_id": project_id,
                    "save_messages": save_messages,
                },
                agent_send_message_to_wayak_params.AgentSendMessageToWayakParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PersistentMessage,
        )


class AsyncAgentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAgentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncAgentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAgentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wayak-ventures/wayak-python-sdk#with_streaming_response
        """
        return AsyncAgentsResourceWithStreamingResponse(self)

    async def extract_content(
        self,
        *,
        file: FileTypes,
        schema: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AgentExtractContentResponse:
        """Extract content from a file (PDF or image) using OCR capabilities.

        Returns a
        complete markdown document with embedded images.

        Args: file: The uploaded file (PDF or image) schema: JSON schema defining fields
        to extract (as form data). Example: { "type": "object", "properties": { "name":
        { "type": "string", "description": "The name of the person" }, "age": { "type":
        "integer", "description": "The age of the person" } }, "required": ["name",
        "age"] }

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_minimal(
            {
                "file": file,
                "schema": schema,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/api/agents/extraction",
            body=await async_maybe_transform(body, agent_extract_content_params.AgentExtractContentParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentExtractContentResponse,
        )

    async def get_completion(
        self,
        *,
        messages: Iterable[MessageParam],
        model: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AgentGetCompletionResponse:
        """
        Get a direct completion from an LLM based on the provided messages.

        Args: request: CompletionRequest containing messages and model name

        Returns: dict: The LLM's response

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/agents/completion",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                },
                agent_get_completion_params.AgentGetCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentGetCompletionResponse,
        )

    async def list_supported_models(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AgentListSupportedModelsResponse:
        """Get all supported models"""
        return await self._get(
            "/api/agents/models",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentListSupportedModelsResponse,
        )

    async def send_message_to_agent(
        self,
        agent_id: str,
        *,
        messages: Iterable[MessageParam],
        thread_id: str,
        file_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[str] | NotGiven = NOT_GIVEN,
        org_id: Optional[str] | NotGiven = NOT_GIVEN,
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
        Send a message to a specific agent

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return await self._post(
            f"/api/agents/agent/{agent_id}",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "thread_id": thread_id,
                    "file_ids": file_ids,
                    "model": model,
                    "org_id": org_id,
                    "project_id": project_id,
                    "save_messages": save_messages,
                },
                agent_send_message_to_agent_params.AgentSendMessageToAgentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PersistentMessage,
        )

    async def send_message_to_wayak(
        self,
        *,
        messages: Iterable[MessageParam],
        thread_id: str,
        file_ids: Optional[List[str]] | NotGiven = NOT_GIVEN,
        model: Optional[str] | NotGiven = NOT_GIVEN,
        org_id: Optional[str] | NotGiven = NOT_GIVEN,
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
        Send a message to a Wayak Agent

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/agents/wayak",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "thread_id": thread_id,
                    "file_ids": file_ids,
                    "model": model,
                    "org_id": org_id,
                    "project_id": project_id,
                    "save_messages": save_messages,
                },
                agent_send_message_to_wayak_params.AgentSendMessageToWayakParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PersistentMessage,
        )


class AgentsResourceWithRawResponse:
    def __init__(self, agents: AgentsResource) -> None:
        self._agents = agents

        self.extract_content = to_raw_response_wrapper(
            agents.extract_content,
        )
        self.get_completion = to_raw_response_wrapper(
            agents.get_completion,
        )
        self.list_supported_models = to_raw_response_wrapper(
            agents.list_supported_models,
        )
        self.send_message_to_agent = to_raw_response_wrapper(
            agents.send_message_to_agent,
        )
        self.send_message_to_wayak = to_raw_response_wrapper(
            agents.send_message_to_wayak,
        )


class AsyncAgentsResourceWithRawResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

        self.extract_content = async_to_raw_response_wrapper(
            agents.extract_content,
        )
        self.get_completion = async_to_raw_response_wrapper(
            agents.get_completion,
        )
        self.list_supported_models = async_to_raw_response_wrapper(
            agents.list_supported_models,
        )
        self.send_message_to_agent = async_to_raw_response_wrapper(
            agents.send_message_to_agent,
        )
        self.send_message_to_wayak = async_to_raw_response_wrapper(
            agents.send_message_to_wayak,
        )


class AgentsResourceWithStreamingResponse:
    def __init__(self, agents: AgentsResource) -> None:
        self._agents = agents

        self.extract_content = to_streamed_response_wrapper(
            agents.extract_content,
        )
        self.get_completion = to_streamed_response_wrapper(
            agents.get_completion,
        )
        self.list_supported_models = to_streamed_response_wrapper(
            agents.list_supported_models,
        )
        self.send_message_to_agent = to_streamed_response_wrapper(
            agents.send_message_to_agent,
        )
        self.send_message_to_wayak = to_streamed_response_wrapper(
            agents.send_message_to_wayak,
        )


class AsyncAgentsResourceWithStreamingResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

        self.extract_content = async_to_streamed_response_wrapper(
            agents.extract_content,
        )
        self.get_completion = async_to_streamed_response_wrapper(
            agents.get_completion,
        )
        self.list_supported_models = async_to_streamed_response_wrapper(
            agents.list_supported_models,
        )
        self.send_message_to_agent = async_to_streamed_response_wrapper(
            agents.send_message_to_agent,
        )
        self.send_message_to_wayak = async_to_streamed_response_wrapper(
            agents.send_message_to_wayak,
        )

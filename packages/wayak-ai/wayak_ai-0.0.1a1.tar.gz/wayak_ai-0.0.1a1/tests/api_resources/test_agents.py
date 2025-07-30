# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from wayak_ai import WayakAI, AsyncWayakAI
from tests.utils import assert_matches_type
from wayak_ai.types import (
    PersistentMessage,
    AgentGetCompletionResponse,
    AgentExtractContentResponse,
    AgentListSupportedModelsResponse,
)
from wayak_ai._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAgents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_extract_content(self, client: WayakAI) -> None:
        agent = client.agents.extract_content(
            file=b"raw file contents",
            schema="schema",
        )
        assert_matches_type(AgentExtractContentResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_extract_content(self, client: WayakAI) -> None:
        response = client.agents.with_raw_response.extract_content(
            file=b"raw file contents",
            schema="schema",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(AgentExtractContentResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_extract_content(self, client: WayakAI) -> None:
        with client.agents.with_streaming_response.extract_content(
            file=b"raw file contents",
            schema="schema",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(AgentExtractContentResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_completion(self, client: WayakAI) -> None:
        agent = client.agents.get_completion(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
        )
        assert_matches_type(AgentGetCompletionResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_completion_with_all_params(self, client: WayakAI) -> None:
        agent = client.agents.get_completion(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                    "id": "id",
                    "created_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "images": ["string"],
                }
            ],
            model="model",
        )
        assert_matches_type(AgentGetCompletionResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_completion(self, client: WayakAI) -> None:
        response = client.agents.with_raw_response.get_completion(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(AgentGetCompletionResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_completion(self, client: WayakAI) -> None:
        with client.agents.with_streaming_response.get_completion(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(AgentGetCompletionResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list_supported_models(self, client: WayakAI) -> None:
        agent = client.agents.list_supported_models()
        assert_matches_type(AgentListSupportedModelsResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_supported_models(self, client: WayakAI) -> None:
        response = client.agents.with_raw_response.list_supported_models()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(AgentListSupportedModelsResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_supported_models(self, client: WayakAI) -> None:
        with client.agents.with_streaming_response.list_supported_models() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(AgentListSupportedModelsResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_send_message_to_agent(self, client: WayakAI) -> None:
        agent = client.agents.send_message_to_agent(
            agent_id="agentId",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_send_message_to_agent_with_all_params(self, client: WayakAI) -> None:
        agent = client.agents.send_message_to_agent(
            agent_id="agentId",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                    "id": "id",
                    "created_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "images": ["string"],
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            file_ids=["string"],
            model="model",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            save_messages=True,
        )
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_send_message_to_agent(self, client: WayakAI) -> None:
        response = client.agents.with_raw_response.send_message_to_agent(
            agent_id="agentId",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_send_message_to_agent(self, client: WayakAI) -> None:
        with client.agents.with_streaming_response.send_message_to_agent(
            agent_id="agentId",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(PersistentMessage, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_send_message_to_agent(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.with_raw_response.send_message_to_agent(
                agent_id="",
                messages=[
                    {
                        "content": "content",
                        "role": "role",
                    }
                ],
                thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_send_message_to_wayak(self, client: WayakAI) -> None:
        agent = client.agents.send_message_to_wayak(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_send_message_to_wayak_with_all_params(self, client: WayakAI) -> None:
        agent = client.agents.send_message_to_wayak(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                    "id": "id",
                    "created_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "images": ["string"],
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            file_ids=["string"],
            model="model",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            save_messages=True,
        )
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_send_message_to_wayak(self, client: WayakAI) -> None:
        response = client.agents.with_raw_response.send_message_to_wayak(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_send_message_to_wayak(self, client: WayakAI) -> None:
        with client.agents.with_streaming_response.send_message_to_wayak(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(PersistentMessage, agent, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAgents:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_extract_content(self, async_client: AsyncWayakAI) -> None:
        agent = await async_client.agents.extract_content(
            file=b"raw file contents",
            schema="schema",
        )
        assert_matches_type(AgentExtractContentResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_extract_content(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.agents.with_raw_response.extract_content(
            file=b"raw file contents",
            schema="schema",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(AgentExtractContentResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_extract_content(self, async_client: AsyncWayakAI) -> None:
        async with async_client.agents.with_streaming_response.extract_content(
            file=b"raw file contents",
            schema="schema",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(AgentExtractContentResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_completion(self, async_client: AsyncWayakAI) -> None:
        agent = await async_client.agents.get_completion(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
        )
        assert_matches_type(AgentGetCompletionResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_completion_with_all_params(self, async_client: AsyncWayakAI) -> None:
        agent = await async_client.agents.get_completion(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                    "id": "id",
                    "created_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "images": ["string"],
                }
            ],
            model="model",
        )
        assert_matches_type(AgentGetCompletionResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_completion(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.agents.with_raw_response.get_completion(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(AgentGetCompletionResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_completion(self, async_client: AsyncWayakAI) -> None:
        async with async_client.agents.with_streaming_response.get_completion(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(AgentGetCompletionResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_supported_models(self, async_client: AsyncWayakAI) -> None:
        agent = await async_client.agents.list_supported_models()
        assert_matches_type(AgentListSupportedModelsResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_supported_models(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.agents.with_raw_response.list_supported_models()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(AgentListSupportedModelsResponse, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_supported_models(self, async_client: AsyncWayakAI) -> None:
        async with async_client.agents.with_streaming_response.list_supported_models() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(AgentListSupportedModelsResponse, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_send_message_to_agent(self, async_client: AsyncWayakAI) -> None:
        agent = await async_client.agents.send_message_to_agent(
            agent_id="agentId",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_send_message_to_agent_with_all_params(self, async_client: AsyncWayakAI) -> None:
        agent = await async_client.agents.send_message_to_agent(
            agent_id="agentId",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                    "id": "id",
                    "created_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "images": ["string"],
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            file_ids=["string"],
            model="model",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            save_messages=True,
        )
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_send_message_to_agent(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.agents.with_raw_response.send_message_to_agent(
            agent_id="agentId",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_send_message_to_agent(self, async_client: AsyncWayakAI) -> None:
        async with async_client.agents.with_streaming_response.send_message_to_agent(
            agent_id="agentId",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(PersistentMessage, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_send_message_to_agent(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.with_raw_response.send_message_to_agent(
                agent_id="",
                messages=[
                    {
                        "content": "content",
                        "role": "role",
                    }
                ],
                thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_send_message_to_wayak(self, async_client: AsyncWayakAI) -> None:
        agent = await async_client.agents.send_message_to_wayak(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_send_message_to_wayak_with_all_params(self, async_client: AsyncWayakAI) -> None:
        agent = await async_client.agents.send_message_to_wayak(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                    "id": "id",
                    "created_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "images": ["string"],
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            file_ids=["string"],
            model="model",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            save_messages=True,
        )
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_send_message_to_wayak(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.agents.with_raw_response.send_message_to_wayak(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_send_message_to_wayak(self, async_client: AsyncWayakAI) -> None:
        async with async_client.agents.with_streaming_response.send_message_to_wayak(
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(PersistentMessage, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

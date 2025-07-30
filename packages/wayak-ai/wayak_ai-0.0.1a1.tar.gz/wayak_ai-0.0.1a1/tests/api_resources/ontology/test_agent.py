# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from wayak_ai import WayakAI, AsyncWayakAI
from tests.utils import assert_matches_type
from wayak_ai.types import PersistentMessage
from wayak_ai._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAgent:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_chat(self, client: WayakAI) -> None:
        agent = client.ontology.agent.chat(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_chat_with_all_params(self, client: WayakAI) -> None:
        agent = client.ontology.agent.chat(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                    "id": "id",
                    "created_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "images": ["string"],
                }
            ],
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            file_ids=["string"],
            model="model",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            save_messages=True,
        )
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_chat(self, client: WayakAI) -> None:
        response = client.ontology.agent.with_raw_response.chat(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_chat(self, client: WayakAI) -> None:
        with client.ontology.agent.with_streaming_response.chat(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(PersistentMessage, agent, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAgent:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_chat(self, async_client: AsyncWayakAI) -> None:
        agent = await async_client.ontology.agent.chat(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_chat_with_all_params(self, async_client: AsyncWayakAI) -> None:
        agent = await async_client.ontology.agent.chat(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                    "id": "id",
                    "created_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "images": ["string"],
                }
            ],
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            file_ids=["string"],
            model="model",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            save_messages=True,
        )
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_chat(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.agent.with_raw_response.chat(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(PersistentMessage, agent, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_chat(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.agent.with_streaming_response.chat(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            messages=[
                {
                    "content": "content",
                    "role": "role",
                }
            ],
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            thread_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(PersistentMessage, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from wayak_ai import WayakAI, AsyncWayakAI
from tests.utils import assert_matches_type
from wayak_ai.types import PersistentBrain, BrainListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBrains:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: WayakAI) -> None:
        brain = client.brains.create(
            backstory="backstory",
            creator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            goal="goal",
            name="name",
            role="role",
        )
        assert_matches_type(PersistentBrain, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: WayakAI) -> None:
        brain = client.brains.create(
            backstory="backstory",
            creator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            goal="goal",
            name="name",
            role="role",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            prebuilt_tools=["string"],
        )
        assert_matches_type(PersistentBrain, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: WayakAI) -> None:
        response = client.brains.with_raw_response.create(
            backstory="backstory",
            creator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            goal="goal",
            name="name",
            role="role",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        brain = response.parse()
        assert_matches_type(PersistentBrain, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: WayakAI) -> None:
        with client.brains.with_streaming_response.create(
            backstory="backstory",
            creator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            goal="goal",
            name="name",
            role="role",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            brain = response.parse()
            assert_matches_type(PersistentBrain, brain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: WayakAI) -> None:
        brain = client.brains.update(
            brain_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PersistentBrain, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: WayakAI) -> None:
        brain = client.brains.update(
            brain_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            backstory="backstory",
            goal="goal",
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            prebuilt_tools=["string"],
            role="role",
        )
        assert_matches_type(PersistentBrain, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: WayakAI) -> None:
        response = client.brains.with_raw_response.update(
            brain_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        brain = response.parse()
        assert_matches_type(PersistentBrain, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: WayakAI) -> None:
        with client.brains.with_streaming_response.update(
            brain_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            brain = response.parse()
            assert_matches_type(PersistentBrain, brain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `brain_id` but received ''"):
            client.brains.with_raw_response.update(
                brain_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: WayakAI) -> None:
        brain = client.brains.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BrainListResponse, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: WayakAI) -> None:
        response = client.brains.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        brain = response.parse()
        assert_matches_type(BrainListResponse, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: WayakAI) -> None:
        with client.brains.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            brain = response.parse()
            assert_matches_type(BrainListResponse, brain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.brains.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: WayakAI) -> None:
        brain = client.brains.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert brain is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: WayakAI) -> None:
        response = client.brains.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        brain = response.parse()
        assert brain is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: WayakAI) -> None:
        with client.brains.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            brain = response.parse()
            assert brain is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `brain_id` but received ''"):
            client.brains.with_raw_response.delete(
                "",
            )


class TestAsyncBrains:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncWayakAI) -> None:
        brain = await async_client.brains.create(
            backstory="backstory",
            creator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            goal="goal",
            name="name",
            role="role",
        )
        assert_matches_type(PersistentBrain, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncWayakAI) -> None:
        brain = await async_client.brains.create(
            backstory="backstory",
            creator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            goal="goal",
            name="name",
            role="role",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            prebuilt_tools=["string"],
        )
        assert_matches_type(PersistentBrain, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.brains.with_raw_response.create(
            backstory="backstory",
            creator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            goal="goal",
            name="name",
            role="role",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        brain = await response.parse()
        assert_matches_type(PersistentBrain, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncWayakAI) -> None:
        async with async_client.brains.with_streaming_response.create(
            backstory="backstory",
            creator_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            goal="goal",
            name="name",
            role="role",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            brain = await response.parse()
            assert_matches_type(PersistentBrain, brain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncWayakAI) -> None:
        brain = await async_client.brains.update(
            brain_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PersistentBrain, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncWayakAI) -> None:
        brain = await async_client.brains.update(
            brain_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            backstory="backstory",
            goal="goal",
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            prebuilt_tools=["string"],
            role="role",
        )
        assert_matches_type(PersistentBrain, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.brains.with_raw_response.update(
            brain_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        brain = await response.parse()
        assert_matches_type(PersistentBrain, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncWayakAI) -> None:
        async with async_client.brains.with_streaming_response.update(
            brain_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            brain = await response.parse()
            assert_matches_type(PersistentBrain, brain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `brain_id` but received ''"):
            await async_client.brains.with_raw_response.update(
                brain_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncWayakAI) -> None:
        brain = await async_client.brains.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(BrainListResponse, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.brains.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        brain = await response.parse()
        assert_matches_type(BrainListResponse, brain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncWayakAI) -> None:
        async with async_client.brains.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            brain = await response.parse()
            assert_matches_type(BrainListResponse, brain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.brains.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncWayakAI) -> None:
        brain = await async_client.brains.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert brain is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.brains.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        brain = await response.parse()
        assert brain is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncWayakAI) -> None:
        async with async_client.brains.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            brain = await response.parse()
            assert brain is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `brain_id` but received ''"):
            await async_client.brains.with_raw_response.delete(
                "",
            )

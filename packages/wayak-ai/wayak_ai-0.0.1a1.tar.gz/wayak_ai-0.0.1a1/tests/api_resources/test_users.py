# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from wayak_ai import WayakAI, AsyncWayakAI
from tests.utils import assert_matches_type
from wayak_ai.types import (
    UserCreateResponse,
    UserListThreadsResponse,
    UserListContextsResponse,
    UserListProjectsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: WayakAI) -> None:
        user = client.users.create(
            email="email",
        )
        assert_matches_type(UserCreateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: WayakAI) -> None:
        user = client.users.create(
            email="email",
            name="name",
            password="password",
        )
        assert_matches_type(UserCreateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: WayakAI) -> None:
        response = client.users.with_raw_response.create(
            email="email",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserCreateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: WayakAI) -> None:
        with client.users.with_streaming_response.create(
            email="email",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserCreateResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list_contexts(self, client: WayakAI) -> None:
        user = client.users.list_contexts(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(UserListContextsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_contexts(self, client: WayakAI) -> None:
        response = client.users.with_raw_response.list_contexts(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserListContextsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_contexts(self, client: WayakAI) -> None:
        with client.users.with_streaming_response.list_contexts(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserListContextsResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list_contexts(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.users.with_raw_response.list_contexts(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list_projects(self, client: WayakAI) -> None:
        user = client.users.list_projects(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(UserListProjectsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_projects_with_all_params(self, client: WayakAI) -> None:
        user = client.users.list_projects(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            limit=0,
        )
        assert_matches_type(UserListProjectsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_projects(self, client: WayakAI) -> None:
        response = client.users.with_raw_response.list_projects(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserListProjectsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_projects(self, client: WayakAI) -> None:
        with client.users.with_streaming_response.list_projects(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserListProjectsResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list_projects(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.users.with_raw_response.list_projects(
                user_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list_threads(self, client: WayakAI) -> None:
        user = client.users.list_threads(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(UserListThreadsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_threads_with_all_params(self, client: WayakAI) -> None:
        user = client.users.list_threads(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            limit=0,
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(UserListThreadsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_threads(self, client: WayakAI) -> None:
        response = client.users.with_raw_response.list_threads(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserListThreadsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_threads(self, client: WayakAI) -> None:
        with client.users.with_streaming_response.list_threads(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserListThreadsResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list_threads(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.users.with_raw_response.list_threads(
                user_id="",
            )


class TestAsyncUsers:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncWayakAI) -> None:
        user = await async_client.users.create(
            email="email",
        )
        assert_matches_type(UserCreateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncWayakAI) -> None:
        user = await async_client.users.create(
            email="email",
            name="name",
            password="password",
        )
        assert_matches_type(UserCreateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.users.with_raw_response.create(
            email="email",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserCreateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncWayakAI) -> None:
        async with async_client.users.with_streaming_response.create(
            email="email",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserCreateResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_contexts(self, async_client: AsyncWayakAI) -> None:
        user = await async_client.users.list_contexts(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(UserListContextsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_contexts(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.users.with_raw_response.list_contexts(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserListContextsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_contexts(self, async_client: AsyncWayakAI) -> None:
        async with async_client.users.with_streaming_response.list_contexts(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserListContextsResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list_contexts(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.users.with_raw_response.list_contexts(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_projects(self, async_client: AsyncWayakAI) -> None:
        user = await async_client.users.list_projects(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(UserListProjectsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_projects_with_all_params(self, async_client: AsyncWayakAI) -> None:
        user = await async_client.users.list_projects(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            limit=0,
        )
        assert_matches_type(UserListProjectsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_projects(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.users.with_raw_response.list_projects(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserListProjectsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_projects(self, async_client: AsyncWayakAI) -> None:
        async with async_client.users.with_streaming_response.list_projects(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserListProjectsResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list_projects(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.users.with_raw_response.list_projects(
                user_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_threads(self, async_client: AsyncWayakAI) -> None:
        user = await async_client.users.list_threads(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(UserListThreadsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_threads_with_all_params(self, async_client: AsyncWayakAI) -> None:
        user = await async_client.users.list_threads(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            limit=0,
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(UserListThreadsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_threads(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.users.with_raw_response.list_threads(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserListThreadsResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_threads(self, async_client: AsyncWayakAI) -> None:
        async with async_client.users.with_streaming_response.list_threads(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserListThreadsResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list_threads(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.users.with_raw_response.list_threads(
                user_id="",
            )

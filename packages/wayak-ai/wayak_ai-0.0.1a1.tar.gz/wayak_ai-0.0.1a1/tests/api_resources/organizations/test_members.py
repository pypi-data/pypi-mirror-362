# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from wayak_ai import WayakAI, AsyncWayakAI
from tests.utils import assert_matches_type
from wayak_ai.types.organizations import (
    MemberAddResponse,
    MemberListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMembers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: WayakAI) -> None:
        member = client.organizations.members.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MemberListResponse, member, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: WayakAI) -> None:
        response = client.organizations.members.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = response.parse()
        assert_matches_type(MemberListResponse, member, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: WayakAI) -> None:
        with client.organizations.members.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = response.parse()
            assert_matches_type(MemberListResponse, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.organizations.members.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_add(self, client: WayakAI) -> None:
        member = client.organizations.members.add(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            role="OWNER",
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MemberAddResponse, member, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_add(self, client: WayakAI) -> None:
        response = client.organizations.members.with_raw_response.add(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            role="OWNER",
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = response.parse()
        assert_matches_type(MemberAddResponse, member, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_add(self, client: WayakAI) -> None:
        with client.organizations.members.with_streaming_response.add(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            role="OWNER",
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = response.parse()
            assert_matches_type(MemberAddResponse, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_add(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.organizations.members.with_raw_response.add(
                org_id="",
                current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                role="OWNER",
                user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_remove(self, client: WayakAI) -> None:
        member = client.organizations.members.remove(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, member, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_remove(self, client: WayakAI) -> None:
        response = client.organizations.members.with_raw_response.remove(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = response.parse()
        assert_matches_type(object, member, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_remove(self, client: WayakAI) -> None:
        with client.organizations.members.with_streaming_response.remove(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = response.parse()
            assert_matches_type(object, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_remove(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.organizations.members.with_raw_response.remove(
                user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                org_id="",
                current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.organizations.members.with_raw_response.remove(
                user_id="",
                org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )


class TestAsyncMembers:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncWayakAI) -> None:
        member = await async_client.organizations.members.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MemberListResponse, member, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.organizations.members.with_raw_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = await response.parse()
        assert_matches_type(MemberListResponse, member, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncWayakAI) -> None:
        async with async_client.organizations.members.with_streaming_response.list(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = await response.parse()
            assert_matches_type(MemberListResponse, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.organizations.members.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_add(self, async_client: AsyncWayakAI) -> None:
        member = await async_client.organizations.members.add(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            role="OWNER",
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MemberAddResponse, member, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_add(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.organizations.members.with_raw_response.add(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            role="OWNER",
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = await response.parse()
        assert_matches_type(MemberAddResponse, member, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncWayakAI) -> None:
        async with async_client.organizations.members.with_streaming_response.add(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            role="OWNER",
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = await response.parse()
            assert_matches_type(MemberAddResponse, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_add(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.organizations.members.with_raw_response.add(
                org_id="",
                current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                role="OWNER",
                user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_remove(self, async_client: AsyncWayakAI) -> None:
        member = await async_client.organizations.members.remove(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(object, member, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_remove(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.organizations.members.with_raw_response.remove(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        member = await response.parse()
        assert_matches_type(object, member, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_remove(self, async_client: AsyncWayakAI) -> None:
        async with async_client.organizations.members.with_streaming_response.remove(
            user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            member = await response.parse()
            assert_matches_type(object, member, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_remove(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.organizations.members.with_raw_response.remove(
                user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                org_id="",
                current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.organizations.members.with_raw_response.remove(
                user_id="",
                org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                current_user_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            )

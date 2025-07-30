# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from wayak_ai import WayakAI, AsyncWayakAI
from tests.utils import assert_matches_type
from wayak_ai.types.users import PersistentUserProfile

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProfile:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_find_by_email(self, client: WayakAI) -> None:
        profile = client.users.profile.find_by_email(
            email="email",
        )
        assert_matches_type(PersistentUserProfile, profile, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_find_by_email(self, client: WayakAI) -> None:
        response = client.users.profile.with_raw_response.find_by_email(
            email="email",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = response.parse()
        assert_matches_type(PersistentUserProfile, profile, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_find_by_email(self, client: WayakAI) -> None:
        with client.users.profile.with_streaming_response.find_by_email(
            email="email",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = response.parse()
            assert_matches_type(PersistentUserProfile, profile, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncProfile:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_find_by_email(self, async_client: AsyncWayakAI) -> None:
        profile = await async_client.users.profile.find_by_email(
            email="email",
        )
        assert_matches_type(PersistentUserProfile, profile, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_find_by_email(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.users.profile.with_raw_response.find_by_email(
            email="email",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        profile = await response.parse()
        assert_matches_type(PersistentUserProfile, profile, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_find_by_email(self, async_client: AsyncWayakAI) -> None:
        async with async_client.users.profile.with_streaming_response.find_by_email(
            email="email",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            profile = await response.parse()
            assert_matches_type(PersistentUserProfile, profile, path=["response"])

        assert cast(Any, response.is_closed) is True

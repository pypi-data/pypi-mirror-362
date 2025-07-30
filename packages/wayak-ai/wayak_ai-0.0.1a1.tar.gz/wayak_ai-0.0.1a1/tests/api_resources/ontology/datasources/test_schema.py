# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from wayak_ai import WayakAI, AsyncWayakAI
from tests.utils import assert_matches_type
from wayak_ai.types.ontology.datasources import DataSourceModel

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSchema:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_refresh(self, client: WayakAI) -> None:
        schema = client.ontology.datasources.schema.refresh(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DataSourceModel, schema, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_refresh(self, client: WayakAI) -> None:
        response = client.ontology.datasources.schema.with_raw_response.refresh(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        schema = response.parse()
        assert_matches_type(DataSourceModel, schema, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_refresh(self, client: WayakAI) -> None:
        with client.ontology.datasources.schema.with_streaming_response.refresh(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            schema = response.parse()
            assert_matches_type(DataSourceModel, schema, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_refresh(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_id` but received ''"):
            client.ontology.datasources.schema.with_raw_response.refresh(
                "",
            )


class TestAsyncSchema:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_refresh(self, async_client: AsyncWayakAI) -> None:
        schema = await async_client.ontology.datasources.schema.refresh(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DataSourceModel, schema, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_refresh(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.datasources.schema.with_raw_response.refresh(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        schema = await response.parse()
        assert_matches_type(DataSourceModel, schema, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_refresh(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.datasources.schema.with_streaming_response.refresh(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            schema = await response.parse()
            assert_matches_type(DataSourceModel, schema, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_refresh(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_id` but received ''"):
            await async_client.ontology.datasources.schema.with_raw_response.refresh(
                "",
            )

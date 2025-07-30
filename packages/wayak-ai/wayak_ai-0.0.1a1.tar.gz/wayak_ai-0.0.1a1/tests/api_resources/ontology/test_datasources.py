# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from wayak_ai import WayakAI, AsyncWayakAI
from tests.utils import assert_matches_type
from wayak_ai.types.ontology import DatasourceListResponse, DatasourceTestConnectionResponse
from wayak_ai.types.ontology.datasources import DataSourceModel

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDatasources:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: WayakAI) -> None:
        datasource = client.ontology.datasources.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DataSourceModel, datasource, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: WayakAI) -> None:
        response = client.ontology.datasources.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        datasource = response.parse()
        assert_matches_type(DataSourceModel, datasource, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: WayakAI) -> None:
        with client.ontology.datasources.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            datasource = response.parse()
            assert_matches_type(DataSourceModel, datasource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_id` but received ''"):
            client.ontology.datasources.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: WayakAI) -> None:
        datasource = client.ontology.datasources.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DatasourceListResponse, datasource, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: WayakAI) -> None:
        response = client.ontology.datasources.with_raw_response.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        datasource = response.parse()
        assert_matches_type(DatasourceListResponse, datasource, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: WayakAI) -> None:
        with client.ontology.datasources.with_streaming_response.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            datasource = response.parse()
            assert_matches_type(DatasourceListResponse, datasource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_test_connection(self, client: WayakAI) -> None:
        datasource = client.ontology.datasources.test_connection(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DatasourceTestConnectionResponse, datasource, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_test_connection(self, client: WayakAI) -> None:
        response = client.ontology.datasources.with_raw_response.test_connection(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        datasource = response.parse()
        assert_matches_type(DatasourceTestConnectionResponse, datasource, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_test_connection(self, client: WayakAI) -> None:
        with client.ontology.datasources.with_streaming_response.test_connection(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            datasource = response.parse()
            assert_matches_type(DatasourceTestConnectionResponse, datasource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_test_connection(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_id` but received ''"):
            client.ontology.datasources.with_raw_response.test_connection(
                "",
            )


class TestAsyncDatasources:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncWayakAI) -> None:
        datasource = await async_client.ontology.datasources.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DataSourceModel, datasource, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.datasources.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        datasource = await response.parse()
        assert_matches_type(DataSourceModel, datasource, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.datasources.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            datasource = await response.parse()
            assert_matches_type(DataSourceModel, datasource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_id` but received ''"):
            await async_client.ontology.datasources.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncWayakAI) -> None:
        datasource = await async_client.ontology.datasources.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DatasourceListResponse, datasource, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.datasources.with_raw_response.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        datasource = await response.parse()
        assert_matches_type(DatasourceListResponse, datasource, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.datasources.with_streaming_response.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            datasource = await response.parse()
            assert_matches_type(DatasourceListResponse, datasource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_test_connection(self, async_client: AsyncWayakAI) -> None:
        datasource = await async_client.ontology.datasources.test_connection(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DatasourceTestConnectionResponse, datasource, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_test_connection(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.datasources.with_raw_response.test_connection(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        datasource = await response.parse()
        assert_matches_type(DatasourceTestConnectionResponse, datasource, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_test_connection(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.datasources.with_streaming_response.test_connection(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            datasource = await response.parse()
            assert_matches_type(DatasourceTestConnectionResponse, datasource, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_test_connection(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_id` but received ''"):
            await async_client.ontology.datasources.with_raw_response.test_connection(
                "",
            )

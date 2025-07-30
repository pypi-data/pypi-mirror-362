# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from wayak_ai import WayakAI, AsyncWayakAI
from tests.utils import assert_matches_type
from wayak_ai.types import OntologyExecuteQueryResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOntology:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_execute_query(self, client: WayakAI) -> None:
        ontology = client.ontology.execute_query(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            sql_query="sql_query",
        )
        assert_matches_type(OntologyExecuteQueryResponse, ontology, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_execute_query(self, client: WayakAI) -> None:
        response = client.ontology.with_raw_response.execute_query(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            sql_query="sql_query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ontology = response.parse()
        assert_matches_type(OntologyExecuteQueryResponse, ontology, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_execute_query(self, client: WayakAI) -> None:
        with client.ontology.with_streaming_response.execute_query(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            sql_query="sql_query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ontology = response.parse()
            assert_matches_type(OntologyExecuteQueryResponse, ontology, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncOntology:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_execute_query(self, async_client: AsyncWayakAI) -> None:
        ontology = await async_client.ontology.execute_query(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            sql_query="sql_query",
        )
        assert_matches_type(OntologyExecuteQueryResponse, ontology, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_execute_query(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.with_raw_response.execute_query(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            sql_query="sql_query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ontology = await response.parse()
        assert_matches_type(OntologyExecuteQueryResponse, ontology, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_execute_query(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.with_streaming_response.execute_query(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            sql_query="sql_query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ontology = await response.parse()
            assert_matches_type(OntologyExecuteQueryResponse, ontology, path=["response"])

        assert cast(Any, response.is_closed) is True

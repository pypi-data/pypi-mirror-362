# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from wayak_ai import WayakAI, AsyncWayakAI
from tests.utils import assert_matches_type
from wayak_ai.types.ontology import (
    MetricModel,
    MetricListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMetrics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: WayakAI) -> None:
        metric = client.ontology.metrics.create(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            query="query",
            title="title",
            vizualisation="graph",
        )
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: WayakAI) -> None:
        metric = client.ontology.metrics.create(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            query="query",
            title="title",
            vizualisation="graph",
            chart_config={"foo": "bar"},
            code="code",
            description="description",
            status="draft",
        )
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: WayakAI) -> None:
        response = client.ontology.metrics.with_raw_response.create(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            query="query",
            title="title",
            vizualisation="graph",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = response.parse()
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: WayakAI) -> None:
        with client.ontology.metrics.with_streaming_response.create(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            query="query",
            title="title",
            vizualisation="graph",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = response.parse()
            assert_matches_type(MetricModel, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: WayakAI) -> None:
        metric = client.ontology.metrics.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: WayakAI) -> None:
        response = client.ontology.metrics.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = response.parse()
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: WayakAI) -> None:
        with client.ontology.metrics.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = response.parse()
            assert_matches_type(MetricModel, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_id` but received ''"):
            client.ontology.metrics.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: WayakAI) -> None:
        metric = client.ontology.metrics.update(
            metric_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: WayakAI) -> None:
        metric = client.ontology.metrics.update(
            metric_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            chart_config={"foo": "bar"},
            code="code",
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            query="query",
            status="draft",
            title="title",
            vizualisation="graph",
        )
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: WayakAI) -> None:
        response = client.ontology.metrics.with_raw_response.update(
            metric_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = response.parse()
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: WayakAI) -> None:
        with client.ontology.metrics.with_streaming_response.update(
            metric_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = response.parse()
            assert_matches_type(MetricModel, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_id` but received ''"):
            client.ontology.metrics.with_raw_response.update(
                metric_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: WayakAI) -> None:
        metric = client.ontology.metrics.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MetricListResponse, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: WayakAI) -> None:
        response = client.ontology.metrics.with_raw_response.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = response.parse()
        assert_matches_type(MetricListResponse, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: WayakAI) -> None:
        with client.ontology.metrics.with_streaming_response.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = response.parse()
            assert_matches_type(MetricListResponse, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: WayakAI) -> None:
        metric = client.ontology.metrics.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: WayakAI) -> None:
        response = client.ontology.metrics.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = response.parse()
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: WayakAI) -> None:
        with client.ontology.metrics.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = response.parse()
            assert_matches_type(MetricModel, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_id` but received ''"):
            client.ontology.metrics.with_raw_response.delete(
                "",
            )


class TestAsyncMetrics:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncWayakAI) -> None:
        metric = await async_client.ontology.metrics.create(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            query="query",
            title="title",
            vizualisation="graph",
        )
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncWayakAI) -> None:
        metric = await async_client.ontology.metrics.create(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            query="query",
            title="title",
            vizualisation="graph",
            chart_config={"foo": "bar"},
            code="code",
            description="description",
            status="draft",
        )
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.metrics.with_raw_response.create(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            query="query",
            title="title",
            vizualisation="graph",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = await response.parse()
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.metrics.with_streaming_response.create(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            query="query",
            title="title",
            vizualisation="graph",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = await response.parse()
            assert_matches_type(MetricModel, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncWayakAI) -> None:
        metric = await async_client.ontology.metrics.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.metrics.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = await response.parse()
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.metrics.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = await response.parse()
            assert_matches_type(MetricModel, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_id` but received ''"):
            await async_client.ontology.metrics.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncWayakAI) -> None:
        metric = await async_client.ontology.metrics.update(
            metric_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncWayakAI) -> None:
        metric = await async_client.ontology.metrics.update(
            metric_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            chart_config={"foo": "bar"},
            code="code",
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            query="query",
            status="draft",
            title="title",
            vizualisation="graph",
        )
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.metrics.with_raw_response.update(
            metric_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = await response.parse()
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.metrics.with_streaming_response.update(
            metric_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = await response.parse()
            assert_matches_type(MetricModel, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_id` but received ''"):
            await async_client.ontology.metrics.with_raw_response.update(
                metric_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncWayakAI) -> None:
        metric = await async_client.ontology.metrics.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MetricListResponse, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.metrics.with_raw_response.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = await response.parse()
        assert_matches_type(MetricListResponse, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.metrics.with_streaming_response.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = await response.parse()
            assert_matches_type(MetricListResponse, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncWayakAI) -> None:
        metric = await async_client.ontology.metrics.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.metrics.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = await response.parse()
        assert_matches_type(MetricModel, metric, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.metrics.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = await response.parse()
            assert_matches_type(MetricModel, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_id` but received ''"):
            await async_client.ontology.metrics.with_raw_response.delete(
                "",
            )

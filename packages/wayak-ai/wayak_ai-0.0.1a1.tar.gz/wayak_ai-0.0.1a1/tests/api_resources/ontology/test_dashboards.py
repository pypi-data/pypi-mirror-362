# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from wayak_ai import WayakAI, AsyncWayakAI
from tests.utils import assert_matches_type
from wayak_ai.types.ontology import (
    DashboardModel,
    DashboardListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDashboards:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: WayakAI) -> None:
        dashboard = client.ontology.dashboards.create(
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: WayakAI) -> None:
        dashboard = client.ontology.dashboards.create(
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            layout=[
                {
                    "metric_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "position": {
                        "h": 0,
                        "w": 0,
                        "x": 0,
                        "y": 0,
                    },
                }
            ],
        )
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: WayakAI) -> None:
        response = client.ontology.dashboards.with_raw_response.create(
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dashboard = response.parse()
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: WayakAI) -> None:
        with client.ontology.dashboards.with_streaming_response.create(
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dashboard = response.parse()
            assert_matches_type(DashboardModel, dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: WayakAI) -> None:
        dashboard = client.ontology.dashboards.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: WayakAI) -> None:
        response = client.ontology.dashboards.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dashboard = response.parse()
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: WayakAI) -> None:
        with client.ontology.dashboards.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dashboard = response.parse()
            assert_matches_type(DashboardModel, dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            client.ontology.dashboards.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: WayakAI) -> None:
        dashboard = client.ontology.dashboards.update(
            dashboard_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: WayakAI) -> None:
        dashboard = client.ontology.dashboards.update(
            dashboard_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            layout=[
                {
                    "metric_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "position": {
                        "h": 0,
                        "w": 0,
                        "x": 0,
                        "y": 0,
                    },
                }
            ],
            name="name",
        )
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: WayakAI) -> None:
        response = client.ontology.dashboards.with_raw_response.update(
            dashboard_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dashboard = response.parse()
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: WayakAI) -> None:
        with client.ontology.dashboards.with_streaming_response.update(
            dashboard_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dashboard = response.parse()
            assert_matches_type(DashboardModel, dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            client.ontology.dashboards.with_raw_response.update(
                dashboard_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: WayakAI) -> None:
        dashboard = client.ontology.dashboards.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DashboardListResponse, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: WayakAI) -> None:
        response = client.ontology.dashboards.with_raw_response.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dashboard = response.parse()
        assert_matches_type(DashboardListResponse, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: WayakAI) -> None:
        with client.ontology.dashboards.with_streaming_response.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dashboard = response.parse()
            assert_matches_type(DashboardListResponse, dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: WayakAI) -> None:
        dashboard = client.ontology.dashboards.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: WayakAI) -> None:
        response = client.ontology.dashboards.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dashboard = response.parse()
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: WayakAI) -> None:
        with client.ontology.dashboards.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dashboard = response.parse()
            assert_matches_type(DashboardModel, dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            client.ontology.dashboards.with_raw_response.delete(
                "",
            )


class TestAsyncDashboards:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncWayakAI) -> None:
        dashboard = await async_client.ontology.dashboards.create(
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncWayakAI) -> None:
        dashboard = await async_client.ontology.dashboards.create(
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            layout=[
                {
                    "metric_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "position": {
                        "h": 0,
                        "w": 0,
                        "x": 0,
                        "y": 0,
                    },
                }
            ],
        )
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.dashboards.with_raw_response.create(
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dashboard = await response.parse()
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.dashboards.with_streaming_response.create(
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dashboard = await response.parse()
            assert_matches_type(DashboardModel, dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncWayakAI) -> None:
        dashboard = await async_client.ontology.dashboards.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.dashboards.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dashboard = await response.parse()
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.dashboards.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dashboard = await response.parse()
            assert_matches_type(DashboardModel, dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            await async_client.ontology.dashboards.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncWayakAI) -> None:
        dashboard = await async_client.ontology.dashboards.update(
            dashboard_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncWayakAI) -> None:
        dashboard = await async_client.ontology.dashboards.update(
            dashboard_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            layout=[
                {
                    "metric_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "position": {
                        "h": 0,
                        "w": 0,
                        "x": 0,
                        "y": 0,
                    },
                }
            ],
            name="name",
        )
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.dashboards.with_raw_response.update(
            dashboard_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dashboard = await response.parse()
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.dashboards.with_streaming_response.update(
            dashboard_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dashboard = await response.parse()
            assert_matches_type(DashboardModel, dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            await async_client.ontology.dashboards.with_raw_response.update(
                dashboard_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncWayakAI) -> None:
        dashboard = await async_client.ontology.dashboards.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DashboardListResponse, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.dashboards.with_raw_response.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dashboard = await response.parse()
        assert_matches_type(DashboardListResponse, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.dashboards.with_streaming_response.list(
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dashboard = await response.parse()
            assert_matches_type(DashboardListResponse, dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncWayakAI) -> None:
        dashboard = await async_client.ontology.dashboards.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.dashboards.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dashboard = await response.parse()
        assert_matches_type(DashboardModel, dashboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.dashboards.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dashboard = await response.parse()
            assert_matches_type(DashboardModel, dashboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `dashboard_id` but received ''"):
            await async_client.ontology.dashboards.with_raw_response.delete(
                "",
            )

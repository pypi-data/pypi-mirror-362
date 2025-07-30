# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from wayak_ai import WayakAI, AsyncWayakAI
from tests.utils import assert_matches_type
from wayak_ai._utils import parse_datetime
from wayak_ai.types.ontology.datasources import (
    DataSourceModel,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClickhouse:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: WayakAI) -> None:
        clickhouse = client.ontology.datasources.clickhouse.create(
            config={
                "host": "host",
                "password": "password",
                "username": "username",
            },
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
        )
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: WayakAI) -> None:
        clickhouse = client.ontology.datasources.clickhouse.create(
            config={
                "host": "host",
                "password": "password",
                "username": "username",
                "port": 0,
            },
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            schema="schema",
        )
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: WayakAI) -> None:
        response = client.ontology.datasources.clickhouse.with_raw_response.create(
            config={
                "host": "host",
                "password": "password",
                "username": "username",
            },
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        clickhouse = response.parse()
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: WayakAI) -> None:
        with client.ontology.datasources.clickhouse.with_streaming_response.create(
            config={
                "host": "host",
                "password": "password",
                "username": "username",
            },
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            clickhouse = response.parse()
            assert_matches_type(DataSourceModel, clickhouse, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: WayakAI) -> None:
        clickhouse = client.ontology.datasources.clickhouse.update(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
        )
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: WayakAI) -> None:
        clickhouse = client.ontology.datasources.clickhouse.update(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            schema="schema",
        )
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: WayakAI) -> None:
        response = client.ontology.datasources.clickhouse.with_raw_response.update(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        clickhouse = response.parse()
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: WayakAI) -> None:
        with client.ontology.datasources.clickhouse.with_streaming_response.update(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            clickhouse = response.parse()
            assert_matches_type(DataSourceModel, clickhouse, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_id` but received ''"):
            client.ontology.datasources.clickhouse.with_raw_response.update(
                datasource_id="",
                config={"foo": "bar"},
                created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
                edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
                name="name",
                org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                type="clickhouse",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: WayakAI) -> None:
        clickhouse = client.ontology.datasources.clickhouse.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: WayakAI) -> None:
        response = client.ontology.datasources.clickhouse.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        clickhouse = response.parse()
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: WayakAI) -> None:
        with client.ontology.datasources.clickhouse.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            clickhouse = response.parse()
            assert_matches_type(DataSourceModel, clickhouse, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: WayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_id` but received ''"):
            client.ontology.datasources.clickhouse.with_raw_response.delete(
                "",
            )


class TestAsyncClickhouse:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncWayakAI) -> None:
        clickhouse = await async_client.ontology.datasources.clickhouse.create(
            config={
                "host": "host",
                "password": "password",
                "username": "username",
            },
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
        )
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncWayakAI) -> None:
        clickhouse = await async_client.ontology.datasources.clickhouse.create(
            config={
                "host": "host",
                "password": "password",
                "username": "username",
                "port": 0,
            },
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            schema="schema",
        )
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.datasources.clickhouse.with_raw_response.create(
            config={
                "host": "host",
                "password": "password",
                "username": "username",
            },
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        clickhouse = await response.parse()
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.datasources.clickhouse.with_streaming_response.create(
            config={
                "host": "host",
                "password": "password",
                "username": "username",
            },
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            clickhouse = await response.parse()
            assert_matches_type(DataSourceModel, clickhouse, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncWayakAI) -> None:
        clickhouse = await async_client.ontology.datasources.clickhouse.update(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
        )
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncWayakAI) -> None:
        clickhouse = await async_client.ontology.datasources.clickhouse.update(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            description="description",
            schema="schema",
        )
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.datasources.clickhouse.with_raw_response.update(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        clickhouse = await response.parse()
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.datasources.clickhouse.with_streaming_response.update(
            datasource_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            config={"foo": "bar"},
            created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            name="name",
            org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            type="clickhouse",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            clickhouse = await response.parse()
            assert_matches_type(DataSourceModel, clickhouse, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_id` but received ''"):
            await async_client.ontology.datasources.clickhouse.with_raw_response.update(
                datasource_id="",
                config={"foo": "bar"},
                created_at=parse_datetime("2019-12-27T18:11:19.117Z"),
                edited_at=parse_datetime("2019-12-27T18:11:19.117Z"),
                name="name",
                org_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                type="clickhouse",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncWayakAI) -> None:
        clickhouse = await async_client.ontology.datasources.clickhouse.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncWayakAI) -> None:
        response = await async_client.ontology.datasources.clickhouse.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        clickhouse = await response.parse()
        assert_matches_type(DataSourceModel, clickhouse, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncWayakAI) -> None:
        async with async_client.ontology.datasources.clickhouse.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            clickhouse = await response.parse()
            assert_matches_type(DataSourceModel, clickhouse, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncWayakAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `datasource_id` but received ''"):
            await async_client.ontology.datasources.clickhouse.with_raw_response.delete(
                "",
            )

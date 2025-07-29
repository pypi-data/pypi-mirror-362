# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from gradientai import GradientAI, AsyncGradientAI
from tests.utils import assert_matches_type
from gradientai.types.agents import (
    RouteAddResponse,
    RouteViewResponse,
    RouteDeleteResponse,
    RouteUpdateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRoutes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: GradientAI) -> None:
        route = client.agents.routes.update(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
        )
        assert_matches_type(RouteUpdateResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: GradientAI) -> None:
        route = client.agents.routes.update(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
            body_child_agent_uuid="child_agent_uuid",
            if_case="if_case",
            body_parent_agent_uuid="parent_agent_uuid",
            route_name="route_name",
            uuid="uuid",
        )
        assert_matches_type(RouteUpdateResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: GradientAI) -> None:
        response = client.agents.routes.with_raw_response.update(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        route = response.parse()
        assert_matches_type(RouteUpdateResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: GradientAI) -> None:
        with client.agents.routes.with_streaming_response.update(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            route = response.parse()
            assert_matches_type(RouteUpdateResponse, route, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: GradientAI) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_parent_agent_uuid` but received ''"
        ):
            client.agents.routes.with_raw_response.update(
                path_child_agent_uuid="child_agent_uuid",
                path_parent_agent_uuid="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_child_agent_uuid` but received ''"):
            client.agents.routes.with_raw_response.update(
                path_child_agent_uuid="",
                path_parent_agent_uuid="parent_agent_uuid",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: GradientAI) -> None:
        route = client.agents.routes.delete(
            child_agent_uuid="child_agent_uuid",
            parent_agent_uuid="parent_agent_uuid",
        )
        assert_matches_type(RouteDeleteResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: GradientAI) -> None:
        response = client.agents.routes.with_raw_response.delete(
            child_agent_uuid="child_agent_uuid",
            parent_agent_uuid="parent_agent_uuid",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        route = response.parse()
        assert_matches_type(RouteDeleteResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: GradientAI) -> None:
        with client.agents.routes.with_streaming_response.delete(
            child_agent_uuid="child_agent_uuid",
            parent_agent_uuid="parent_agent_uuid",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            route = response.parse()
            assert_matches_type(RouteDeleteResponse, route, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: GradientAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `parent_agent_uuid` but received ''"):
            client.agents.routes.with_raw_response.delete(
                child_agent_uuid="child_agent_uuid",
                parent_agent_uuid="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `child_agent_uuid` but received ''"):
            client.agents.routes.with_raw_response.delete(
                child_agent_uuid="",
                parent_agent_uuid="parent_agent_uuid",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_add(self, client: GradientAI) -> None:
        route = client.agents.routes.add(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
        )
        assert_matches_type(RouteAddResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_add_with_all_params(self, client: GradientAI) -> None:
        route = client.agents.routes.add(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
            body_child_agent_uuid="child_agent_uuid",
            if_case="if_case",
            body_parent_agent_uuid="parent_agent_uuid",
            route_name="route_name",
        )
        assert_matches_type(RouteAddResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_add(self, client: GradientAI) -> None:
        response = client.agents.routes.with_raw_response.add(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        route = response.parse()
        assert_matches_type(RouteAddResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_add(self, client: GradientAI) -> None:
        with client.agents.routes.with_streaming_response.add(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            route = response.parse()
            assert_matches_type(RouteAddResponse, route, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_add(self, client: GradientAI) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_parent_agent_uuid` but received ''"
        ):
            client.agents.routes.with_raw_response.add(
                path_child_agent_uuid="child_agent_uuid",
                path_parent_agent_uuid="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_child_agent_uuid` but received ''"):
            client.agents.routes.with_raw_response.add(
                path_child_agent_uuid="",
                path_parent_agent_uuid="parent_agent_uuid",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_view(self, client: GradientAI) -> None:
        route = client.agents.routes.view(
            "uuid",
        )
        assert_matches_type(RouteViewResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_view(self, client: GradientAI) -> None:
        response = client.agents.routes.with_raw_response.view(
            "uuid",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        route = response.parse()
        assert_matches_type(RouteViewResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_view(self, client: GradientAI) -> None:
        with client.agents.routes.with_streaming_response.view(
            "uuid",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            route = response.parse()
            assert_matches_type(RouteViewResponse, route, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_view(self, client: GradientAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `uuid` but received ''"):
            client.agents.routes.with_raw_response.view(
                "",
            )


class TestAsyncRoutes:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncGradientAI) -> None:
        route = await async_client.agents.routes.update(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
        )
        assert_matches_type(RouteUpdateResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncGradientAI) -> None:
        route = await async_client.agents.routes.update(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
            body_child_agent_uuid="child_agent_uuid",
            if_case="if_case",
            body_parent_agent_uuid="parent_agent_uuid",
            route_name="route_name",
            uuid="uuid",
        )
        assert_matches_type(RouteUpdateResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncGradientAI) -> None:
        response = await async_client.agents.routes.with_raw_response.update(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        route = await response.parse()
        assert_matches_type(RouteUpdateResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncGradientAI) -> None:
        async with async_client.agents.routes.with_streaming_response.update(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            route = await response.parse()
            assert_matches_type(RouteUpdateResponse, route, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncGradientAI) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_parent_agent_uuid` but received ''"
        ):
            await async_client.agents.routes.with_raw_response.update(
                path_child_agent_uuid="child_agent_uuid",
                path_parent_agent_uuid="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_child_agent_uuid` but received ''"):
            await async_client.agents.routes.with_raw_response.update(
                path_child_agent_uuid="",
                path_parent_agent_uuid="parent_agent_uuid",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncGradientAI) -> None:
        route = await async_client.agents.routes.delete(
            child_agent_uuid="child_agent_uuid",
            parent_agent_uuid="parent_agent_uuid",
        )
        assert_matches_type(RouteDeleteResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncGradientAI) -> None:
        response = await async_client.agents.routes.with_raw_response.delete(
            child_agent_uuid="child_agent_uuid",
            parent_agent_uuid="parent_agent_uuid",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        route = await response.parse()
        assert_matches_type(RouteDeleteResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncGradientAI) -> None:
        async with async_client.agents.routes.with_streaming_response.delete(
            child_agent_uuid="child_agent_uuid",
            parent_agent_uuid="parent_agent_uuid",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            route = await response.parse()
            assert_matches_type(RouteDeleteResponse, route, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncGradientAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `parent_agent_uuid` but received ''"):
            await async_client.agents.routes.with_raw_response.delete(
                child_agent_uuid="child_agent_uuid",
                parent_agent_uuid="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `child_agent_uuid` but received ''"):
            await async_client.agents.routes.with_raw_response.delete(
                child_agent_uuid="",
                parent_agent_uuid="parent_agent_uuid",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_add(self, async_client: AsyncGradientAI) -> None:
        route = await async_client.agents.routes.add(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
        )
        assert_matches_type(RouteAddResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_add_with_all_params(self, async_client: AsyncGradientAI) -> None:
        route = await async_client.agents.routes.add(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
            body_child_agent_uuid="child_agent_uuid",
            if_case="if_case",
            body_parent_agent_uuid="parent_agent_uuid",
            route_name="route_name",
        )
        assert_matches_type(RouteAddResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_add(self, async_client: AsyncGradientAI) -> None:
        response = await async_client.agents.routes.with_raw_response.add(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        route = await response.parse()
        assert_matches_type(RouteAddResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_add(self, async_client: AsyncGradientAI) -> None:
        async with async_client.agents.routes.with_streaming_response.add(
            path_child_agent_uuid="child_agent_uuid",
            path_parent_agent_uuid="parent_agent_uuid",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            route = await response.parse()
            assert_matches_type(RouteAddResponse, route, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_add(self, async_client: AsyncGradientAI) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_parent_agent_uuid` but received ''"
        ):
            await async_client.agents.routes.with_raw_response.add(
                path_child_agent_uuid="child_agent_uuid",
                path_parent_agent_uuid="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_child_agent_uuid` but received ''"):
            await async_client.agents.routes.with_raw_response.add(
                path_child_agent_uuid="",
                path_parent_agent_uuid="parent_agent_uuid",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_view(self, async_client: AsyncGradientAI) -> None:
        route = await async_client.agents.routes.view(
            "uuid",
        )
        assert_matches_type(RouteViewResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_view(self, async_client: AsyncGradientAI) -> None:
        response = await async_client.agents.routes.with_raw_response.view(
            "uuid",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        route = await response.parse()
        assert_matches_type(RouteViewResponse, route, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_view(self, async_client: AsyncGradientAI) -> None:
        async with async_client.agents.routes.with_streaming_response.view(
            "uuid",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            route = await response.parse()
            assert_matches_type(RouteViewResponse, route, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_view(self, async_client: AsyncGradientAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `uuid` but received ''"):
            await async_client.agents.routes.with_raw_response.view(
                "",
            )

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from solvice_vrp_solver import SolviceVrpSolver, AsyncSolviceVrpSolver
from solvice_vrp_solver.types import OnRouteRequest, SolviceStatusJob
from solvice_vrp_solver.types.vrp import OnRouteResponse, SolveExplanationResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSolves:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: SolviceVrpSolver) -> None:
        solve = client.vrp.solves.retrieve(
            "id",
        )
        assert_matches_type(OnRouteRequest, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: SolviceVrpSolver) -> None:
        response = client.vrp.solves.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solve = response.parse()
        assert_matches_type(OnRouteRequest, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: SolviceVrpSolver) -> None:
        with client.vrp.solves.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solve = response.parse()
            assert_matches_type(OnRouteRequest, solve, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: SolviceVrpSolver) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vrp.solves.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_explanation(self, client: SolviceVrpSolver) -> None:
        solve = client.vrp.solves.explanation(
            "id",
        )
        assert_matches_type(SolveExplanationResponse, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_explanation(self, client: SolviceVrpSolver) -> None:
        response = client.vrp.solves.with_raw_response.explanation(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solve = response.parse()
        assert_matches_type(SolveExplanationResponse, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_explanation(self, client: SolviceVrpSolver) -> None:
        with client.vrp.solves.with_streaming_response.explanation(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solve = response.parse()
            assert_matches_type(SolveExplanationResponse, solve, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_explanation(self, client: SolviceVrpSolver) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vrp.solves.with_raw_response.explanation(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_solution(self, client: SolviceVrpSolver) -> None:
        solve = client.vrp.solves.solution(
            "id",
        )
        assert_matches_type(OnRouteResponse, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_solution(self, client: SolviceVrpSolver) -> None:
        response = client.vrp.solves.with_raw_response.solution(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solve = response.parse()
        assert_matches_type(OnRouteResponse, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_solution(self, client: SolviceVrpSolver) -> None:
        with client.vrp.solves.with_streaming_response.solution(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solve = response.parse()
            assert_matches_type(OnRouteResponse, solve, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_solution(self, client: SolviceVrpSolver) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vrp.solves.with_raw_response.solution(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_status(self, client: SolviceVrpSolver) -> None:
        solve = client.vrp.solves.status(
            "id",
        )
        assert_matches_type(SolviceStatusJob, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_status(self, client: SolviceVrpSolver) -> None:
        response = client.vrp.solves.with_raw_response.status(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solve = response.parse()
        assert_matches_type(SolviceStatusJob, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_status(self, client: SolviceVrpSolver) -> None:
        with client.vrp.solves.with_streaming_response.status(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solve = response.parse()
            assert_matches_type(SolviceStatusJob, solve, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_status(self, client: SolviceVrpSolver) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.vrp.solves.with_raw_response.status(
                "",
            )


class TestAsyncSolves:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSolviceVrpSolver) -> None:
        solve = await async_client.vrp.solves.retrieve(
            "id",
        )
        assert_matches_type(OnRouteRequest, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSolviceVrpSolver) -> None:
        response = await async_client.vrp.solves.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solve = await response.parse()
        assert_matches_type(OnRouteRequest, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSolviceVrpSolver) -> None:
        async with async_client.vrp.solves.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solve = await response.parse()
            assert_matches_type(OnRouteRequest, solve, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSolviceVrpSolver) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vrp.solves.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_explanation(self, async_client: AsyncSolviceVrpSolver) -> None:
        solve = await async_client.vrp.solves.explanation(
            "id",
        )
        assert_matches_type(SolveExplanationResponse, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_explanation(self, async_client: AsyncSolviceVrpSolver) -> None:
        response = await async_client.vrp.solves.with_raw_response.explanation(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solve = await response.parse()
        assert_matches_type(SolveExplanationResponse, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_explanation(self, async_client: AsyncSolviceVrpSolver) -> None:
        async with async_client.vrp.solves.with_streaming_response.explanation(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solve = await response.parse()
            assert_matches_type(SolveExplanationResponse, solve, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_explanation(self, async_client: AsyncSolviceVrpSolver) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vrp.solves.with_raw_response.explanation(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_solution(self, async_client: AsyncSolviceVrpSolver) -> None:
        solve = await async_client.vrp.solves.solution(
            "id",
        )
        assert_matches_type(OnRouteResponse, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_solution(self, async_client: AsyncSolviceVrpSolver) -> None:
        response = await async_client.vrp.solves.with_raw_response.solution(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solve = await response.parse()
        assert_matches_type(OnRouteResponse, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_solution(self, async_client: AsyncSolviceVrpSolver) -> None:
        async with async_client.vrp.solves.with_streaming_response.solution(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solve = await response.parse()
            assert_matches_type(OnRouteResponse, solve, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_solution(self, async_client: AsyncSolviceVrpSolver) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vrp.solves.with_raw_response.solution(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_status(self, async_client: AsyncSolviceVrpSolver) -> None:
        solve = await async_client.vrp.solves.status(
            "id",
        )
        assert_matches_type(SolviceStatusJob, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_status(self, async_client: AsyncSolviceVrpSolver) -> None:
        response = await async_client.vrp.solves.with_raw_response.status(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solve = await response.parse()
        assert_matches_type(SolviceStatusJob, solve, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_status(self, async_client: AsyncSolviceVrpSolver) -> None:
        async with async_client.vrp.solves.with_streaming_response.status(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solve = await response.parse()
            assert_matches_type(SolviceStatusJob, solve, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_status(self, async_client: AsyncSolviceVrpSolver) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.vrp.solves.with_raw_response.status(
                "",
            )

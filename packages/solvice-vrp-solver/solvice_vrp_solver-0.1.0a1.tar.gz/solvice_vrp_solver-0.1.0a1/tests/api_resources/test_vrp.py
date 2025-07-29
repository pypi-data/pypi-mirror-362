# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from solvice_vrp_solver import SolviceVrpSolver, AsyncSolviceVrpSolver
from solvice_vrp_solver.types import (
    OnRouteRequest,
    SolviceStatusJob,
)
from solvice_vrp_solver._utils import parse_datetime
from solvice_vrp_solver.types.vrp import OnRouteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVrp:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_demo(self, client: SolviceVrpSolver) -> None:
        vrp = client.vrp.demo()
        assert_matches_type(OnRouteRequest, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_demo_with_all_params(self, client: SolviceVrpSolver) -> None:
        vrp = client.vrp.demo(
            geolocation="geolocation",
            jobs=0,
            radius=0,
        )
        assert_matches_type(OnRouteRequest, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_demo(self, client: SolviceVrpSolver) -> None:
        response = client.vrp.with_raw_response.demo()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vrp = response.parse()
        assert_matches_type(OnRouteRequest, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_demo(self, client: SolviceVrpSolver) -> None:
        with client.vrp.with_streaming_response.demo() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vrp = response.parse()
            assert_matches_type(OnRouteRequest, vrp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_evaluate(self, client: SolviceVrpSolver) -> None:
        vrp = client.vrp.evaluate(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_evaluate_with_all_params(self, client: SolviceVrpSolver) -> None:
        vrp = client.vrp.evaluate(
            jobs=[
                {
                    "name": "1",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
                {
                    "name": "2",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
            ],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                            "breaks": [{"type": "WINDOWED"}],
                            "end": {
                                "latitude": 51.05,
                                "longitude": 3.72,
                            },
                            "ignore_travel_time_from_last_job": False,
                            "ignore_travel_time_to_first_job": False,
                            "overtime": {},
                            "overtime_end": "2023-01-13 19:00:00+00:00",
                            "start": {
                                "latitude": 51.0543,
                                "longitude": 3.7174,
                            },
                            "tags": ["delivery", "installation"],
                        }
                    ],
                    "capacity": [500, 200],
                    "category": "CAR",
                    "end": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "hourly_cost": 60,
                    "max_drive_time": 0,
                    "max_drive_time_in_seconds": {},
                    "max_drive_time_job": 0,
                    "region": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "rules": [
                        {
                            "max_drive_time": 10800,
                            "max_job_complexity": 0,
                            "max_service_time": 21600,
                            "max_work_time": 28800,
                            "min_drive_time": 3600,
                            "min_job_complexity": 0,
                            "min_service_time": 7200,
                            "min_work_time": 14400,
                            "period": {
                                "end": "2007-12-31 17:00:00",
                                "from": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "to": parse_datetime("2019-12-27T18:11:19.117Z"),
                            },
                        }
                    ],
                    "start": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "tags": ["string"],
                }
            ],
            hook="https://example.com",
            label="label",
            options={
                "euclidian": False,
                "explanation": {
                    "enabled": True,
                    "filter_hard_constraints": True,
                    "only_unassigned": True,
                },
                "fair_complexity_per_resource": True,
                "fair_complexity_per_trip": True,
                "fair_workload_per_resource": False,
                "fair_workload_per_trip": False,
                "max_suggestions": 3,
                "minimize_resources": True,
                "only_feasible_suggestions": True,
                "partial_planning": True,
                "polylines": True,
                "routing_engine": "OSM",
                "snap_unit": 300,
                "traffic": 1.1,
                "workload_sensitivity": 0.1,
            },
            relations=[
                {
                    "jobs": ["Job-1", "Job-2"],
                    "time_interval": "FROM_ARRIVAL",
                    "type": "SEQUENCE",
                    "max_time_interval": 3600,
                    "max_waiting_time": 1200,
                    "min_time_interval": 0,
                    "partial_planning": False,
                    "resource": "vehicle-1",
                    "tags": ["urgent"],
                }
            ],
            weights={
                "allowed_resources_weight": 500,
                "asap_weight": 5,
                "drive_time_weight": 1,
                "minimize_resources_weight": 0,
                "planned_weight": 1000,
                "priority_weight": 100,
                "ranking_weight": 1,
                "travel_time_weight": 1,
                "urgency_weight": 50,
                "wait_time_weight": 1,
                "workload_spread_weight": 10,
            },
        )
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_evaluate(self, client: SolviceVrpSolver) -> None:
        response = client.vrp.with_raw_response.evaluate(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vrp = response.parse()
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_evaluate(self, client: SolviceVrpSolver) -> None:
        with client.vrp.with_streaming_response.evaluate(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vrp = response.parse()
            assert_matches_type(SolviceStatusJob, vrp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_solve(self, client: SolviceVrpSolver) -> None:
        vrp = client.vrp.solve(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_solve_with_all_params(self, client: SolviceVrpSolver) -> None:
        vrp = client.vrp.solve(
            jobs=[
                {
                    "name": "1",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
                {
                    "name": "2",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
            ],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                            "breaks": [{"type": "WINDOWED"}],
                            "end": {
                                "latitude": 51.05,
                                "longitude": 3.72,
                            },
                            "ignore_travel_time_from_last_job": False,
                            "ignore_travel_time_to_first_job": False,
                            "overtime": {},
                            "overtime_end": "2023-01-13 19:00:00+00:00",
                            "start": {
                                "latitude": 51.0543,
                                "longitude": 3.7174,
                            },
                            "tags": ["delivery", "installation"],
                        }
                    ],
                    "capacity": [500, 200],
                    "category": "CAR",
                    "end": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "hourly_cost": 60,
                    "max_drive_time": 0,
                    "max_drive_time_in_seconds": {},
                    "max_drive_time_job": 0,
                    "region": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "rules": [
                        {
                            "max_drive_time": 10800,
                            "max_job_complexity": 0,
                            "max_service_time": 21600,
                            "max_work_time": 28800,
                            "min_drive_time": 3600,
                            "min_job_complexity": 0,
                            "min_service_time": 7200,
                            "min_work_time": 14400,
                            "period": {
                                "end": "2007-12-31 17:00:00",
                                "from": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "to": parse_datetime("2019-12-27T18:11:19.117Z"),
                            },
                        }
                    ],
                    "start": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "tags": ["string"],
                }
            ],
            millis="millis",
            hook="https://example.com",
            label="label",
            options={
                "euclidian": False,
                "explanation": {
                    "enabled": True,
                    "filter_hard_constraints": True,
                    "only_unassigned": True,
                },
                "fair_complexity_per_resource": True,
                "fair_complexity_per_trip": True,
                "fair_workload_per_resource": False,
                "fair_workload_per_trip": False,
                "max_suggestions": 3,
                "minimize_resources": True,
                "only_feasible_suggestions": True,
                "partial_planning": True,
                "polylines": True,
                "routing_engine": "OSM",
                "snap_unit": 300,
                "traffic": 1.1,
                "workload_sensitivity": 0.1,
            },
            relations=[
                {
                    "jobs": ["Job-1", "Job-2"],
                    "time_interval": "FROM_ARRIVAL",
                    "type": "SEQUENCE",
                    "max_time_interval": 3600,
                    "max_waiting_time": 1200,
                    "min_time_interval": 0,
                    "partial_planning": False,
                    "resource": "vehicle-1",
                    "tags": ["urgent"],
                }
            ],
            weights={
                "allowed_resources_weight": 500,
                "asap_weight": 5,
                "drive_time_weight": 1,
                "minimize_resources_weight": 0,
                "planned_weight": 1000,
                "priority_weight": 100,
                "ranking_weight": 1,
                "travel_time_weight": 1,
                "urgency_weight": 50,
                "wait_time_weight": 1,
                "workload_spread_weight": 10,
            },
            instance="instance",
        )
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_solve(self, client: SolviceVrpSolver) -> None:
        response = client.vrp.with_raw_response.solve(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vrp = response.parse()
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_solve(self, client: SolviceVrpSolver) -> None:
        with client.vrp.with_streaming_response.solve(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vrp = response.parse()
            assert_matches_type(SolviceStatusJob, vrp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_suggest(self, client: SolviceVrpSolver) -> None:
        vrp = client.vrp.suggest(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_suggest_with_all_params(self, client: SolviceVrpSolver) -> None:
        vrp = client.vrp.suggest(
            jobs=[
                {
                    "name": "1",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
                {
                    "name": "2",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
            ],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                            "breaks": [{"type": "WINDOWED"}],
                            "end": {
                                "latitude": 51.05,
                                "longitude": 3.72,
                            },
                            "ignore_travel_time_from_last_job": False,
                            "ignore_travel_time_to_first_job": False,
                            "overtime": {},
                            "overtime_end": "2023-01-13 19:00:00+00:00",
                            "start": {
                                "latitude": 51.0543,
                                "longitude": 3.7174,
                            },
                            "tags": ["delivery", "installation"],
                        }
                    ],
                    "capacity": [500, 200],
                    "category": "CAR",
                    "end": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "hourly_cost": 60,
                    "max_drive_time": 0,
                    "max_drive_time_in_seconds": {},
                    "max_drive_time_job": 0,
                    "region": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "rules": [
                        {
                            "max_drive_time": 10800,
                            "max_job_complexity": 0,
                            "max_service_time": 21600,
                            "max_work_time": 28800,
                            "min_drive_time": 3600,
                            "min_job_complexity": 0,
                            "min_service_time": 7200,
                            "min_work_time": 14400,
                            "period": {
                                "end": "2007-12-31 17:00:00",
                                "from": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "to": parse_datetime("2019-12-27T18:11:19.117Z"),
                            },
                        }
                    ],
                    "start": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "tags": ["string"],
                }
            ],
            millis="millis",
            hook="https://example.com",
            label="label",
            options={
                "euclidian": False,
                "explanation": {
                    "enabled": True,
                    "filter_hard_constraints": True,
                    "only_unassigned": True,
                },
                "fair_complexity_per_resource": True,
                "fair_complexity_per_trip": True,
                "fair_workload_per_resource": False,
                "fair_workload_per_trip": False,
                "max_suggestions": 3,
                "minimize_resources": True,
                "only_feasible_suggestions": True,
                "partial_planning": True,
                "polylines": True,
                "routing_engine": "OSM",
                "snap_unit": 300,
                "traffic": 1.1,
                "workload_sensitivity": 0.1,
            },
            relations=[
                {
                    "jobs": ["Job-1", "Job-2"],
                    "time_interval": "FROM_ARRIVAL",
                    "type": "SEQUENCE",
                    "max_time_interval": 3600,
                    "max_waiting_time": 1200,
                    "min_time_interval": 0,
                    "partial_planning": False,
                    "resource": "vehicle-1",
                    "tags": ["urgent"],
                }
            ],
            weights={
                "allowed_resources_weight": 500,
                "asap_weight": 5,
                "drive_time_weight": 1,
                "minimize_resources_weight": 0,
                "planned_weight": 1000,
                "priority_weight": 100,
                "ranking_weight": 1,
                "travel_time_weight": 1,
                "urgency_weight": 50,
                "wait_time_weight": 1,
                "workload_spread_weight": 10,
            },
        )
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_suggest(self, client: SolviceVrpSolver) -> None:
        response = client.vrp.with_raw_response.suggest(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vrp = response.parse()
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_suggest(self, client: SolviceVrpSolver) -> None:
        with client.vrp.with_streaming_response.suggest(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vrp = response.parse()
            assert_matches_type(SolviceStatusJob, vrp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_sync(self, client: SolviceVrpSolver) -> None:
        vrp = client.vrp.sync(
            operation="SOLVE",
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )
        assert_matches_type(OnRouteResponse, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_sync_with_all_params(self, client: SolviceVrpSolver) -> None:
        vrp = client.vrp.sync(
            operation="SOLVE",
            jobs=[
                {
                    "name": "1",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
                {
                    "name": "2",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
            ],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                            "breaks": [{"type": "WINDOWED"}],
                            "end": {
                                "latitude": 51.05,
                                "longitude": 3.72,
                            },
                            "ignore_travel_time_from_last_job": False,
                            "ignore_travel_time_to_first_job": False,
                            "overtime": {},
                            "overtime_end": "2023-01-13 19:00:00+00:00",
                            "start": {
                                "latitude": 51.0543,
                                "longitude": 3.7174,
                            },
                            "tags": ["delivery", "installation"],
                        }
                    ],
                    "capacity": [500, 200],
                    "category": "CAR",
                    "end": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "hourly_cost": 60,
                    "max_drive_time": 0,
                    "max_drive_time_in_seconds": {},
                    "max_drive_time_job": 0,
                    "region": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "rules": [
                        {
                            "max_drive_time": 10800,
                            "max_job_complexity": 0,
                            "max_service_time": 21600,
                            "max_work_time": 28800,
                            "min_drive_time": 3600,
                            "min_job_complexity": 0,
                            "min_service_time": 7200,
                            "min_work_time": 14400,
                            "period": {
                                "end": "2007-12-31 17:00:00",
                                "from": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "to": parse_datetime("2019-12-27T18:11:19.117Z"),
                            },
                        }
                    ],
                    "start": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "tags": ["string"],
                }
            ],
            millis="millis",
            hook="https://example.com",
            label="label",
            options={
                "euclidian": False,
                "explanation": {
                    "enabled": True,
                    "filter_hard_constraints": True,
                    "only_unassigned": True,
                },
                "fair_complexity_per_resource": True,
                "fair_complexity_per_trip": True,
                "fair_workload_per_resource": False,
                "fair_workload_per_trip": False,
                "max_suggestions": 3,
                "minimize_resources": True,
                "only_feasible_suggestions": True,
                "partial_planning": True,
                "polylines": True,
                "routing_engine": "OSM",
                "snap_unit": 300,
                "traffic": 1.1,
                "workload_sensitivity": 0.1,
            },
            relations=[
                {
                    "jobs": ["Job-1", "Job-2"],
                    "time_interval": "FROM_ARRIVAL",
                    "type": "SEQUENCE",
                    "max_time_interval": 3600,
                    "max_waiting_time": 1200,
                    "min_time_interval": 0,
                    "partial_planning": False,
                    "resource": "vehicle-1",
                    "tags": ["urgent"],
                }
            ],
            weights={
                "allowed_resources_weight": 500,
                "asap_weight": 5,
                "drive_time_weight": 1,
                "minimize_resources_weight": 0,
                "planned_weight": 1000,
                "priority_weight": 100,
                "ranking_weight": 1,
                "travel_time_weight": 1,
                "urgency_weight": 50,
                "wait_time_weight": 1,
                "workload_spread_weight": 10,
            },
        )
        assert_matches_type(OnRouteResponse, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_sync(self, client: SolviceVrpSolver) -> None:
        response = client.vrp.with_raw_response.sync(
            operation="SOLVE",
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vrp = response.parse()
        assert_matches_type(OnRouteResponse, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_sync(self, client: SolviceVrpSolver) -> None:
        with client.vrp.with_streaming_response.sync(
            operation="SOLVE",
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vrp = response.parse()
            assert_matches_type(OnRouteResponse, vrp, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncVrp:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip()
    @parametrize
    async def test_method_demo(self, async_client: AsyncSolviceVrpSolver) -> None:
        vrp = await async_client.vrp.demo()
        assert_matches_type(OnRouteRequest, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_demo_with_all_params(self, async_client: AsyncSolviceVrpSolver) -> None:
        vrp = await async_client.vrp.demo(
            geolocation="geolocation",
            jobs=0,
            radius=0,
        )
        assert_matches_type(OnRouteRequest, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_demo(self, async_client: AsyncSolviceVrpSolver) -> None:
        response = await async_client.vrp.with_raw_response.demo()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vrp = await response.parse()
        assert_matches_type(OnRouteRequest, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_demo(self, async_client: AsyncSolviceVrpSolver) -> None:
        async with async_client.vrp.with_streaming_response.demo() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vrp = await response.parse()
            assert_matches_type(OnRouteRequest, vrp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_evaluate(self, async_client: AsyncSolviceVrpSolver) -> None:
        vrp = await async_client.vrp.evaluate(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_evaluate_with_all_params(self, async_client: AsyncSolviceVrpSolver) -> None:
        vrp = await async_client.vrp.evaluate(
            jobs=[
                {
                    "name": "1",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
                {
                    "name": "2",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
            ],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                            "breaks": [{"type": "WINDOWED"}],
                            "end": {
                                "latitude": 51.05,
                                "longitude": 3.72,
                            },
                            "ignore_travel_time_from_last_job": False,
                            "ignore_travel_time_to_first_job": False,
                            "overtime": {},
                            "overtime_end": "2023-01-13 19:00:00+00:00",
                            "start": {
                                "latitude": 51.0543,
                                "longitude": 3.7174,
                            },
                            "tags": ["delivery", "installation"],
                        }
                    ],
                    "capacity": [500, 200],
                    "category": "CAR",
                    "end": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "hourly_cost": 60,
                    "max_drive_time": 0,
                    "max_drive_time_in_seconds": {},
                    "max_drive_time_job": 0,
                    "region": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "rules": [
                        {
                            "max_drive_time": 10800,
                            "max_job_complexity": 0,
                            "max_service_time": 21600,
                            "max_work_time": 28800,
                            "min_drive_time": 3600,
                            "min_job_complexity": 0,
                            "min_service_time": 7200,
                            "min_work_time": 14400,
                            "period": {
                                "end": "2007-12-31 17:00:00",
                                "from": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "to": parse_datetime("2019-12-27T18:11:19.117Z"),
                            },
                        }
                    ],
                    "start": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "tags": ["string"],
                }
            ],
            hook="https://example.com",
            label="label",
            options={
                "euclidian": False,
                "explanation": {
                    "enabled": True,
                    "filter_hard_constraints": True,
                    "only_unassigned": True,
                },
                "fair_complexity_per_resource": True,
                "fair_complexity_per_trip": True,
                "fair_workload_per_resource": False,
                "fair_workload_per_trip": False,
                "max_suggestions": 3,
                "minimize_resources": True,
                "only_feasible_suggestions": True,
                "partial_planning": True,
                "polylines": True,
                "routing_engine": "OSM",
                "snap_unit": 300,
                "traffic": 1.1,
                "workload_sensitivity": 0.1,
            },
            relations=[
                {
                    "jobs": ["Job-1", "Job-2"],
                    "time_interval": "FROM_ARRIVAL",
                    "type": "SEQUENCE",
                    "max_time_interval": 3600,
                    "max_waiting_time": 1200,
                    "min_time_interval": 0,
                    "partial_planning": False,
                    "resource": "vehicle-1",
                    "tags": ["urgent"],
                }
            ],
            weights={
                "allowed_resources_weight": 500,
                "asap_weight": 5,
                "drive_time_weight": 1,
                "minimize_resources_weight": 0,
                "planned_weight": 1000,
                "priority_weight": 100,
                "ranking_weight": 1,
                "travel_time_weight": 1,
                "urgency_weight": 50,
                "wait_time_weight": 1,
                "workload_spread_weight": 10,
            },
        )
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_evaluate(self, async_client: AsyncSolviceVrpSolver) -> None:
        response = await async_client.vrp.with_raw_response.evaluate(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vrp = await response.parse()
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_evaluate(self, async_client: AsyncSolviceVrpSolver) -> None:
        async with async_client.vrp.with_streaming_response.evaluate(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vrp = await response.parse()
            assert_matches_type(SolviceStatusJob, vrp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_solve(self, async_client: AsyncSolviceVrpSolver) -> None:
        vrp = await async_client.vrp.solve(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_solve_with_all_params(self, async_client: AsyncSolviceVrpSolver) -> None:
        vrp = await async_client.vrp.solve(
            jobs=[
                {
                    "name": "1",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
                {
                    "name": "2",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
            ],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                            "breaks": [{"type": "WINDOWED"}],
                            "end": {
                                "latitude": 51.05,
                                "longitude": 3.72,
                            },
                            "ignore_travel_time_from_last_job": False,
                            "ignore_travel_time_to_first_job": False,
                            "overtime": {},
                            "overtime_end": "2023-01-13 19:00:00+00:00",
                            "start": {
                                "latitude": 51.0543,
                                "longitude": 3.7174,
                            },
                            "tags": ["delivery", "installation"],
                        }
                    ],
                    "capacity": [500, 200],
                    "category": "CAR",
                    "end": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "hourly_cost": 60,
                    "max_drive_time": 0,
                    "max_drive_time_in_seconds": {},
                    "max_drive_time_job": 0,
                    "region": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "rules": [
                        {
                            "max_drive_time": 10800,
                            "max_job_complexity": 0,
                            "max_service_time": 21600,
                            "max_work_time": 28800,
                            "min_drive_time": 3600,
                            "min_job_complexity": 0,
                            "min_service_time": 7200,
                            "min_work_time": 14400,
                            "period": {
                                "end": "2007-12-31 17:00:00",
                                "from": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "to": parse_datetime("2019-12-27T18:11:19.117Z"),
                            },
                        }
                    ],
                    "start": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "tags": ["string"],
                }
            ],
            millis="millis",
            hook="https://example.com",
            label="label",
            options={
                "euclidian": False,
                "explanation": {
                    "enabled": True,
                    "filter_hard_constraints": True,
                    "only_unassigned": True,
                },
                "fair_complexity_per_resource": True,
                "fair_complexity_per_trip": True,
                "fair_workload_per_resource": False,
                "fair_workload_per_trip": False,
                "max_suggestions": 3,
                "minimize_resources": True,
                "only_feasible_suggestions": True,
                "partial_planning": True,
                "polylines": True,
                "routing_engine": "OSM",
                "snap_unit": 300,
                "traffic": 1.1,
                "workload_sensitivity": 0.1,
            },
            relations=[
                {
                    "jobs": ["Job-1", "Job-2"],
                    "time_interval": "FROM_ARRIVAL",
                    "type": "SEQUENCE",
                    "max_time_interval": 3600,
                    "max_waiting_time": 1200,
                    "min_time_interval": 0,
                    "partial_planning": False,
                    "resource": "vehicle-1",
                    "tags": ["urgent"],
                }
            ],
            weights={
                "allowed_resources_weight": 500,
                "asap_weight": 5,
                "drive_time_weight": 1,
                "minimize_resources_weight": 0,
                "planned_weight": 1000,
                "priority_weight": 100,
                "ranking_weight": 1,
                "travel_time_weight": 1,
                "urgency_weight": 50,
                "wait_time_weight": 1,
                "workload_spread_weight": 10,
            },
            instance="instance",
        )
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_solve(self, async_client: AsyncSolviceVrpSolver) -> None:
        response = await async_client.vrp.with_raw_response.solve(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vrp = await response.parse()
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_solve(self, async_client: AsyncSolviceVrpSolver) -> None:
        async with async_client.vrp.with_streaming_response.solve(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vrp = await response.parse()
            assert_matches_type(SolviceStatusJob, vrp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_suggest(self, async_client: AsyncSolviceVrpSolver) -> None:
        vrp = await async_client.vrp.suggest(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_suggest_with_all_params(self, async_client: AsyncSolviceVrpSolver) -> None:
        vrp = await async_client.vrp.suggest(
            jobs=[
                {
                    "name": "1",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
                {
                    "name": "2",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
            ],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                            "breaks": [{"type": "WINDOWED"}],
                            "end": {
                                "latitude": 51.05,
                                "longitude": 3.72,
                            },
                            "ignore_travel_time_from_last_job": False,
                            "ignore_travel_time_to_first_job": False,
                            "overtime": {},
                            "overtime_end": "2023-01-13 19:00:00+00:00",
                            "start": {
                                "latitude": 51.0543,
                                "longitude": 3.7174,
                            },
                            "tags": ["delivery", "installation"],
                        }
                    ],
                    "capacity": [500, 200],
                    "category": "CAR",
                    "end": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "hourly_cost": 60,
                    "max_drive_time": 0,
                    "max_drive_time_in_seconds": {},
                    "max_drive_time_job": 0,
                    "region": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "rules": [
                        {
                            "max_drive_time": 10800,
                            "max_job_complexity": 0,
                            "max_service_time": 21600,
                            "max_work_time": 28800,
                            "min_drive_time": 3600,
                            "min_job_complexity": 0,
                            "min_service_time": 7200,
                            "min_work_time": 14400,
                            "period": {
                                "end": "2007-12-31 17:00:00",
                                "from": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "to": parse_datetime("2019-12-27T18:11:19.117Z"),
                            },
                        }
                    ],
                    "start": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "tags": ["string"],
                }
            ],
            millis="millis",
            hook="https://example.com",
            label="label",
            options={
                "euclidian": False,
                "explanation": {
                    "enabled": True,
                    "filter_hard_constraints": True,
                    "only_unassigned": True,
                },
                "fair_complexity_per_resource": True,
                "fair_complexity_per_trip": True,
                "fair_workload_per_resource": False,
                "fair_workload_per_trip": False,
                "max_suggestions": 3,
                "minimize_resources": True,
                "only_feasible_suggestions": True,
                "partial_planning": True,
                "polylines": True,
                "routing_engine": "OSM",
                "snap_unit": 300,
                "traffic": 1.1,
                "workload_sensitivity": 0.1,
            },
            relations=[
                {
                    "jobs": ["Job-1", "Job-2"],
                    "time_interval": "FROM_ARRIVAL",
                    "type": "SEQUENCE",
                    "max_time_interval": 3600,
                    "max_waiting_time": 1200,
                    "min_time_interval": 0,
                    "partial_planning": False,
                    "resource": "vehicle-1",
                    "tags": ["urgent"],
                }
            ],
            weights={
                "allowed_resources_weight": 500,
                "asap_weight": 5,
                "drive_time_weight": 1,
                "minimize_resources_weight": 0,
                "planned_weight": 1000,
                "priority_weight": 100,
                "ranking_weight": 1,
                "travel_time_weight": 1,
                "urgency_weight": 50,
                "wait_time_weight": 1,
                "workload_spread_weight": 10,
            },
        )
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_suggest(self, async_client: AsyncSolviceVrpSolver) -> None:
        response = await async_client.vrp.with_raw_response.suggest(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vrp = await response.parse()
        assert_matches_type(SolviceStatusJob, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_suggest(self, async_client: AsyncSolviceVrpSolver) -> None:
        async with async_client.vrp.with_streaming_response.suggest(
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vrp = await response.parse()
            assert_matches_type(SolviceStatusJob, vrp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_sync(self, async_client: AsyncSolviceVrpSolver) -> None:
        vrp = await async_client.vrp.sync(
            operation="SOLVE",
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )
        assert_matches_type(OnRouteResponse, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_sync_with_all_params(self, async_client: AsyncSolviceVrpSolver) -> None:
        vrp = await async_client.vrp.sync(
            operation="SOLVE",
            jobs=[
                {
                    "name": "1",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
                {
                    "name": "2",
                    "allowed_resources": ["string"],
                    "complexity": 1,
                    "disallowed_resources": ["string"],
                    "duration": 3600,
                    "duration_squash": 30,
                    "hard": True,
                    "hard_weight": 1,
                    "initial_arrival": "2023-01-13T09:00",
                    "initial_resource": "initialResource",
                    "load": [5, 10],
                    "location": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "padding": 300,
                    "planned_arrival": "2023-01-13T09:00",
                    "planned_date": "2022-03-10",
                    "planned_resource": "plannedResource",
                    "priority": 100,
                    "rankings": [
                        {
                            "name": "certified-technician",
                            "ranking": 5,
                        }
                    ],
                    "resumable": True,
                    "tags": [
                        {
                            "name": "certified-technician",
                            "hard": False,
                            "weight": 300,
                        }
                    ],
                    "urgency": 100,
                    "windows": [
                        {
                            "from": "2024-01-15 09:00:00+00:00",
                            "to": "2024-01-15 17:00:00+00:00",
                            "hard": True,
                            "weight": 1,
                        }
                    ],
                },
            ],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                            "breaks": [{"type": "WINDOWED"}],
                            "end": {
                                "latitude": 51.05,
                                "longitude": 3.72,
                            },
                            "ignore_travel_time_from_last_job": False,
                            "ignore_travel_time_to_first_job": False,
                            "overtime": {},
                            "overtime_end": "2023-01-13 19:00:00+00:00",
                            "start": {
                                "latitude": 51.0543,
                                "longitude": 3.7174,
                            },
                            "tags": ["delivery", "installation"],
                        }
                    ],
                    "capacity": [500, 200],
                    "category": "CAR",
                    "end": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "hourly_cost": 60,
                    "max_drive_time": 0,
                    "max_drive_time_in_seconds": {},
                    "max_drive_time_job": 0,
                    "region": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "rules": [
                        {
                            "max_drive_time": 10800,
                            "max_job_complexity": 0,
                            "max_service_time": 21600,
                            "max_work_time": 28800,
                            "min_drive_time": 3600,
                            "min_job_complexity": 0,
                            "min_service_time": 7200,
                            "min_work_time": 14400,
                            "period": {
                                "end": "2007-12-31 17:00:00",
                                "from": parse_datetime("2019-12-27T18:11:19.117Z"),
                                "to": parse_datetime("2019-12-27T18:11:19.117Z"),
                            },
                        }
                    ],
                    "start": {
                        "latitude": 50.0987624,
                        "longitude": 4.93849204,
                    },
                    "tags": ["string"],
                }
            ],
            millis="millis",
            hook="https://example.com",
            label="label",
            options={
                "euclidian": False,
                "explanation": {
                    "enabled": True,
                    "filter_hard_constraints": True,
                    "only_unassigned": True,
                },
                "fair_complexity_per_resource": True,
                "fair_complexity_per_trip": True,
                "fair_workload_per_resource": False,
                "fair_workload_per_trip": False,
                "max_suggestions": 3,
                "minimize_resources": True,
                "only_feasible_suggestions": True,
                "partial_planning": True,
                "polylines": True,
                "routing_engine": "OSM",
                "snap_unit": 300,
                "traffic": 1.1,
                "workload_sensitivity": 0.1,
            },
            relations=[
                {
                    "jobs": ["Job-1", "Job-2"],
                    "time_interval": "FROM_ARRIVAL",
                    "type": "SEQUENCE",
                    "max_time_interval": 3600,
                    "max_waiting_time": 1200,
                    "min_time_interval": 0,
                    "partial_planning": False,
                    "resource": "vehicle-1",
                    "tags": ["urgent"],
                }
            ],
            weights={
                "allowed_resources_weight": 500,
                "asap_weight": 5,
                "drive_time_weight": 1,
                "minimize_resources_weight": 0,
                "planned_weight": 1000,
                "priority_weight": 100,
                "ranking_weight": 1,
                "travel_time_weight": 1,
                "urgency_weight": 50,
                "wait_time_weight": 1,
                "workload_spread_weight": 10,
            },
        )
        assert_matches_type(OnRouteResponse, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_sync(self, async_client: AsyncSolviceVrpSolver) -> None:
        response = await async_client.vrp.with_raw_response.sync(
            operation="SOLVE",
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        vrp = await response.parse()
        assert_matches_type(OnRouteResponse, vrp, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_sync(self, async_client: AsyncSolviceVrpSolver) -> None:
        async with async_client.vrp.with_streaming_response.sync(
            operation="SOLVE",
            jobs=[{"name": "1"}, {"name": "2"}],
            resources=[
                {
                    "name": "1",
                    "shifts": [
                        {
                            "from": "2023-01-13 08:00:00+00:00",
                            "to": "2023-01-13 17:00:00+00:00",
                        }
                    ],
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            vrp = await response.parse()
            assert_matches_type(OnRouteResponse, vrp, path=["response"])

        assert cast(Any, response.is_closed) is True

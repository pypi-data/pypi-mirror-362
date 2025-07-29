# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo
from .explanation_options_param import ExplanationOptionsParam

__all__ = ["OptionsParam"]


class OptionsParam(TypedDict, total=False):
    euclidian: Optional[bool]
    """Use euclidian distance for travel time. Default false."""

    explanation: Optional[ExplanationOptionsParam]
    """Options to manage the explanation of the solution"""

    fair_complexity_per_resource: Annotated[Optional[bool], PropertyInfo(alias="fairComplexityPerResource")]

    fair_complexity_per_trip: Annotated[Optional[bool], PropertyInfo(alias="fairComplexityPerTrip")]

    fair_workload_per_resource: Annotated[Optional[bool], PropertyInfo(alias="fairWorkloadPerResource")]
    """
    If true, the workload (service time) will be spread over all days of one
    resource. (interacts with `Weights.workloadSpreadWeight` and
    `options.workloadSensitivity`)
    """

    fair_workload_per_trip: Annotated[Optional[bool], PropertyInfo(alias="fairWorkloadPerTrip")]
    """
    If true, the workload (service time) will be spread over all resources and all
    days. (interacts with `Weights.workloadSpreadWeight` and
    `options.workloadSensitivity`)
    """

    max_suggestions: Annotated[Optional[int], PropertyInfo(alias="maxSuggestions")]
    """
    If the request is submitted to the suggestion end point it indicates the maximum
    number of suggestions the solver should return (default is 0 which means return
    all)
    """

    minimize_resources: Annotated[Optional[bool], PropertyInfo(alias="minimizeResources")]
    """Minimise the vehicle useage or minimise total travel time.

    Two different objective functions.
    """

    only_feasible_suggestions: Annotated[Optional[bool], PropertyInfo(alias="onlyFeasibleSuggestions")]
    """
    If the request is a suggestion then if the initial plan is feasible the solver
    will return only feasible suggestions otherwise it will return only suggestions
    that do not worsen the infeasibility (default is true)
    """

    partial_planning: Annotated[Optional[bool], PropertyInfo(alias="partialPlanning")]
    """
    We will try to assign as many jobs as possible and create a partial schedule
    unless `partial` is set to `false`. Default set to true.
    """

    polylines: Optional[bool]
    """Let our map server calculate the actual polylines for connecting the visits.

    Processing will take longer.
    """

    routing_engine: Annotated[
        Optional[Literal["OSM", "TOMTOM", "GOOGLE", "ANYMAP"]], PropertyInfo(alias="routingEngine")
    ]
    """The routing engine to use for distance and travel time calculations"""

    snap_unit: Annotated[Optional[int], PropertyInfo(alias="snapUnit")]
    """The smallest steps in arrival time to which results will be snapped.

    The snapping policy is round-up and is used at runtime, implying it influences
    the score calculation. Unless a post-calculation feature such as order padding
    is used, any calculated arrival time in `[391, 395]` with a `snapUnit` of `5`
    will yield `395`. Fallback value for `Options.use_snapUnit_for_waitRange`.
    """

    traffic: Optional[float]
    """Modifier to travel time for traffic.

    If you want actual traffic information, use HERE or TomTom map integration.
    """

    workload_sensitivity: Annotated[Optional[float], PropertyInfo(alias="workloadSensitivity")]

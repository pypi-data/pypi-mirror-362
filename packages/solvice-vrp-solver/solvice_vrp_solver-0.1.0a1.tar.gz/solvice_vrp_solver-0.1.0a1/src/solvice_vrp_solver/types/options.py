# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .explanation_options import ExplanationOptions

__all__ = ["Options"]


class Options(BaseModel):
    euclidian: Optional[bool] = None
    """Use euclidian distance for travel time. Default false."""

    explanation: Optional[ExplanationOptions] = None
    """Options to manage the explanation of the solution"""

    fair_complexity_per_resource: Optional[bool] = FieldInfo(alias="fairComplexityPerResource", default=None)

    fair_complexity_per_trip: Optional[bool] = FieldInfo(alias="fairComplexityPerTrip", default=None)

    fair_workload_per_resource: Optional[bool] = FieldInfo(alias="fairWorkloadPerResource", default=None)
    """
    If true, the workload (service time) will be spread over all days of one
    resource. (interacts with `Weights.workloadSpreadWeight` and
    `options.workloadSensitivity`)
    """

    fair_workload_per_trip: Optional[bool] = FieldInfo(alias="fairWorkloadPerTrip", default=None)
    """
    If true, the workload (service time) will be spread over all resources and all
    days. (interacts with `Weights.workloadSpreadWeight` and
    `options.workloadSensitivity`)
    """

    max_suggestions: Optional[int] = FieldInfo(alias="maxSuggestions", default=None)
    """
    If the request is submitted to the suggestion end point it indicates the maximum
    number of suggestions the solver should return (default is 0 which means return
    all)
    """

    minimize_resources: Optional[bool] = FieldInfo(alias="minimizeResources", default=None)
    """Minimise the vehicle useage or minimise total travel time.

    Two different objective functions.
    """

    only_feasible_suggestions: Optional[bool] = FieldInfo(alias="onlyFeasibleSuggestions", default=None)
    """
    If the request is a suggestion then if the initial plan is feasible the solver
    will return only feasible suggestions otherwise it will return only suggestions
    that do not worsen the infeasibility (default is true)
    """

    partial_planning: Optional[bool] = FieldInfo(alias="partialPlanning", default=None)
    """
    We will try to assign as many jobs as possible and create a partial schedule
    unless `partial` is set to `false`. Default set to true.
    """

    polylines: Optional[bool] = None
    """Let our map server calculate the actual polylines for connecting the visits.

    Processing will take longer.
    """

    routing_engine: Optional[Literal["OSM", "TOMTOM", "GOOGLE", "ANYMAP"]] = FieldInfo(
        alias="routingEngine", default=None
    )
    """The routing engine to use for distance and travel time calculations"""

    snap_unit: Optional[int] = FieldInfo(alias="snapUnit", default=None)
    """The smallest steps in arrival time to which results will be snapped.

    The snapping policy is round-up and is used at runtime, implying it influences
    the score calculation. Unless a post-calculation feature such as order padding
    is used, any calculated arrival time in `[391, 395]` with a `snapUnit` of `5`
    will yield `395`. Fallback value for `Options.use_snapUnit_for_waitRange`.
    """

    traffic: Optional[float] = None
    """Modifier to travel time for traffic.

    If you want actual traffic information, use HERE or TomTom map integration.
    """

    workload_sensitivity: Optional[float] = FieldInfo(alias="workloadSensitivity", default=None)

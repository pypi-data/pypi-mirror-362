# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["WeightsParam"]


class WeightsParam(TypedDict, total=False):
    allowed_resources_weight: Annotated[Optional[int], PropertyInfo(alias="allowedResourcesWeight")]
    """Weight modifier for the resources allowed constraint."""

    asap_weight: Annotated[Optional[int], PropertyInfo(alias="asapWeight")]
    """Weight modifier scheduling jobs as soon (on day basis) as possible."""

    drive_time_weight: Annotated[Optional[int], PropertyInfo(alias="driveTimeWeight")]
    """Weight modifier for the drive time constraint."""

    minimize_resources_weight: Annotated[Optional[int], PropertyInfo(alias="minimizeResourcesWeight")]
    """Weight modifier for minimizing activating another resource on a day trip.

    The weight is put on the same balance as travel time. So setting this weight to
    3600 (1hour) will make sure that the solver will try to minimize the number of
    resources used on a day trip compared to 1 extra hour of travel time.
    """

    planned_weight: Annotated[Optional[int], PropertyInfo(alias="plannedWeight")]
    """Weight modifier for planned vehicle and planned date requirement."""

    priority_weight: Annotated[Optional[int], PropertyInfo(alias="priorityWeight")]
    """
    Weight modifier for `job.priority` that ensures that priority orders are
    scheduled. Note that this does not make sure that they are scheduled sooner.
    """

    ranking_weight: Annotated[Optional[int], PropertyInfo(alias="rankingWeight")]
    """Weight modifier for tag ranking preference.

    Higher weight increases the importance of assigning jobs to higher-ranked
    resources.
    """

    travel_time_weight: Annotated[Optional[int], PropertyInfo(alias="travelTimeWeight")]
    """Weight modifier for travel time."""

    urgency_weight: Annotated[Optional[int], PropertyInfo(alias="urgencyWeight")]
    """Weight modifier for the urgency constraint."""

    wait_time_weight: Annotated[Optional[int], PropertyInfo(alias="waitTimeWeight")]
    """Weight modifier for wait time constraint."""

    workload_spread_weight: Annotated[Optional[int], PropertyInfo(alias="workloadSpreadWeight")]
    """Weight modifier for service time per vehicle day."""

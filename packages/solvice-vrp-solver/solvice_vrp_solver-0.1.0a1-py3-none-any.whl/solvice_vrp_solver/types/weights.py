# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Weights"]


class Weights(BaseModel):
    allowed_resources_weight: Optional[int] = FieldInfo(alias="allowedResourcesWeight", default=None)
    """Weight modifier for the resources allowed constraint."""

    asap_weight: Optional[int] = FieldInfo(alias="asapWeight", default=None)
    """Weight modifier scheduling jobs as soon (on day basis) as possible."""

    drive_time_weight: Optional[int] = FieldInfo(alias="driveTimeWeight", default=None)
    """Weight modifier for the drive time constraint."""

    minimize_resources_weight: Optional[int] = FieldInfo(alias="minimizeResourcesWeight", default=None)
    """Weight modifier for minimizing activating another resource on a day trip.

    The weight is put on the same balance as travel time. So setting this weight to
    3600 (1hour) will make sure that the solver will try to minimize the number of
    resources used on a day trip compared to 1 extra hour of travel time.
    """

    planned_weight: Optional[int] = FieldInfo(alias="plannedWeight", default=None)
    """Weight modifier for planned vehicle and planned date requirement."""

    priority_weight: Optional[int] = FieldInfo(alias="priorityWeight", default=None)
    """
    Weight modifier for `job.priority` that ensures that priority orders are
    scheduled. Note that this does not make sure that they are scheduled sooner.
    """

    ranking_weight: Optional[int] = FieldInfo(alias="rankingWeight", default=None)
    """Weight modifier for tag ranking preference.

    Higher weight increases the importance of assigning jobs to higher-ranked
    resources.
    """

    travel_time_weight: Optional[int] = FieldInfo(alias="travelTimeWeight", default=None)
    """Weight modifier for travel time."""

    urgency_weight: Optional[int] = FieldInfo(alias="urgencyWeight", default=None)
    """Weight modifier for the urgency constraint."""

    wait_time_weight: Optional[int] = FieldInfo(alias="waitTimeWeight", default=None)
    """Weight modifier for wait time constraint."""

    workload_spread_weight: Optional[int] = FieldInfo(alias="workloadSpreadWeight", default=None)
    """Weight modifier for service time per vehicle day."""

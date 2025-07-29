# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .location import Location

__all__ = ["Job", "Ranking", "Tag", "Window"]


class Ranking(BaseModel):
    name: str
    """The name of the Resource"""

    ranking: Optional[int] = None
    """Resource ranking for this tag (1-100).

    Lower ranking means more preferred resource. When a job is assigned to a
    resource, the score is penalised based on the ranking.
    """


class Tag(BaseModel):
    name: str
    """
    Tag restriction name which can force some Jobs to be scheduled by Resources with
    the same tag
    """

    hard: Optional[bool] = None
    """Hard or soft constraint."""

    weight: Optional[int] = None
    """Value of the weight.

    This will be on the same level as travel time in the case of soft constraint.
    """


class Window(BaseModel):
    from_: str = FieldInfo(alias="from")
    """Date time start of window"""

    to: str
    """Date time end of window"""

    hard: Optional[bool] = None
    """Hard constraint violation of DateWindow"""

    weight: Optional[int] = None
    """Weight constraint modifier"""


class Job(BaseModel):
    name: str
    """Unique description"""

    allowed_resources: Optional[List[str]] = FieldInfo(alias="allowedResources", default=None)
    """List of vehicle names that are allowed to be assigned to this order."""

    complexity: Optional[int] = None
    """Complexity of the job"""

    disallowed_resources: Optional[List[str]] = FieldInfo(alias="disallowedResources", default=None)
    """List of vehicle names that are allowed to be assigned to this order."""

    duration: Optional[int] = None
    """Service duration of the job"""

    duration_squash: Optional[int] = FieldInfo(alias="durationSquash", default=None)
    """
    When a job is performed at the same location as another job, `durationSquash`
    ensures that the 2nd job' service time is reduced to this value. Example:
    `duration=600` and `durationSquash=30` means that the 2nd job will only take 30
    seconds to perform.
    """

    hard: Optional[bool] = None
    """
    In the case of partialPlanning planning, this indicates whether this order
    should be integrated into the planning or not.
    """

    hard_weight: Optional[int] = FieldInfo(alias="hardWeight", default=None)
    """
    In the case of partialPlanning planning, this indicates the weight of this
    order.
    """

    initial_arrival: Optional[str] = FieldInfo(alias="initialArrival", default=None)
    """Warm start for the arrival time.

    Use this to speed up the solver and to start from an initial solution.
    """

    initial_resource: Optional[str] = FieldInfo(alias="initialResource", default=None)
    """
    Warm start for the assigned resource: name of the vehicle to which this job is
    planned. Use this to speed up the solver and to start from an initial solution.
    """

    load: Optional[List[int]] = None
    """Load"""

    location: Optional[Location] = None
    """Geographical Location in WGS-84"""

    padding: Optional[int] = None
    """Padding time before and after the job. In seconds"""

    planned_arrival: Optional[str] = FieldInfo(alias="plannedArrival", default=None)
    """Planned arrival time The second of day at which the order is planned to
    complete.

    The difference with the actual arrival time is scaled in the score with
    plannedWeight.
    """

    planned_date: Optional[str] = FieldInfo(alias="plannedDate", default=None)
    """
    Fixed date on which this order is already planned and should hence be taken into
    account in the planning.
    """

    planned_resource: Optional[str] = FieldInfo(alias="plannedResource", default=None)
    """
    Name of the resource to which this order is already planned and should hence be
    taken into account in the next planning.
    """

    priority: Optional[int] = None
    """
    Priority of the job will ensure that it is included in the planning over other
    lower priority jobs. We evaluate the priority multiplied with the duration of
    the job. The higher the priority, the more likely it is that the job will be
    included in the planning. Defaults to 1.
    """

    rankings: Optional[List[Ranking]] = None
    """
    Rankings define resource preferences for this job, where lower values indicate
    stronger preference for specific resources.
    """

    resumable: Optional[bool] = None
    """Enables job interruption by resource unavailability breaks.

    When true, the job can start before a break, pause during the break, and resume
    afterward. Default: false.
    """

    tags: Optional[List[Tag]] = None
    """A tag is a string that can be used to link jobs to resources."""

    urgency: Optional[int] = None
    """
    Urgency of the job will ensure that it is likely to be scheduled before jobs
    with a lower urgency.
    """

    windows: Optional[List[Window]] = None
    """List of start/end date/time combinations."""

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .location_param import LocationParam

__all__ = ["JobParam", "Ranking", "Tag", "Window"]


class Ranking(TypedDict, total=False):
    name: Required[str]
    """The name of the Resource"""

    ranking: Optional[int]
    """Resource ranking for this tag (1-100).

    Lower ranking means more preferred resource. When a job is assigned to a
    resource, the score is penalised based on the ranking.
    """


class Tag(TypedDict, total=False):
    name: Required[str]
    """
    Tag restriction name which can force some Jobs to be scheduled by Resources with
    the same tag
    """

    hard: Optional[bool]
    """Hard or soft constraint."""

    weight: Optional[int]
    """Value of the weight.

    This will be on the same level as travel time in the case of soft constraint.
    """


_WindowReservedKeywords = TypedDict(
    "_WindowReservedKeywords",
    {
        "from": str,
    },
    total=False,
)


class Window(_WindowReservedKeywords, total=False):
    to: Required[str]
    """Date time end of window"""

    hard: Optional[bool]
    """Hard constraint violation of DateWindow"""

    weight: Optional[int]
    """Weight constraint modifier"""


class JobParam(TypedDict, total=False):
    name: Required[str]
    """Unique description"""

    allowed_resources: Annotated[Optional[List[str]], PropertyInfo(alias="allowedResources")]
    """List of vehicle names that are allowed to be assigned to this order."""

    complexity: Optional[int]
    """Complexity of the job"""

    disallowed_resources: Annotated[Optional[List[str]], PropertyInfo(alias="disallowedResources")]
    """List of vehicle names that are allowed to be assigned to this order."""

    duration: Optional[int]
    """Service duration of the job"""

    duration_squash: Annotated[Optional[int], PropertyInfo(alias="durationSquash")]
    """
    When a job is performed at the same location as another job, `durationSquash`
    ensures that the 2nd job' service time is reduced to this value. Example:
    `duration=600` and `durationSquash=30` means that the 2nd job will only take 30
    seconds to perform.
    """

    hard: Optional[bool]
    """
    In the case of partialPlanning planning, this indicates whether this order
    should be integrated into the planning or not.
    """

    hard_weight: Annotated[Optional[int], PropertyInfo(alias="hardWeight")]
    """
    In the case of partialPlanning planning, this indicates the weight of this
    order.
    """

    initial_arrival: Annotated[Optional[str], PropertyInfo(alias="initialArrival")]
    """Warm start for the arrival time.

    Use this to speed up the solver and to start from an initial solution.
    """

    initial_resource: Annotated[Optional[str], PropertyInfo(alias="initialResource")]
    """
    Warm start for the assigned resource: name of the vehicle to which this job is
    planned. Use this to speed up the solver and to start from an initial solution.
    """

    load: Optional[Iterable[int]]
    """Load"""

    location: Optional[LocationParam]
    """Geographical Location in WGS-84"""

    padding: Optional[int]
    """Padding time before and after the job. In seconds"""

    planned_arrival: Annotated[Optional[str], PropertyInfo(alias="plannedArrival")]
    """Planned arrival time The second of day at which the order is planned to
    complete.

    The difference with the actual arrival time is scaled in the score with
    plannedWeight.
    """

    planned_date: Annotated[Optional[str], PropertyInfo(alias="plannedDate")]
    """
    Fixed date on which this order is already planned and should hence be taken into
    account in the planning.
    """

    planned_resource: Annotated[Optional[str], PropertyInfo(alias="plannedResource")]
    """
    Name of the resource to which this order is already planned and should hence be
    taken into account in the next planning.
    """

    priority: Optional[int]
    """
    Priority of the job will ensure that it is included in the planning over other
    lower priority jobs. We evaluate the priority multiplied with the duration of
    the job. The higher the priority, the more likely it is that the job will be
    included in the planning. Defaults to 1.
    """

    rankings: Optional[Iterable[Ranking]]
    """
    Rankings define resource preferences for this job, where lower values indicate
    stronger preference for specific resources.
    """

    resumable: Optional[bool]
    """Enables job interruption by resource unavailability breaks.

    When true, the job can start before a break, pause during the break, and resume
    afterward. Default: false.
    """

    tags: Optional[Iterable[Tag]]
    """A tag is a string that can be used to link jobs to resources."""

    urgency: Optional[int]
    """
    Urgency of the job will ensure that it is likely to be scheduled before jobs
    with a lower urgency.
    """

    windows: Optional[Iterable[Window]]
    """List of start/end date/time combinations."""

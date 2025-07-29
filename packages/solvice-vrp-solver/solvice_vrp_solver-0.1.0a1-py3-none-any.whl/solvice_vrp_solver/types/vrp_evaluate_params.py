# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .options_param import OptionsParam
from .weights_param import WeightsParam
from .location_param import LocationParam

__all__ = [
    "VrpEvaluateParams",
    "Job",
    "JobRanking",
    "JobTag",
    "JobWindow",
    "Resource",
    "ResourceShift",
    "ResourceShiftBreak",
    "ResourceRule",
    "ResourceRulePeriod",
    "Relation",
]


class VrpEvaluateParams(TypedDict, total=False):
    jobs: Required[Iterable[Job]]
    """List of Jobs"""

    resources: Required[Iterable[Resource]]
    """List of Resources"""

    hook: Optional[str]
    """Webhook endpoint to receive POST request with the id."""

    label: Optional[str]

    options: Optional[OptionsParam]
    """Options to tweak the routing engine"""

    relations: Optional[Iterable[Relation]]

    weights: Optional[WeightsParam]
    """OnRoute Weights"""


class JobRanking(TypedDict, total=False):
    name: Required[str]
    """The name of the Resource"""

    ranking: Optional[int]
    """Resource ranking for this tag (1-100).

    Lower ranking means more preferred resource. When a job is assigned to a
    resource, the score is penalised based on the ranking.
    """


class JobTag(TypedDict, total=False):
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


_JobWindowReservedKeywords = TypedDict(
    "_JobWindowReservedKeywords",
    {
        "from": str,
    },
    total=False,
)


class JobWindow(_JobWindowReservedKeywords, total=False):
    to: Required[str]
    """Date time end of window"""

    hard: Optional[bool]
    """Hard constraint violation of DateWindow"""

    weight: Optional[int]
    """Weight constraint modifier"""


class Job(TypedDict, total=False):
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

    rankings: Optional[Iterable[JobRanking]]
    """
    Rankings define resource preferences for this job, where lower values indicate
    stronger preference for specific resources.
    """

    resumable: Optional[bool]
    """Enables job interruption by resource unavailability breaks.

    When true, the job can start before a break, pause during the break, and resume
    afterward. Default: false.
    """

    tags: Optional[Iterable[JobTag]]
    """A tag is a string that can be used to link jobs to resources."""

    urgency: Optional[int]
    """
    Urgency of the job will ensure that it is likely to be scheduled before jobs
    with a lower urgency.
    """

    windows: Optional[Iterable[JobWindow]]
    """List of start/end date/time combinations."""


class ResourceShiftBreak(TypedDict, total=False):
    type: Required[Literal["WINDOWED", "DRIVE", "UNAVAILABILITY"]]
    """Type of break that can be defined for a resource"""


_ResourceShiftReservedKeywords = TypedDict(
    "_ResourceShiftReservedKeywords",
    {
        "from": str,
    },
    total=False,
)


class ResourceShift(_ResourceShiftReservedKeywords, total=False):
    to: Required[str]
    """End of the shift datetime"""

    breaks: Optional[Iterable[ResourceShiftBreak]]
    """Windowed breaks definitions."""

    end: Optional[LocationParam]
    """Geographical Location in WGS-84"""

    ignore_travel_time_from_last_job: Annotated[Optional[bool], PropertyInfo(alias="ignoreTravelTimeFromLastJob")]
    """Ignore the travel time from the last order to the optional end location"""

    ignore_travel_time_to_first_job: Annotated[Optional[bool], PropertyInfo(alias="ignoreTravelTimeToFirstJob")]
    """Ignore the travel time from the start location to the first order"""

    overtime: object
    """Can go into overtime."""

    overtime_end: Annotated[Optional[str], PropertyInfo(alias="overtimeEnd")]
    """Maximum overtime time."""

    start: Optional[LocationParam]
    """Geographical Location in WGS-84"""

    tags: Optional[List[str]]
    """
    Shift tags will ensure that this resource can only do Jobs of this tag during
    this shift. This allows for tag based availability.
    """


_ResourceRulePeriodReservedKeywords = TypedDict(
    "_ResourceRulePeriodReservedKeywords",
    {
        "from": Union[str, datetime],
    },
    total=False,
)


class ResourceRulePeriod(_ResourceRulePeriodReservedKeywords, total=False):
    end: Required[object]
    """End date-time"""

    to: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]


class ResourceRule(TypedDict, total=False):
    max_drive_time: Annotated[Optional[int], PropertyInfo(alias="maxDriveTime")]
    """Maximum drive time in seconds"""

    max_job_complexity: Annotated[Optional[int], PropertyInfo(alias="maxJobComplexity")]
    """
    Sum of the complexity of the jobs completed by this resource should not go over
    this value
    """

    max_service_time: Annotated[Optional[int], PropertyInfo(alias="maxServiceTime")]
    """Maximum service time in seconds"""

    max_work_time: Annotated[Optional[int], PropertyInfo(alias="maxWorkTime")]
    """Maximum work time in seconds. Work time is service time + drive/travel time."""

    min_drive_time: Annotated[Optional[int], PropertyInfo(alias="minDriveTime")]
    """Minimum drive time in seconds"""

    min_job_complexity: Annotated[Optional[int], PropertyInfo(alias="minJobComplexity")]
    """
    Sum of the complexity of the jobs completed by this resource should reach this
    value
    """

    min_service_time: Annotated[Optional[int], PropertyInfo(alias="minServiceTime")]
    """Minimum service time in seconds"""

    min_work_time: Annotated[Optional[int], PropertyInfo(alias="minWorkTime")]
    """Minimum work time in seconds. Work time is service time + drive/travel time."""

    period: ResourceRulePeriod
    """Subset of the planning period"""


class Resource(TypedDict, total=False):
    name: Required[str]
    """Unique name"""

    shifts: Required[Optional[Iterable[ResourceShift]]]
    """Shift definition of a Resource over course of planning period"""

    capacity: Optional[Iterable[int]]
    """Capacity"""

    category: Optional[Literal["CAR", "BIKE", "TRUCK"]]
    """Transportation type for the resource"""

    end: Optional[LocationParam]
    """Geographical Location in WGS-84"""

    hourly_cost: Annotated[Optional[int], PropertyInfo(alias="hourlyCost")]
    """Financial cost per hour per resource.

    Only calculated when working (driving, servicing or waiting)
    """

    max_drive_time: Annotated[Optional[int], PropertyInfo(alias="maxDriveTime")]

    max_drive_time_in_seconds: Annotated[object, PropertyInfo(alias="maxDriveTimeInSeconds")]
    """Maximum drive time in seconds"""

    max_drive_time_job: Annotated[Optional[int], PropertyInfo(alias="maxDriveTimeJob")]

    region: Optional[LocationParam]
    """Geographical Location in WGS-84"""

    rules: Optional[Iterable[ResourceRule]]
    """Periodic Rules"""

    start: Optional[LocationParam]
    """Geographical Location in WGS-84"""

    tags: Optional[List[str]]
    """Tag requirements"""


class Relation(TypedDict, total=False):
    jobs: Required[List[str]]
    """List of job names. This can be sequence dependent."""

    time_interval: Required[Annotated[Literal["FROM_ARRIVAL", "FROM_DEPARTURE"], PropertyInfo(alias="timeInterval")]]
    """
    Determines if the time interval between jobs should be measured from arrival or
    departure
    """

    type: Required[
        Literal[
            "SAME_TRIP",
            "SEQUENCE",
            "DIRECT_SEQUENCE",
            "SAME_TIME",
            "NEIGHBOR",
            "PICKUP_AND_DELIVERY",
            "SAME_RESOURCE",
            "SAME_DAY",
            "GROUP_SEQUENCE",
        ]
    ]
    """Type of relation between jobs"""

    max_time_interval: Annotated[Optional[int], PropertyInfo(alias="maxTimeInterval")]
    """Maximum seconds between two jobs in a SEQUENCE relation."""

    max_waiting_time: Annotated[Optional[int], PropertyInfo(alias="maxWaitingTime")]
    """
    In case of a `SAME_TIME` relation, the maximum waiting time in seconds between
    the jobs. Defaults to `1200` seconds or `20` minutes.
    """

    min_time_interval: Annotated[Optional[int], PropertyInfo(alias="minTimeInterval")]
    """Minimum seconds between two jobs in a SEQUENCE relation."""

    partial_planning: Annotated[bool, PropertyInfo(alias="partialPlanning")]
    """
    Allows the solver to plan a subset of the jobs in the job relation when
    overconstrained
    """

    resource: Optional[str]
    """Optional resource"""

    tags: Optional[List[str]]
    """
    When using the GROUP_SEQUENCE relation it is used to define the job groups by
    inserting the tags that differentiate them
    """

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .options import Options
from .weights import Weights
from .._models import BaseModel
from .location import Location

__all__ = [
    "OnRouteRequest",
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


class JobRanking(BaseModel):
    name: str
    """The name of the Resource"""

    ranking: Optional[int] = None
    """Resource ranking for this tag (1-100).

    Lower ranking means more preferred resource. When a job is assigned to a
    resource, the score is penalised based on the ranking.
    """


class JobTag(BaseModel):
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


class JobWindow(BaseModel):
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

    rankings: Optional[List[JobRanking]] = None
    """
    Rankings define resource preferences for this job, where lower values indicate
    stronger preference for specific resources.
    """

    resumable: Optional[bool] = None
    """Enables job interruption by resource unavailability breaks.

    When true, the job can start before a break, pause during the break, and resume
    afterward. Default: false.
    """

    tags: Optional[List[JobTag]] = None
    """A tag is a string that can be used to link jobs to resources."""

    urgency: Optional[int] = None
    """
    Urgency of the job will ensure that it is likely to be scheduled before jobs
    with a lower urgency.
    """

    windows: Optional[List[JobWindow]] = None
    """List of start/end date/time combinations."""


class ResourceShiftBreak(BaseModel):
    type: Literal["WINDOWED", "DRIVE", "UNAVAILABILITY"]
    """Type of break that can be defined for a resource"""


class ResourceShift(BaseModel):
    from_: str = FieldInfo(alias="from")
    """Start of the shift datetime"""

    to: str
    """End of the shift datetime"""

    breaks: Optional[List[ResourceShiftBreak]] = None
    """Windowed breaks definitions."""

    end: Optional[Location] = None
    """Geographical Location in WGS-84"""

    ignore_travel_time_from_last_job: Optional[bool] = FieldInfo(alias="ignoreTravelTimeFromLastJob", default=None)
    """Ignore the travel time from the last order to the optional end location"""

    ignore_travel_time_to_first_job: Optional[bool] = FieldInfo(alias="ignoreTravelTimeToFirstJob", default=None)
    """Ignore the travel time from the start location to the first order"""

    overtime: Optional[object] = None
    """Can go into overtime."""

    overtime_end: Optional[str] = FieldInfo(alias="overtimeEnd", default=None)
    """Maximum overtime time."""

    start: Optional[Location] = None
    """Geographical Location in WGS-84"""

    tags: Optional[List[str]] = None
    """
    Shift tags will ensure that this resource can only do Jobs of this tag during
    this shift. This allows for tag based availability.
    """


class ResourceRulePeriod(BaseModel):
    end: object
    """End date-time"""

    from_: datetime = FieldInfo(alias="from")
    """Start date-time"""

    to: datetime


class ResourceRule(BaseModel):
    max_drive_time: Optional[int] = FieldInfo(alias="maxDriveTime", default=None)
    """Maximum drive time in seconds"""

    max_job_complexity: Optional[int] = FieldInfo(alias="maxJobComplexity", default=None)
    """
    Sum of the complexity of the jobs completed by this resource should not go over
    this value
    """

    max_service_time: Optional[int] = FieldInfo(alias="maxServiceTime", default=None)
    """Maximum service time in seconds"""

    max_work_time: Optional[int] = FieldInfo(alias="maxWorkTime", default=None)
    """Maximum work time in seconds. Work time is service time + drive/travel time."""

    min_drive_time: Optional[int] = FieldInfo(alias="minDriveTime", default=None)
    """Minimum drive time in seconds"""

    min_job_complexity: Optional[int] = FieldInfo(alias="minJobComplexity", default=None)
    """
    Sum of the complexity of the jobs completed by this resource should reach this
    value
    """

    min_service_time: Optional[int] = FieldInfo(alias="minServiceTime", default=None)
    """Minimum service time in seconds"""

    min_work_time: Optional[int] = FieldInfo(alias="minWorkTime", default=None)
    """Minimum work time in seconds. Work time is service time + drive/travel time."""

    period: Optional[ResourceRulePeriod] = None
    """Subset of the planning period"""


class Resource(BaseModel):
    name: str
    """Unique name"""

    shifts: Optional[List[ResourceShift]] = None
    """Shift definition of a Resource over course of planning period"""

    capacity: Optional[List[int]] = None
    """Capacity"""

    category: Optional[Literal["CAR", "BIKE", "TRUCK"]] = None
    """Transportation type for the resource"""

    end: Optional[Location] = None
    """Geographical Location in WGS-84"""

    hourly_cost: Optional[int] = FieldInfo(alias="hourlyCost", default=None)
    """Financial cost per hour per resource.

    Only calculated when working (driving, servicing or waiting)
    """

    max_drive_time: Optional[int] = FieldInfo(alias="maxDriveTime", default=None)

    max_drive_time_in_seconds: Optional[object] = FieldInfo(alias="maxDriveTimeInSeconds", default=None)
    """Maximum drive time in seconds"""

    max_drive_time_job: Optional[int] = FieldInfo(alias="maxDriveTimeJob", default=None)

    region: Optional[Location] = None
    """Geographical Location in WGS-84"""

    rules: Optional[List[ResourceRule]] = None
    """Periodic Rules"""

    start: Optional[Location] = None
    """Geographical Location in WGS-84"""

    tags: Optional[List[str]] = None
    """Tag requirements"""


class Relation(BaseModel):
    jobs: List[str]
    """List of job names. This can be sequence dependent."""

    time_interval: Literal["FROM_ARRIVAL", "FROM_DEPARTURE"] = FieldInfo(alias="timeInterval")
    """
    Determines if the time interval between jobs should be measured from arrival or
    departure
    """

    type: Literal[
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
    """Type of relation between jobs"""

    max_time_interval: Optional[int] = FieldInfo(alias="maxTimeInterval", default=None)
    """Maximum seconds between two jobs in a SEQUENCE relation."""

    max_waiting_time: Optional[int] = FieldInfo(alias="maxWaitingTime", default=None)
    """
    In case of a `SAME_TIME` relation, the maximum waiting time in seconds between
    the jobs. Defaults to `1200` seconds or `20` minutes.
    """

    min_time_interval: Optional[int] = FieldInfo(alias="minTimeInterval", default=None)
    """Minimum seconds between two jobs in a SEQUENCE relation."""

    partial_planning: Optional[bool] = FieldInfo(alias="partialPlanning", default=None)
    """
    Allows the solver to plan a subset of the jobs in the job relation when
    overconstrained
    """

    resource: Optional[str] = None
    """Optional resource"""

    tags: Optional[List[str]] = None
    """
    When using the GROUP_SEQUENCE relation it is used to define the job groups by
    inserting the tags that differentiate them
    """


class OnRouteRequest(BaseModel):
    jobs: List[Job]
    """List of Jobs"""

    resources: List[Resource]
    """List of Resources"""

    hook: Optional[str] = None
    """Webhook endpoint to receive POST request with the id."""

    label: Optional[str] = None

    options: Optional[Options] = None
    """Options to tweak the routing engine"""

    relations: Optional[List[Relation]] = None

    weights: Optional[Weights] = None
    """OnRoute Weights"""

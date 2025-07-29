# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .location_param import LocationParam

__all__ = ["ResourceParam", "Shift", "ShiftBreak", "Rule", "RulePeriod"]


class ShiftBreak(TypedDict, total=False):
    type: Required[Literal["WINDOWED", "DRIVE", "UNAVAILABILITY"]]
    """Type of break that can be defined for a resource"""


_ShiftReservedKeywords = TypedDict(
    "_ShiftReservedKeywords",
    {
        "from": str,
    },
    total=False,
)


class Shift(_ShiftReservedKeywords, total=False):
    to: Required[str]
    """End of the shift datetime"""

    breaks: Optional[Iterable[ShiftBreak]]
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


_RulePeriodReservedKeywords = TypedDict(
    "_RulePeriodReservedKeywords",
    {
        "from": Union[str, datetime],
    },
    total=False,
)


class RulePeriod(_RulePeriodReservedKeywords, total=False):
    end: Required[object]
    """End date-time"""

    to: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]


class Rule(TypedDict, total=False):
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

    period: RulePeriod
    """Subset of the planning period"""


class ResourceParam(TypedDict, total=False):
    name: Required[str]
    """Unique name"""

    shifts: Required[Optional[Iterable[Shift]]]
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

    rules: Optional[Iterable[Rule]]
    """Periodic Rules"""

    start: Optional[LocationParam]
    """Geographical Location in WGS-84"""

    tags: Optional[List[str]]
    """Tag requirements"""

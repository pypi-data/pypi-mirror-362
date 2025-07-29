# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .location import Location

__all__ = ["Resource", "Shift", "ShiftBreak", "Rule", "RulePeriod"]


class ShiftBreak(BaseModel):
    type: Literal["WINDOWED", "DRIVE", "UNAVAILABILITY"]
    """Type of break that can be defined for a resource"""


class Shift(BaseModel):
    from_: str = FieldInfo(alias="from")
    """Start of the shift datetime"""

    to: str
    """End of the shift datetime"""

    breaks: Optional[List[ShiftBreak]] = None
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


class RulePeriod(BaseModel):
    end: object
    """End date-time"""

    from_: datetime = FieldInfo(alias="from")
    """Start date-time"""

    to: datetime


class Rule(BaseModel):
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

    period: Optional[RulePeriod] = None
    """Subset of the planning period"""


class Resource(BaseModel):
    name: str
    """Unique name"""

    shifts: Optional[List[Shift]] = None
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

    rules: Optional[List[Rule]] = None
    """Periodic Rules"""

    start: Optional[Location] = None
    """Geographical Location in WGS-84"""

    tags: Optional[List[str]] = None
    """Tag requirements"""

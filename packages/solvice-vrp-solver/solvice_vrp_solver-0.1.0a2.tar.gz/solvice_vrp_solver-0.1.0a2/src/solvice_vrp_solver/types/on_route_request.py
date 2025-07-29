# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .job import Job
from .options import Options
from .weights import Weights
from .._models import BaseModel
from .resource import Resource

__all__ = ["OnRouteRequest", "Relation"]


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

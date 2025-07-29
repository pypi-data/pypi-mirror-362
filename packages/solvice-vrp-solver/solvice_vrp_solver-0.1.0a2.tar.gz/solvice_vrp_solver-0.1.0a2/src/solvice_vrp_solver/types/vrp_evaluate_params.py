# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .job_param import JobParam
from .options_param import OptionsParam
from .weights_param import WeightsParam
from .resource_param import ResourceParam

__all__ = ["VrpEvaluateParams", "Relation"]


class VrpEvaluateParams(TypedDict, total=False):
    jobs: Required[Iterable[JobParam]]
    """List of Jobs"""

    resources: Required[Iterable[ResourceParam]]
    """List of Resources"""

    hook: Optional[str]
    """Webhook endpoint to receive POST request with the id."""

    label: Optional[str]

    options: Optional[OptionsParam]
    """Options to tweak the routing engine"""

    relations: Optional[Iterable[Relation]]

    weights: Optional[WeightsParam]
    """OnRoute Weights"""


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

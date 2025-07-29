# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .onroute_constraint import OnrouteConstraint

__all__ = ["JobExplanationResponse", "Score", "Conflicts", "Unresolved"]


class Score(BaseModel):
    feasible: Optional[bool] = None

    hard_score: Optional[int] = FieldInfo(alias="hardScore", default=None)
    """The score of the constraints that are hard.

    This should be 0 in order to be feasible.
    """

    medium_score: Optional[int] = FieldInfo(alias="mediumScore", default=None)
    """The score of the constraints that are medium."""

    soft_score: Optional[int] = FieldInfo(alias="softScore", default=None)
    """The score of the constraints that are soft."""


class Conflicts(BaseModel):
    constraint: str
    """Constraint type."""

    score: str
    """Score impact of this conflict."""

    job: Optional[str] = None
    """Job id."""

    relation: Optional[str] = None

    resource: Optional[str] = None
    """Resource id."""

    tag: Optional[str] = None
    """Tag id."""


class Unresolved(BaseModel):
    constraint: OnrouteConstraint
    """Types of constraints that can be violated in a routing solution"""

    score: str
    """Score impact of this conflict."""


class JobExplanationResponse(BaseModel):
    score: Optional[Score] = None
    """Score of the solution."""

    alternatives: Optional[Dict[str, object]] = None
    """
    When `options.explanation.enabled` is set to `true`, this field will contain the
    alternatives for the solution.The key is the job name and the value is the list
    of assignments. Each assignment contains the resource, the date, and the score.
    In this way, you can check the impact of the alternative on the score.
    """

    conflicts: Optional[Conflicts] = None
    """Conflicts in the solution"""

    unresolved: Optional[Unresolved] = None
    """Unresolved constraints in the solution"""

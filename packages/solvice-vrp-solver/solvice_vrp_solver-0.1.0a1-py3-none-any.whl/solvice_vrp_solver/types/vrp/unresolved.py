# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel
from .onroute_constraint import OnrouteConstraint

__all__ = ["Unresolved"]


class Unresolved(BaseModel):
    constraint: OnrouteConstraint
    """Types of constraints that can be violated in a routing solution"""

    score: str
    """Score impact of this conflict."""

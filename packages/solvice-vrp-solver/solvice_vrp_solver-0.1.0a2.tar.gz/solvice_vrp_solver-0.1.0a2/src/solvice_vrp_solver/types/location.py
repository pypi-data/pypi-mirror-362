# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["Location"]


class Location(BaseModel):
    latitude: Optional[float] = None
    """Latitude"""

    longitude: Optional[float] = None
    """Longitude"""

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["LocationParam"]


class LocationParam(TypedDict, total=False):
    latitude: float
    """Latitude"""

    longitude: float
    """Longitude"""

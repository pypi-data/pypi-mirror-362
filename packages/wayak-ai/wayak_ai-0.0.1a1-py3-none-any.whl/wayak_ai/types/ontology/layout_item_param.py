# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["LayoutItemParam", "Position"]


class Position(TypedDict, total=False):
    h: Required[int]
    """Height of the item"""

    w: Required[int]
    """Width of the item"""

    x: Required[int]
    """X coordinate (horizontal position)"""

    y: Required[int]
    """Y coordinate (vertical position)"""


class LayoutItemParam(TypedDict, total=False):
    metric_id: Required[Annotated[str, PropertyInfo(alias="metricId")]]
    """ID of the metric to display"""

    position: Optional[Position]
    """Model representing the position and size of a metric in the dashboard layout"""

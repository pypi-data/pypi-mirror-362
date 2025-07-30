# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["LayoutItem", "Position"]


class Position(BaseModel):
    h: int
    """Height of the item"""

    w: int
    """Width of the item"""

    x: int
    """X coordinate (horizontal position)"""

    y: int
    """Y coordinate (vertical position)"""


class LayoutItem(BaseModel):
    metric_id: str = FieldInfo(alias="metricId")
    """ID of the metric to display"""

    position: Optional[Position] = None
    """Model representing the position and size of a metric in the dashboard layout"""

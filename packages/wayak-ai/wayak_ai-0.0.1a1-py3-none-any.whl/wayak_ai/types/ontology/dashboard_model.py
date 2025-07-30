# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ..._models import BaseModel
from .layout_item import LayoutItem

__all__ = ["DashboardModel"]


class DashboardModel(BaseModel):
    created_at: datetime

    edited_at: datetime

    name: str
    """Name of the dashboard"""

    org_id: str
    """Organization ID"""

    id: Optional[str] = None

    description: Optional[str] = None
    """Description of the dashboard"""

    layout: Optional[List[LayoutItem]] = None
    """Layout configuration for dashboard metrics"""

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import TypedDict

from .layout_item_param import LayoutItemParam

__all__ = ["DashboardUpdateParams"]


class DashboardUpdateParams(TypedDict, total=False):
    description: Optional[str]

    layout: Optional[Iterable[LayoutItemParam]]

    name: Optional[str]

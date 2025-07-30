# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

from .layout_item_param import LayoutItemParam

__all__ = ["DashboardCreateParams"]


class DashboardCreateParams(TypedDict, total=False):
    name: Required[str]

    org_id: Required[str]

    description: Optional[str]

    layout: Optional[Iterable[LayoutItemParam]]

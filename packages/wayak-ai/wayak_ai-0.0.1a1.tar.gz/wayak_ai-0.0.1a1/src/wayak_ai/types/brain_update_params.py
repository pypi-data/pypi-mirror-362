# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

__all__ = ["BrainUpdateParams"]


class BrainUpdateParams(TypedDict, total=False):
    backstory: Optional[str]

    goal: Optional[str]

    name: Optional[str]

    org_id: Optional[str]

    prebuilt_tools: Optional[List[str]]

    role: Optional[str]

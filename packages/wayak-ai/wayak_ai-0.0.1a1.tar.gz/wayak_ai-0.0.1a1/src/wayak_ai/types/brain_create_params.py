# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

__all__ = ["BrainCreateParams"]


class BrainCreateParams(TypedDict, total=False):
    backstory: Required[str]

    creator_id: Required[str]

    goal: Required[str]

    name: Required[str]

    role: Required[str]

    org_id: Optional[str]

    prebuilt_tools: Optional[List[str]]

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ThreadCreateParams"]


class ThreadCreateParams(TypedDict, total=False):
    model: Required[str]

    title: Required[str]

    user_id: Required[str]

    description: Optional[str]

    org_id: Optional[str]

    project_id: Optional[str]

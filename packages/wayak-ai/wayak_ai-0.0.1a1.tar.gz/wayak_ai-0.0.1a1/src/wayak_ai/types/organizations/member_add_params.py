# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .role import Role

__all__ = ["MemberAddParams"]


class MemberAddParams(TypedDict, total=False):
    current_user_id: Required[str]

    role: Required[Role]

    user_id: Required[str]

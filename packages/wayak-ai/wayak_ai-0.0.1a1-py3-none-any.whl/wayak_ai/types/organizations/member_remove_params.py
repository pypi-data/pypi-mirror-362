# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["MemberRemoveParams"]


class MemberRemoveParams(TypedDict, total=False):
    org_id: Required[str]

    current_user_id: Required[str]

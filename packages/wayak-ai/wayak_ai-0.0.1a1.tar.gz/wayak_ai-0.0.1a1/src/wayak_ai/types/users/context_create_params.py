# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ContextCreateParams"]


class ContextCreateParams(TypedDict, total=False):
    company_description: Required[str]

    name: Required[str]

    role: Required[str]

    user_id: Required[str]

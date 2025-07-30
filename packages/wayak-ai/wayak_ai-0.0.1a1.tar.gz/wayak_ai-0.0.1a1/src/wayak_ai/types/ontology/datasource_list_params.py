# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DatasourceListParams"]


class DatasourceListParams(TypedDict, total=False):
    org_id: Required[str]
    """Organization ID"""

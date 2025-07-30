# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["UserListThreadsParams"]


class UserListThreadsParams(TypedDict, total=False):
    limit: int
    """The maximum number of threads to return. No limit by default"""

    org_id: str
    """The ID of the organization to filter threads by"""

    project_id: str
    """The ID of the project to filter threads by"""

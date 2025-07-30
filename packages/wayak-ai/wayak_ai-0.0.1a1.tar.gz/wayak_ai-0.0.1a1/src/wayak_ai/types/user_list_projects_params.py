# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["UserListProjectsParams"]


class UserListProjectsParams(TypedDict, total=False):
    limit: int
    """The maximum number of projects to return. No limit by default"""

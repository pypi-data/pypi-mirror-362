# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ClickhouseConfigParam"]


class ClickhouseConfigParam(TypedDict, total=False):
    host: Required[str]
    """Host of the clickhouse instance"""

    password: Required[str]
    """Password of the clickhouse instance"""

    username: Required[str]
    """Username of the clickhouse instance"""

    port: int

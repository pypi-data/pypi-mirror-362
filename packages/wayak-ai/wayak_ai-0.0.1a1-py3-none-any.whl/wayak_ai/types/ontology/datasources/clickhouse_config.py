# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ...._models import BaseModel

__all__ = ["ClickhouseConfig"]


class ClickhouseConfig(BaseModel):
    host: str
    """Host of the clickhouse instance"""

    password: str
    """Password of the clickhouse instance"""

    username: str
    """Username of the clickhouse instance"""

    port: Optional[int] = None

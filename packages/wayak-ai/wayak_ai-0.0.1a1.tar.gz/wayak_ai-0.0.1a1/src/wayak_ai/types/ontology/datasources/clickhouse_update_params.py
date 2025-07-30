# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from ...._utils import PropertyInfo
from .supported_data_sources import SupportedDataSources
from .clickhouse_config_param import ClickhouseConfigParam

__all__ = ["ClickhouseUpdateParams", "Config"]


class ClickhouseUpdateParams(TypedDict, total=False):
    config: Required[Config]
    """Configuration for the data source"""

    created_at: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    edited_at: Required[Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]]

    name: Required[str]
    """Name of the data source"""

    org_id: Required[str]
    """Organization ID of the data source"""

    type: Required[SupportedDataSources]
    """Type of the data source"""

    id: Optional[str]

    description: Optional[str]
    """Guidelines to use for the data source"""

    schema: Optional[str]
    """Schema of the data source"""


Config: TypeAlias = Union[Dict[str, object], ClickhouseConfigParam]

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .clickhouse_config import ClickhouseConfig
from .supported_data_sources import SupportedDataSources

__all__ = ["DataSourceModel", "Config"]

Config: TypeAlias = Union[Dict[str, object], ClickhouseConfig]


class DataSourceModel(BaseModel):
    config: Config
    """Configuration for the data source"""

    created_at: datetime

    edited_at: Optional[datetime] = None

    name: str
    """Name of the data source"""

    org_id: str
    """Organization ID of the data source"""

    type: SupportedDataSources
    """Type of the data source"""

    id: Optional[str] = None

    description: Optional[str] = None
    """Guidelines to use for the data source"""

    schema_: Optional[str] = FieldInfo(alias="schema", default=None)
    """Schema of the data source"""

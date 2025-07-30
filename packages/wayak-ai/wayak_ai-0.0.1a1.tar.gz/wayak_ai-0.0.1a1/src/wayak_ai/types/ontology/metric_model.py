# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from ..._models import BaseModel
from .metric_status_enum import MetricStatusEnum
from .chart_visualization_type import ChartVisualizationType

__all__ = ["MetricModel"]


class MetricModel(BaseModel):
    created_at: datetime

    datasource_id: str
    """ID of the datasource this metric uses"""

    edited_at: datetime

    org_id: str
    """Organization ID"""

    query: str
    """SQL query for the metric"""

    status: MetricStatusEnum
    """Status of the metric"""

    title: str
    """Title of the metric"""

    vizualisation: ChartVisualizationType
    """Type of visualization for the metric"""

    id: Optional[str] = None

    chart_config: Optional[Dict[str, object]] = None
    """Configuration for the chart visualization"""

    code: Optional[str] = None
    """Additional code for metric processing"""

    description: Optional[str] = None
    """Description of the metric"""

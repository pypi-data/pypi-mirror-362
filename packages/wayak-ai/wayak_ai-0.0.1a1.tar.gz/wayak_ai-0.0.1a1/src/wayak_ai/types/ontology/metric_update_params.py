# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

from .metric_status_enum import MetricStatusEnum
from .chart_visualization_type import ChartVisualizationType

__all__ = ["MetricUpdateParams"]


class MetricUpdateParams(TypedDict, total=False):
    chart_config: Optional[Dict[str, object]]

    code: Optional[str]

    datasource_id: Optional[str]

    description: Optional[str]

    query: Optional[str]

    status: Optional[MetricStatusEnum]
    """Status of a metric"""

    title: Optional[str]

    vizualisation: Optional[ChartVisualizationType]
    """Types of chart visualizations available for metrics"""

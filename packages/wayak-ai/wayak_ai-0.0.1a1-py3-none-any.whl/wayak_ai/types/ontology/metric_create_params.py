# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

from .metric_status_enum import MetricStatusEnum
from .chart_visualization_type import ChartVisualizationType

__all__ = ["MetricCreateParams"]


class MetricCreateParams(TypedDict, total=False):
    datasource_id: Required[str]

    org_id: Required[str]

    query: Required[str]

    title: Required[str]

    vizualisation: Required[ChartVisualizationType]
    """Types of chart visualizations available for metrics"""

    chart_config: Optional[Dict[str, object]]

    code: Optional[str]

    description: Optional[str]

    status: Optional[MetricStatusEnum]
    """Status of a metric"""

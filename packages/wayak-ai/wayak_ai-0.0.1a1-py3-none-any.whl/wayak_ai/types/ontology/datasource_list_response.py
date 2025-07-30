# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .datasources.data_source_model import DataSourceModel

__all__ = ["DatasourceListResponse"]

DatasourceListResponse: TypeAlias = List[DataSourceModel]

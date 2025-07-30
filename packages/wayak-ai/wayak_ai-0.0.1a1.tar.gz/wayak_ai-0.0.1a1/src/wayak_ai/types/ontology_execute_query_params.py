# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["OntologyExecuteQueryParams"]


class OntologyExecuteQueryParams(TypedDict, total=False):
    datasource_id: Required[str]
    """ID of the datasource to use"""

    sql_query: Required[str]

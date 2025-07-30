# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["OntologyExecuteQueryResponse"]


class OntologyExecuteQueryResponse(BaseModel):
    dimensions: List[str]

    source: List[List[object]]

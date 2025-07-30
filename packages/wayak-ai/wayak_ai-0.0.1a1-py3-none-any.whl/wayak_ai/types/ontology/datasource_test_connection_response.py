# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["DatasourceTestConnectionResponse"]


class DatasourceTestConnectionResponse(BaseModel):
    message: str
    """A message describing the result."""

    status: str
    """The status of the connection test."""

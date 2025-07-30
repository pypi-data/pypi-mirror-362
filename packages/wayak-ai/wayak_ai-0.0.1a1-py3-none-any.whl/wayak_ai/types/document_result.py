# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["DocumentResult"]


class DocumentResult(BaseModel):
    content: str

    document_id: str

    document_url: str

    file_name: str

    page_number: int

    result_number: Optional[int] = None

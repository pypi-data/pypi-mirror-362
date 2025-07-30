# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["PersistentFile"]


class PersistentFile(BaseModel):
    created_at: datetime

    file_indexed: bool

    file_name: str

    file_type: str

    index_status: Literal["NOT_INDEXED", "PROCESSING", "ERROR", "SUCCESS"]

    indexed_pages: Optional[int] = None

    project_id: str

    storage_url: str

    total_pages: Optional[int] = None

    web_url: Optional[str] = None

    id: Optional[str] = None

    file_summary: Optional[str] = None

    indexing_version: Optional[Literal["UNKNOWN", "V1"]] = None

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .persistent_thread import PersistentThread

__all__ = ["UserListThreadsResponse"]


class UserListThreadsResponse(BaseModel):
    results: List[PersistentThread]

    total_count: int

    page_size: Optional[int] = None

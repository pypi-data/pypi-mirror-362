# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .persistent_project import PersistentProject

__all__ = ["UserListProjectsResponse"]


class UserListProjectsResponse(BaseModel):
    results: List[PersistentProject]

    total_count: int

    page_size: Optional[int] = None

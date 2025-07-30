# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["PersistentBrain"]


class PersistentBrain(BaseModel):
    backstory: str

    created_at: datetime

    creator_id: str

    goal: str

    name: str

    role: str

    id: Optional[str] = None

    org_id: Optional[str] = None

    prebuilt_tools: Optional[List[str]] = None

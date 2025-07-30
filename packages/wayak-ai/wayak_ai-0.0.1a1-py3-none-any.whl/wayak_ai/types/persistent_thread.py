# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["PersistentThread"]


class PersistentThread(BaseModel):
    created_at: datetime

    description: Optional[str] = None

    edited_at: datetime

    model: str

    project_id: Optional[str] = None

    title: Optional[str] = None

    user_id: str

    id: Optional[str] = None

    deleted_at: Optional[datetime] = None

    org_id: Optional[str] = None

    usage_synced_at: Optional[datetime] = None

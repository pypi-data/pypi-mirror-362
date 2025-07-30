# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["PersistentUserContext"]


class PersistentUserContext(BaseModel):
    company_description: str

    created_at: datetime

    name: str

    role: str

    user_id: str

    id: Optional[str] = None

    org_id: Optional[str] = None

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .role import Role
from ..._models import BaseModel

__all__ = ["MemberAddResponse"]


class MemberAddResponse(BaseModel):
    created_at: datetime

    edited_at: datetime

    org_id: str

    role: Role

    user_id: str

    id: Optional[str] = None

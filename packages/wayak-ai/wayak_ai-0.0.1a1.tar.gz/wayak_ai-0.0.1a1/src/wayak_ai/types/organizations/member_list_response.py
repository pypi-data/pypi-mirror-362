# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .role import Role
from ..._models import BaseModel
from ..users.persistent_user_profile import PersistentUserProfile

__all__ = ["MemberListResponse", "OrgMember"]


class OrgMember(BaseModel):
    created_at: datetime

    edited_at: datetime

    org_id: str

    profiles: PersistentUserProfile

    role: Role

    user_id: str

    id: Optional[str] = None


class MemberListResponse(BaseModel):
    org_members: List[OrgMember]

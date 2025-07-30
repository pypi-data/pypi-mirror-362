# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["PersistentUserProfile"]


class PersistentUserProfile(BaseModel):
    id: str

    email: str

    name: str

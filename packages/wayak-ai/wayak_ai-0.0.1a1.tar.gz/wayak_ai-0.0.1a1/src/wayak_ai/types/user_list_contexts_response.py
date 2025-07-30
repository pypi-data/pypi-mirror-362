# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .users.persistent_user_context import PersistentUserContext

__all__ = ["UserListContextsResponse"]

UserListContextsResponse: TypeAlias = List[PersistentUserContext]

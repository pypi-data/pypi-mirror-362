# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .persistent_thread import PersistentThread

__all__ = ["OrganizationGetThreadsResponse"]

OrganizationGetThreadsResponse: TypeAlias = List[PersistentThread]

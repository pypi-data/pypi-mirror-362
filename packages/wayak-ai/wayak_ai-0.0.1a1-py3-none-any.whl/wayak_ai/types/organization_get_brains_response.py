# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .persistent_brain import PersistentBrain

__all__ = ["OrganizationGetBrainsResponse"]

OrganizationGetBrainsResponse: TypeAlias = List[PersistentBrain]

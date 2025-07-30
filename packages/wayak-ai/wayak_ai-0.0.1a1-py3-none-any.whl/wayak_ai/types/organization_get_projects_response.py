# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .persistent_project import PersistentProject

__all__ = ["OrganizationGetProjectsResponse"]

OrganizationGetProjectsResponse: TypeAlias = List[PersistentProject]

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from ..persistent_file import PersistentFile

__all__ = ["FileListResponse"]

FileListResponse: TypeAlias = List[PersistentFile]

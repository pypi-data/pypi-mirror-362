# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["MessageParam"]


class MessageParam(TypedDict, total=False):
    content: Required[str]

    role: Required[str]

    id: Optional[str]

    created_at: Annotated[Union[str, datetime, None], PropertyInfo(alias="createdAt", format="iso8601")]

    images: Optional[List[str]]

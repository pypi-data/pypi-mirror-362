# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Required, TypedDict

__all__ = ["MessageCreateParams"]


class MessageCreateParams(TypedDict, total=False):
    content: Required[Dict[str, object]]

    models: Required[List[str]]

    role: Required[str]

    thread_id: Required[str]

    citations: Optional[List[str]]

    documents: Optional[Dict[str, object]]

    images: Optional[List[str]]

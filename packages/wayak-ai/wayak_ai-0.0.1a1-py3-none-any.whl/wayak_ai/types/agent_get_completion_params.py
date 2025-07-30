# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .message_param import MessageParam

__all__ = ["AgentGetCompletionParams"]


class AgentGetCompletionParams(TypedDict, total=False):
    messages: Required[Iterable[MessageParam]]

    model: str

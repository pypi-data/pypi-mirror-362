# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .message_param import MessageParam

__all__ = ["AgentSendMessageToAgentParams"]


class AgentSendMessageToAgentParams(TypedDict, total=False):
    messages: Required[Iterable[MessageParam]]

    thread_id: Required[Annotated[str, PropertyInfo(alias="threadId")]]

    file_ids: Annotated[Optional[List[str]], PropertyInfo(alias="fileIds")]

    model: Optional[str]

    org_id: Annotated[Optional[str], PropertyInfo(alias="orgId")]

    project_id: Annotated[Optional[str], PropertyInfo(alias="projectId")]

    save_messages: Annotated[Optional[bool], PropertyInfo(alias="saveMessages")]

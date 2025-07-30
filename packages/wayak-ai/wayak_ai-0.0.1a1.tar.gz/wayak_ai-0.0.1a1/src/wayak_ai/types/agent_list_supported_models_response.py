# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["AgentListSupportedModelsResponse", "AgentListSupportedModelsResponseItem"]


class AgentListSupportedModelsResponseItem(BaseModel):
    description: str

    max_input_tokens: int

    max_output_tokens: int

    model: str

    api_model_name: str = FieldInfo(alias="model_name")

    provider: str


AgentListSupportedModelsResponse: TypeAlias = List[AgentListSupportedModelsResponseItem]

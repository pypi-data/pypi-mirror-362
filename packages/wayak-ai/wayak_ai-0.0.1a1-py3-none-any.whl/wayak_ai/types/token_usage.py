# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["TokenUsage"]


class TokenUsage(BaseModel):
    input_token_count: Optional[int] = None

    output_token_count: Optional[int] = None

    raw_provider_cost: Optional[float] = None

    total_token_count: Optional[int] = None

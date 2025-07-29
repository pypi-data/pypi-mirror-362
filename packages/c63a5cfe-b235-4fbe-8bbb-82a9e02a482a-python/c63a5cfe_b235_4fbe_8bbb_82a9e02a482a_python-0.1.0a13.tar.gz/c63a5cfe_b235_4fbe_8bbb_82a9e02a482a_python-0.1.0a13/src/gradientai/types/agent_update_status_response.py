# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

from .._models import BaseModel

__all__ = ["AgentUpdateStatusResponse"]


class AgentUpdateStatusResponse(BaseModel):
    agent: Optional["APIAgent"] = None


from .api_agent import APIAgent

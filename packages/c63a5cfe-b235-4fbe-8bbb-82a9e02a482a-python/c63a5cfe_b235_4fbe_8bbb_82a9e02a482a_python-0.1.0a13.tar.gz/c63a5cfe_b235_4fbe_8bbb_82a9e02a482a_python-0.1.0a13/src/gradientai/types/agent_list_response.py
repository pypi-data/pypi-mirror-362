# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .api_agent_model import APIAgentModel
from .shared.api_meta import APIMeta
from .shared.api_links import APILinks
from .api_knowledge_base import APIKnowledgeBase
from .api_retrieval_method import APIRetrievalMethod
from .api_deployment_visibility import APIDeploymentVisibility

__all__ = [
    "AgentListResponse",
    "Agent",
    "AgentChatbot",
    "AgentChatbotIdentifier",
    "AgentDeployment",
    "AgentTemplate",
    "AgentTemplateGuardrail",
]


class AgentChatbot(BaseModel):
    button_background_color: Optional[str] = None

    logo: Optional[str] = None

    name: Optional[str] = None

    primary_color: Optional[str] = None

    secondary_color: Optional[str] = None

    starting_message: Optional[str] = None


class AgentChatbotIdentifier(BaseModel):
    agent_chatbot_identifier: Optional[str] = None


class AgentDeployment(BaseModel):
    created_at: Optional[datetime] = None

    name: Optional[str] = None

    status: Optional[
        Literal[
            "STATUS_UNKNOWN",
            "STATUS_WAITING_FOR_DEPLOYMENT",
            "STATUS_DEPLOYING",
            "STATUS_RUNNING",
            "STATUS_FAILED",
            "STATUS_WAITING_FOR_UNDEPLOYMENT",
            "STATUS_UNDEPLOYING",
            "STATUS_UNDEPLOYMENT_FAILED",
            "STATUS_DELETED",
        ]
    ] = None

    updated_at: Optional[datetime] = None

    url: Optional[str] = None

    uuid: Optional[str] = None

    visibility: Optional[APIDeploymentVisibility] = None


class AgentTemplateGuardrail(BaseModel):
    priority: Optional[int] = None

    uuid: Optional[str] = None


class AgentTemplate(BaseModel):
    created_at: Optional[datetime] = None

    description: Optional[str] = None

    guardrails: Optional[List[AgentTemplateGuardrail]] = None

    instruction: Optional[str] = None

    k: Optional[int] = None

    knowledge_bases: Optional[List[APIKnowledgeBase]] = None

    long_description: Optional[str] = None

    max_tokens: Optional[int] = None

    model: Optional[APIAgentModel] = None

    name: Optional[str] = None

    short_description: Optional[str] = None

    summary: Optional[str] = None

    tags: Optional[List[str]] = None

    temperature: Optional[float] = None

    template_type: Optional[Literal["AGENT_TEMPLATE_TYPE_STANDARD", "AGENT_TEMPLATE_TYPE_ONE_CLICK"]] = None

    top_p: Optional[float] = None

    updated_at: Optional[datetime] = None

    uuid: Optional[str] = None


class Agent(BaseModel):
    chatbot: Optional[AgentChatbot] = None

    chatbot_identifiers: Optional[List[AgentChatbotIdentifier]] = None

    created_at: Optional[datetime] = None

    deployment: Optional[AgentDeployment] = None

    description: Optional[str] = None

    if_case: Optional[str] = None

    instruction: Optional[str] = None
    """Agent instruction.

    Instructions help your agent to perform its job effectively. See
    [Write Effective Agent Instructions](https://docs.digitalocean.com/products/genai-platform/concepts/best-practices/#agent-instructions)
    for best practices.
    """

    k: Optional[int] = None

    max_tokens: Optional[int] = None
    """
    Specifies the maximum number of tokens the model can process in a single input
    or output, set as a number between 1 and 512. This determines the length of each
    response.
    """

    model: Optional[APIAgentModel] = None

    name: Optional[str] = None

    project_id: Optional[str] = None

    provide_citations: Optional[bool] = None

    region: Optional[str] = None

    retrieval_method: Optional[APIRetrievalMethod] = None

    route_created_at: Optional[datetime] = None

    route_created_by: Optional[str] = None

    route_name: Optional[str] = None

    route_uuid: Optional[str] = None

    tags: Optional[List[str]] = None

    temperature: Optional[float] = None
    """Controls the model’s creativity, specified as a number between 0 and 1.

    Lower values produce more predictable and conservative responses, while higher
    values encourage creativity and variation.
    """

    template: Optional[AgentTemplate] = None

    top_p: Optional[float] = None
    """
    Defines the cumulative probability threshold for word selection, specified as a
    number between 0 and 1. Higher values allow for more diverse outputs, while
    lower values ensure focused and coherent responses.
    """

    updated_at: Optional[datetime] = None

    url: Optional[str] = None

    user_id: Optional[str] = None

    uuid: Optional[str] = None


class AgentListResponse(BaseModel):
    agents: Optional[List[Agent]] = None

    links: Optional[APILinks] = None

    meta: Optional[APIMeta] = None

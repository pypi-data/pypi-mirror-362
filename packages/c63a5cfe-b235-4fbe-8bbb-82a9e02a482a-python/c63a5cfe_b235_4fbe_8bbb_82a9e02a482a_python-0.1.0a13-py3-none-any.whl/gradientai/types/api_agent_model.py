# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .api_agreement import APIAgreement
from .api_model_version import APIModelVersion

__all__ = ["APIAgentModel"]


class APIAgentModel(BaseModel):
    agreement: Optional[APIAgreement] = None

    created_at: Optional[datetime] = None

    inference_name: Optional[str] = None

    inference_version: Optional[str] = None

    is_foundational: Optional[bool] = None

    metadata: Optional[object] = None

    name: Optional[str] = None

    parent_uuid: Optional[str] = None

    provider: Optional[Literal["MODEL_PROVIDER_DIGITALOCEAN", "MODEL_PROVIDER_ANTHROPIC", "MODEL_PROVIDER_OPENAI"]] = (
        None
    )

    updated_at: Optional[datetime] = None

    upload_complete: Optional[bool] = None

    url: Optional[str] = None

    usecases: Optional[
        List[
            Literal[
                "MODEL_USECASE_UNKNOWN",
                "MODEL_USECASE_AGENT",
                "MODEL_USECASE_FINETUNED",
                "MODEL_USECASE_KNOWLEDGEBASE",
                "MODEL_USECASE_GUARDRAIL",
                "MODEL_USECASE_REASONING",
                "MODEL_USECASE_SERVERLESS",
            ]
        ]
    ] = None

    uuid: Optional[str] = None

    version: Optional[APIModelVersion] = None

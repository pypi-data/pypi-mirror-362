# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from ..shared.api_meta import APIMeta
from .api_indexing_job import APIIndexingJob
from ..shared.api_links import APILinks

__all__ = ["IndexingJobListResponse"]


class IndexingJobListResponse(BaseModel):
    jobs: Optional[List[APIIndexingJob]] = None

    links: Optional[APILinks] = None

    meta: Optional[APIMeta] = None

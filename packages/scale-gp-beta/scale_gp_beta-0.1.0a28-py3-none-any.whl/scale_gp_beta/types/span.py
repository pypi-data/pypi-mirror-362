# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import builtins
from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Span"]


class Span(BaseModel):
    id: str

    account_id: str

    created_by_user_id: str

    name: str

    start_timestamp: datetime

    trace_id: str
    """id for grouping traces together, uuid is recommended"""

    application_interaction_id: Optional[str] = None
    """The interaction ID this span belongs to"""

    application_variant_id: Optional[str] = None
    """The id of the application variant this span belongs to"""

    end_timestamp: Optional[datetime] = None

    group_id: Optional[str] = None
    """Reference to a group_id"""

    input: Optional[Dict[str, object]] = None

    metadata: Optional[Dict[str, object]] = None

    object: Optional[Literal["span"]] = None

    output: Optional[Dict[str, builtins.object]] = None

    parent_id: Optional[str] = None
    """Reference to a parent span_id"""

    status: Optional[Literal["SUCCESS", "ERROR", "CANCELED"]] = None

    type: Optional[
        Literal[
            "TEXT_INPUT",
            "TEXT_OUTPUT",
            "COMPLETION_INPUT",
            "COMPLETION",
            "KB_RETRIEVAL",
            "KB_INPUT",
            "RERANKING",
            "EXTERNAL_ENDPOINT",
            "PROMPT_ENGINEERING",
            "DOCUMENT_INPUT",
            "MAP_REDUCE",
            "DOCUMENT_SEARCH",
            "DOCUMENT_PROMPT",
            "CUSTOM",
            "CODE_EXECUTION",
            "DATA_MANIPULATION",
            "EVALUATION",
            "FILE_RETRIEVAL",
            "KB_ADD_CHUNK",
            "KB_MANAGEMENT",
            "GUARDRAIL",
            "TRACER",
            "AGENT_TRACER",
            "AGENT_WORKFLOW",
            "STANDALONE",
        ]
    ] = None

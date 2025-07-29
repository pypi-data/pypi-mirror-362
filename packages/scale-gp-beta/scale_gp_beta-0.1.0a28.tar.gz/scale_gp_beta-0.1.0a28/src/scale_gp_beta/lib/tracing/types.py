"""
This is necessary, unfortunately. Stainless does not provide SpanStatusLiterals and SpanTypeLiterals as enums, only as
type annotations.

For strict linting, we need to reference these enums.

NOTE: These will have to be manually updated to support updated span_types and status.
"""

from typing_extensions import Any, Dict, Literal

SpanInputParam = Dict[str, Any]
SpanOutputParam = Dict[str, Any]
SpanMetadataParam = Dict[str, Any]

SpanStatusLiterals = Literal["SUCCESS", "ERROR", "CANCELED"]

SpanTypeLiterals = Literal[
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
        "TRACER",
        "AGENT_TRACER",
        "AGENT_WORKFLOW",
        "STANDALONE",
]

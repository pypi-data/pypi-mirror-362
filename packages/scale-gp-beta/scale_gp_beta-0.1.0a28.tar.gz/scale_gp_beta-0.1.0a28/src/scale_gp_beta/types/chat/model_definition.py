# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["ModelDefinition"]


class ModelDefinition(BaseModel):
    name: str = FieldInfo(alias="model_name")
    """model name, for example `gpt-4o`"""

    type: Literal["generic", "completion", "chat_completion"] = FieldInfo(alias="model_type")
    """model type, for example `chat_completion`"""

    vendor: Literal[
        "openai",
        "cohere",
        "vertex_ai",
        "anthropic",
        "azure",
        "gemini",
        "launch",
        "llmengine",
        "model_zoo",
        "bedrock",
        "xai",
        "fireworks_ai",
    ] = FieldInfo(alias="model_vendor")
    """model vendor, for example `openai`"""

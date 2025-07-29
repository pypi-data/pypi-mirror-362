# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

__all__ = ["EvaluationUpdateParams"]


class EvaluationUpdateParams(TypedDict, total=False):
    description: str

    name: str

    tags: List[str]
    """The tags associated with the entity"""

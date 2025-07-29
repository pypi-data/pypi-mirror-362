# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .dataset import Dataset
from .._compat import PYDANTIC_V2
from .._models import BaseModel

__all__ = ["Evaluation"]


class Evaluation(BaseModel):
    id: str

    created_at: datetime

    created_by_user_id: str

    datasets: List[Dataset]

    name: str

    status: Literal["failed", "completed", "running"]

    tags: List[str]
    """The tags associated with the entity"""

    archived_at: Optional[datetime] = None

    description: Optional[str] = None

    object: Optional[Literal["evaluation"]] = None

    tasks: Optional[List["EvaluationTask"]] = None
    """Tasks executed during evaluation. Populated with optional `task` view."""


from .evaluation_task import EvaluationTask

if PYDANTIC_V2:
    Evaluation.model_rebuild()
else:
    Evaluation.update_forward_refs()  # type: ignore

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Dataset"]


class Dataset(BaseModel):
    id: str

    created_at: datetime

    created_by_user_id: str

    current_version_num: int

    name: str

    tags: List[str]
    """The tags associated with the entity"""

    archived_at: Optional[datetime] = None

    description: Optional[str] = None

    object: Optional[Literal["dataset"]] = None

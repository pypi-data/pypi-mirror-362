# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "Question",
    "CategoricalQuestion",
    "CategoricalQuestionConfiguration",
    "RatingQuestion",
    "RatingQuestionConfiguration",
    "NumberQuestion",
    "NumberQuestionConfiguration",
    "FreeTextQuestion",
    "FreeTextQuestionConfiguration",
    "FormQuestion",
    "FormQuestionConfiguration",
]


class CategoricalQuestionConfiguration(BaseModel):
    choices: List[str]
    """Categorical answer choices (must contain at least one entry)"""


class CategoricalQuestion(BaseModel):
    id: str
    """Unique identifier of the entity"""

    configuration: CategoricalQuestionConfiguration

    created_at: datetime
    """ISO-timestamp when the entity was created"""

    created_by_user_id: str
    """User who originally created the entity"""

    name: str

    prompt: str
    """user-facing question prompt"""

    object: Optional[Literal["question"]] = None

    question_type: Optional[Literal["categorical"]] = None


class RatingQuestionConfiguration(BaseModel):
    max_label: str
    """Label shown for the maximum rating"""

    min_label: str
    """Label shown for the minimum rating"""

    steps: int
    """Number of discrete points on the scale (e.g., 5 for a 1–5 scale)"""


class RatingQuestion(BaseModel):
    id: str
    """Unique identifier of the entity"""

    configuration: RatingQuestionConfiguration

    created_at: datetime
    """ISO-timestamp when the entity was created"""

    created_by_user_id: str
    """User who originally created the entity"""

    name: str

    prompt: str
    """user-facing question prompt"""

    object: Optional[Literal["question"]] = None

    question_type: Optional[Literal["rating"]] = None


class NumberQuestionConfiguration(BaseModel):
    max: Optional[float] = None
    """Maximum value for the number"""

    min: Optional[float] = None
    """Minimum value for the number"""


class NumberQuestion(BaseModel):
    id: str
    """Unique identifier of the entity"""

    created_at: datetime
    """ISO-timestamp when the entity was created"""

    created_by_user_id: str
    """User who originally created the entity"""

    name: str

    prompt: str
    """user-facing question prompt"""

    configuration: Optional[NumberQuestionConfiguration] = None

    object: Optional[Literal["question"]] = None

    question_type: Optional[Literal["number"]] = None


class FreeTextQuestionConfiguration(BaseModel):
    max_length: Optional[int] = None
    """Maximum characters allowed"""

    min_length: Optional[int] = None
    """Minimum characters required"""


class FreeTextQuestion(BaseModel):
    id: str
    """Unique identifier of the entity"""

    created_at: datetime
    """ISO-timestamp when the entity was created"""

    created_by_user_id: str
    """User who originally created the entity"""

    name: str

    prompt: str
    """user-facing question prompt"""

    configuration: Optional[FreeTextQuestionConfiguration] = None

    object: Optional[Literal["question"]] = None

    question_type: Optional[Literal["free_text"]] = None


class FormQuestionConfiguration(BaseModel):
    form_schema: Dict[str, object]
    """The JSON schema of the desired form object"""


class FormQuestion(BaseModel):
    id: str
    """Unique identifier of the entity"""

    configuration: FormQuestionConfiguration

    created_at: datetime
    """ISO-timestamp when the entity was created"""

    created_by_user_id: str
    """User who originally created the entity"""

    name: str

    prompt: str
    """user-facing question prompt"""

    object: Optional[Literal["question"]] = None

    question_type: Optional[Literal["form"]] = None


Question: TypeAlias = Annotated[
    Union[CategoricalQuestion, RatingQuestion, NumberQuestion, FreeTextQuestion, FormQuestion],
    PropertyInfo(discriminator="question_type"),
]

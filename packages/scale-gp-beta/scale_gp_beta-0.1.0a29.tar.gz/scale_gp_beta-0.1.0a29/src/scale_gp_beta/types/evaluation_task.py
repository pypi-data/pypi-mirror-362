# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._compat import PYDANTIC_V2
from .._models import BaseModel
from .item_locator import ItemLocator

__all__ = [
    "EvaluationTask",
    "ChatCompletionEvaluationTask",
    "ChatCompletionEvaluationTaskConfiguration",
    "GenericInferenceEvaluationTask",
    "GenericInferenceEvaluationTaskConfiguration",
    "GenericInferenceEvaluationTaskConfigurationInferenceConfiguration",
    "GenericInferenceEvaluationTaskConfigurationInferenceConfigurationLaunchInferenceConfiguration",
    "ApplicationVariantV1EvaluationTask",
    "ApplicationVariantV1EvaluationTaskConfiguration",
    "ApplicationVariantV1EvaluationTaskConfigurationHistoryApplicationRequestResponsePairArray",
    "ApplicationVariantV1EvaluationTaskConfigurationOverrides",
    "ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides",
    "ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState",
    "ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace",
    "MetricEvaluationTask",
    "MetricEvaluationTaskConfiguration",
    "MetricEvaluationTaskConfigurationBleuScorerConfigWithItemLocator",
    "MetricEvaluationTaskConfigurationMeteorScorerConfigWithItemLocator",
    "MetricEvaluationTaskConfigurationCosineSimilarityScorerConfigWithItemLocator",
    "MetricEvaluationTaskConfigurationF1ScorerConfigWithItemLocator",
    "MetricEvaluationTaskConfigurationRougeScorer1ConfigWithItemLocator",
    "MetricEvaluationTaskConfigurationRougeScorer2ConfigWithItemLocator",
    "MetricEvaluationTaskConfigurationRougeScorerLConfigWithItemLocator",
    "AutoEvaluationQuestionTask",
    "AutoEvaluationQuestionTaskConfiguration",
    "AutoEvaluationGuidedDecodingEvaluationTask",
    "AutoEvaluationGuidedDecodingEvaluationTaskConfiguration",
    "ContributorEvaluationQuestionTask",
    "ContributorEvaluationQuestionTaskConfiguration",
]


class ChatCompletionEvaluationTaskConfiguration(BaseModel):
    messages: Union[List[Dict[str, object]], ItemLocator]

    model: str

    audio: Union[Dict[str, object], ItemLocator, None] = None

    frequency_penalty: Union[float, ItemLocator, None] = None

    function_call: Union[Dict[str, object], ItemLocator, None] = None

    functions: Union[List[Dict[str, object]], ItemLocator, None] = None

    logit_bias: Union[Dict[str, int], ItemLocator, None] = None

    logprobs: Union[bool, ItemLocator, None] = None

    max_completion_tokens: Union[int, ItemLocator, None] = None

    max_tokens: Union[int, ItemLocator, None] = None

    metadata: Union[Dict[str, str], ItemLocator, None] = None

    modalities: Union[List[str], ItemLocator, None] = None

    n: Union[int, ItemLocator, None] = None

    parallel_tool_calls: Union[bool, ItemLocator, None] = None

    prediction: Union[Dict[str, object], ItemLocator, None] = None

    presence_penalty: Union[float, ItemLocator, None] = None

    reasoning_effort: Optional[str] = None

    response_format: Union[Dict[str, object], ItemLocator, None] = None

    seed: Union[int, ItemLocator, None] = None

    stop: Optional[str] = None

    store: Union[bool, ItemLocator, None] = None

    temperature: Union[float, ItemLocator, None] = None

    tool_choice: Optional[str] = None

    tools: Union[List[Dict[str, object]], ItemLocator, None] = None

    top_k: Union[int, ItemLocator, None] = None

    top_logprobs: Union[int, ItemLocator, None] = None

    top_p: Union[float, ItemLocator, None] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ChatCompletionEvaluationTask(BaseModel):
    configuration: ChatCompletionEvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `chat_completion`"""

    task_type: Optional[Literal["chat_completion"]] = None


class GenericInferenceEvaluationTaskConfigurationInferenceConfigurationLaunchInferenceConfiguration(BaseModel):
    num_retries: Optional[int] = None

    timeout_seconds: Optional[int] = None


GenericInferenceEvaluationTaskConfigurationInferenceConfiguration: TypeAlias = Union[
    GenericInferenceEvaluationTaskConfigurationInferenceConfigurationLaunchInferenceConfiguration, ItemLocator
]


class GenericInferenceEvaluationTaskConfiguration(BaseModel):
    model: str

    args: Union[Dict[str, object], ItemLocator, None] = None

    inference_configuration: Optional[GenericInferenceEvaluationTaskConfigurationInferenceConfiguration] = None


class GenericInferenceEvaluationTask(BaseModel):
    configuration: GenericInferenceEvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `inference`"""

    task_type: Optional[Literal["inference"]] = None


class ApplicationVariantV1EvaluationTaskConfigurationHistoryApplicationRequestResponsePairArray(BaseModel):
    request: str
    """Request inputs"""

    response: str
    """Response outputs"""

    session_data: Optional[Dict[str, object]] = None
    """Session data corresponding to the request response pair"""


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState(BaseModel):
    current_node: str

    state: Dict[str, object]


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace(BaseModel):
    duration_ms: int

    node_id: str

    operation_input: str

    operation_output: str

    operation_type: str

    start_timestamp: str

    workflow_id: str

    operation_metadata: Optional[Dict[str, object]] = None


class ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides(BaseModel):
    concurrent: Optional[bool] = None

    initial_state: Optional[
        ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState
    ] = None

    partial_trace: Optional[
        List[ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace]
    ] = None

    return_span: Optional[bool] = None

    use_channels: Optional[bool] = None


ApplicationVariantV1EvaluationTaskConfigurationOverrides: TypeAlias = Union[
    ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides, ItemLocator
]


class ApplicationVariantV1EvaluationTaskConfiguration(BaseModel):
    application_variant_id: str

    inputs: Union[Dict[str, object], ItemLocator]

    history: Union[
        List[ApplicationVariantV1EvaluationTaskConfigurationHistoryApplicationRequestResponsePairArray],
        ItemLocator,
        None,
    ] = None

    operation_metadata: Union[Dict[str, object], ItemLocator, None] = None

    overrides: Optional[ApplicationVariantV1EvaluationTaskConfigurationOverrides] = None
    """Execution override options for agentic applications"""


class ApplicationVariantV1EvaluationTask(BaseModel):
    configuration: ApplicationVariantV1EvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `application_variant`"""

    task_type: Optional[Literal["application_variant"]] = None


class MetricEvaluationTaskConfigurationBleuScorerConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["bleu"]


class MetricEvaluationTaskConfigurationMeteorScorerConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["meteor"]


class MetricEvaluationTaskConfigurationCosineSimilarityScorerConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["cosine_similarity"]


class MetricEvaluationTaskConfigurationF1ScorerConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["f1"]


class MetricEvaluationTaskConfigurationRougeScorer1ConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["rouge1"]


class MetricEvaluationTaskConfigurationRougeScorer2ConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["rouge2"]


class MetricEvaluationTaskConfigurationRougeScorerLConfigWithItemLocator(BaseModel):
    candidate: str

    reference: str

    type: Literal["rougeL"]


MetricEvaluationTaskConfiguration: TypeAlias = Annotated[
    Union[
        MetricEvaluationTaskConfigurationBleuScorerConfigWithItemLocator,
        MetricEvaluationTaskConfigurationMeteorScorerConfigWithItemLocator,
        MetricEvaluationTaskConfigurationCosineSimilarityScorerConfigWithItemLocator,
        MetricEvaluationTaskConfigurationF1ScorerConfigWithItemLocator,
        MetricEvaluationTaskConfigurationRougeScorer1ConfigWithItemLocator,
        MetricEvaluationTaskConfigurationRougeScorer2ConfigWithItemLocator,
        MetricEvaluationTaskConfigurationRougeScorerLConfigWithItemLocator,
    ],
    PropertyInfo(discriminator="type"),
]


class MetricEvaluationTask(BaseModel):
    configuration: MetricEvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column.

    Defaults to the metric type specified in the configuration
    """

    task_type: Optional[Literal["metric"]] = None


class AutoEvaluationQuestionTaskConfiguration(BaseModel):
    model: str
    """model specified as `model_vendor/model_name`"""

    prompt: str

    question_id: str
    """question to be evaluated"""


class AutoEvaluationQuestionTask(BaseModel):
    configuration: AutoEvaluationQuestionTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column. Defaults to the `auto_evaluation_question`"""

    task_type: Optional[Literal["auto_evaluation.question"]] = None


class AutoEvaluationGuidedDecodingEvaluationTaskConfiguration(BaseModel):
    choices: List[str]
    """Choices array cannot be empty"""

    model: str
    """model specified as `model_vendor/model_name`"""

    prompt: str

    inference_args: Optional[Dict[str, object]] = None
    """Additional arguments to pass to the inference request"""

    system_prompt: Optional[str] = None


class AutoEvaluationGuidedDecodingEvaluationTask(BaseModel):
    configuration: AutoEvaluationGuidedDecodingEvaluationTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column.

    Defaults to the `auto_evaluation_guided_decoding`
    """

    task_type: Optional[Literal["auto_evaluation.guided_decoding"]] = None


class ContributorEvaluationQuestionTaskConfiguration(BaseModel):
    layout: "Container"

    question_id: str

    queue_id: Optional[str] = None
    """The contributor annotation queue to include this task in. Defaults to `default`"""


class ContributorEvaluationQuestionTask(BaseModel):
    configuration: ContributorEvaluationQuestionTaskConfiguration

    alias: Optional[str] = None
    """Alias to title the results column.

    Defaults to the `contributor_evaluation_question`
    """

    task_type: Optional[Literal["contributor_evaluation.question"]] = None


EvaluationTask: TypeAlias = Annotated[
    Union[
        ChatCompletionEvaluationTask,
        GenericInferenceEvaluationTask,
        ApplicationVariantV1EvaluationTask,
        MetricEvaluationTask,
        AutoEvaluationQuestionTask,
        AutoEvaluationGuidedDecodingEvaluationTask,
        ContributorEvaluationQuestionTask,
    ],
    PropertyInfo(discriminator="task_type"),
]

from .container import Container

if PYDANTIC_V2:
    ChatCompletionEvaluationTask.model_rebuild()
    ChatCompletionEvaluationTaskConfiguration.model_rebuild()
    GenericInferenceEvaluationTask.model_rebuild()
    GenericInferenceEvaluationTaskConfiguration.model_rebuild()
    GenericInferenceEvaluationTaskConfigurationInferenceConfigurationLaunchInferenceConfiguration.model_rebuild()
    ApplicationVariantV1EvaluationTask.model_rebuild()
    ApplicationVariantV1EvaluationTaskConfiguration.model_rebuild()
    ApplicationVariantV1EvaluationTaskConfigurationHistoryApplicationRequestResponsePairArray.model_rebuild()
    ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides.model_rebuild()
    ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState.model_rebuild()
    ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace.model_rebuild()
    MetricEvaluationTask.model_rebuild()
    MetricEvaluationTaskConfigurationBleuScorerConfigWithItemLocator.model_rebuild()
    MetricEvaluationTaskConfigurationMeteorScorerConfigWithItemLocator.model_rebuild()
    MetricEvaluationTaskConfigurationCosineSimilarityScorerConfigWithItemLocator.model_rebuild()
    MetricEvaluationTaskConfigurationF1ScorerConfigWithItemLocator.model_rebuild()
    MetricEvaluationTaskConfigurationRougeScorer1ConfigWithItemLocator.model_rebuild()
    MetricEvaluationTaskConfigurationRougeScorer2ConfigWithItemLocator.model_rebuild()
    MetricEvaluationTaskConfigurationRougeScorerLConfigWithItemLocator.model_rebuild()
    AutoEvaluationQuestionTask.model_rebuild()
    AutoEvaluationQuestionTaskConfiguration.model_rebuild()
    AutoEvaluationGuidedDecodingEvaluationTask.model_rebuild()
    AutoEvaluationGuidedDecodingEvaluationTaskConfiguration.model_rebuild()
    ContributorEvaluationQuestionTask.model_rebuild()
    ContributorEvaluationQuestionTaskConfiguration.model_rebuild()
else:
    ChatCompletionEvaluationTask.update_forward_refs()  # type: ignore
    ChatCompletionEvaluationTaskConfiguration.update_forward_refs()  # type: ignore
    GenericInferenceEvaluationTask.update_forward_refs()  # type: ignore
    GenericInferenceEvaluationTaskConfiguration.update_forward_refs()  # type: ignore
    GenericInferenceEvaluationTaskConfigurationInferenceConfigurationLaunchInferenceConfiguration.update_forward_refs()  # type: ignore
    ApplicationVariantV1EvaluationTask.update_forward_refs()  # type: ignore
    ApplicationVariantV1EvaluationTaskConfiguration.update_forward_refs()  # type: ignore
    ApplicationVariantV1EvaluationTaskConfigurationHistoryApplicationRequestResponsePairArray.update_forward_refs()  # type: ignore
    ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverrides.update_forward_refs()  # type: ignore
    ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesInitialState.update_forward_refs()  # type: ignore
    ApplicationVariantV1EvaluationTaskConfigurationOverridesAgenticApplicationOverridesPartialTrace.update_forward_refs()  # type: ignore
    MetricEvaluationTask.update_forward_refs()  # type: ignore
    MetricEvaluationTaskConfigurationBleuScorerConfigWithItemLocator.update_forward_refs()  # type: ignore
    MetricEvaluationTaskConfigurationMeteorScorerConfigWithItemLocator.update_forward_refs()  # type: ignore
    MetricEvaluationTaskConfigurationCosineSimilarityScorerConfigWithItemLocator.update_forward_refs()  # type: ignore
    MetricEvaluationTaskConfigurationF1ScorerConfigWithItemLocator.update_forward_refs()  # type: ignore
    MetricEvaluationTaskConfigurationRougeScorer1ConfigWithItemLocator.update_forward_refs()  # type: ignore
    MetricEvaluationTaskConfigurationRougeScorer2ConfigWithItemLocator.update_forward_refs()  # type: ignore
    MetricEvaluationTaskConfigurationRougeScorerLConfigWithItemLocator.update_forward_refs()  # type: ignore
    AutoEvaluationQuestionTask.update_forward_refs()  # type: ignore
    AutoEvaluationQuestionTaskConfiguration.update_forward_refs()  # type: ignore
    AutoEvaluationGuidedDecodingEvaluationTask.update_forward_refs()  # type: ignore
    AutoEvaluationGuidedDecodingEvaluationTaskConfiguration.update_forward_refs()  # type: ignore
    ContributorEvaluationQuestionTask.update_forward_refs()  # type: ignore
    ContributorEvaluationQuestionTaskConfiguration.update_forward_refs()  # type: ignore

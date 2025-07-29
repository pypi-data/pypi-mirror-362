# Completions

Types:

```python
from scale_gp_beta.types import Completion
```

Methods:

- <code title="post /v5/completions">client.completions.<a href="./src/scale_gp_beta/resources/completions.py">create</a>(\*\*<a href="src/scale_gp_beta/types/completion_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/completion.py">Completion</a></code>

# Chat

## Completions

Types:

```python
from scale_gp_beta.types.chat import (
    ChatCompletion,
    ChatCompletionChunk,
    ModelDefinition,
    CompletionCreateResponse,
    CompletionModelsResponse,
)
```

Methods:

- <code title="post /v5/chat/completions">client.chat.completions.<a href="./src/scale_gp_beta/resources/chat/completions.py">create</a>(\*\*<a href="src/scale_gp_beta/types/chat/completion_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/chat/completion_create_response.py">CompletionCreateResponse</a></code>
- <code title="get /v5/chat/completions/models">client.chat.completions.<a href="./src/scale_gp_beta/resources/chat/completions.py">models</a>(\*\*<a href="src/scale_gp_beta/types/chat/completion_models_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/chat/completion_models_response.py">CompletionModelsResponse</a></code>

# Inference

Types:

```python
from scale_gp_beta.types import InferenceResponse, InferenceResponseChunk, InferenceCreateResponse
```

Methods:

- <code title="post /v5/inference">client.inference.<a href="./src/scale_gp_beta/resources/inference.py">create</a>(\*\*<a href="src/scale_gp_beta/types/inference_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/inference_create_response.py">InferenceCreateResponse</a></code>

# Questions

Types:

```python
from scale_gp_beta.types import Question, QuestionList
```

Methods:

- <code title="post /v5/questions">client.questions.<a href="./src/scale_gp_beta/resources/questions.py">create</a>(\*\*<a href="src/scale_gp_beta/types/question_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/question.py">Question</a></code>
- <code title="get /v5/questions/{question_id}">client.questions.<a href="./src/scale_gp_beta/resources/questions.py">retrieve</a>(question_id) -> <a href="./src/scale_gp_beta/types/question.py">Question</a></code>
- <code title="get /v5/questions">client.questions.<a href="./src/scale_gp_beta/resources/questions.py">list</a>(\*\*<a href="src/scale_gp_beta/types/question_list_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/question.py">SyncCursorPage[Question]</a></code>

# Files

Types:

```python
from scale_gp_beta.types import File, FileList, FileDeleteResponse
```

Methods:

- <code title="post /v5/files">client.files.<a href="./src/scale_gp_beta/resources/files/files.py">create</a>(\*\*<a href="src/scale_gp_beta/types/file_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/file.py">File</a></code>
- <code title="get /v5/files/{file_id}">client.files.<a href="./src/scale_gp_beta/resources/files/files.py">retrieve</a>(file_id) -> <a href="./src/scale_gp_beta/types/file.py">File</a></code>
- <code title="patch /v5/files/{file_id}">client.files.<a href="./src/scale_gp_beta/resources/files/files.py">update</a>(file_id, \*\*<a href="src/scale_gp_beta/types/file_update_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/file.py">File</a></code>
- <code title="get /v5/files">client.files.<a href="./src/scale_gp_beta/resources/files/files.py">list</a>(\*\*<a href="src/scale_gp_beta/types/file_list_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/file.py">SyncCursorPage[File]</a></code>
- <code title="delete /v5/files/{file_id}">client.files.<a href="./src/scale_gp_beta/resources/files/files.py">delete</a>(file_id) -> <a href="./src/scale_gp_beta/types/file_delete_response.py">FileDeleteResponse</a></code>

## Content

Methods:

- <code title="get /v5/files/{file_id}/content">client.files.content.<a href="./src/scale_gp_beta/resources/files/content.py">retrieve</a>(file_id) -> object</code>

# Models

Types:

```python
from scale_gp_beta.types import InferenceModel, InferenceModelList, ModelDeleteResponse
```

Methods:

- <code title="post /v5/models">client.models.<a href="./src/scale_gp_beta/resources/models.py">create</a>(\*\*<a href="src/scale_gp_beta/types/model_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/inference_model.py">InferenceModel</a></code>
- <code title="get /v5/models/{model_id}">client.models.<a href="./src/scale_gp_beta/resources/models.py">retrieve</a>(model_id) -> <a href="./src/scale_gp_beta/types/inference_model.py">InferenceModel</a></code>
- <code title="patch /v5/models/{model_id}">client.models.<a href="./src/scale_gp_beta/resources/models.py">update</a>(model_id, \*\*<a href="src/scale_gp_beta/types/model_update_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/inference_model.py">InferenceModel</a></code>
- <code title="get /v5/models">client.models.<a href="./src/scale_gp_beta/resources/models.py">list</a>(\*\*<a href="src/scale_gp_beta/types/model_list_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/inference_model.py">SyncCursorPage[InferenceModel]</a></code>
- <code title="delete /v5/models/{model_id}">client.models.<a href="./src/scale_gp_beta/resources/models.py">delete</a>(model_id) -> <a href="./src/scale_gp_beta/types/model_delete_response.py">ModelDeleteResponse</a></code>

# Datasets

Types:

```python
from scale_gp_beta.types import Dataset, DatasetDeleteResponse
```

Methods:

- <code title="post /v5/datasets">client.datasets.<a href="./src/scale_gp_beta/resources/datasets.py">create</a>(\*\*<a href="src/scale_gp_beta/types/dataset_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/dataset.py">Dataset</a></code>
- <code title="get /v5/datasets/{dataset_id}">client.datasets.<a href="./src/scale_gp_beta/resources/datasets.py">retrieve</a>(dataset_id, \*\*<a href="src/scale_gp_beta/types/dataset_retrieve_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/dataset.py">Dataset</a></code>
- <code title="patch /v5/datasets/{dataset_id}">client.datasets.<a href="./src/scale_gp_beta/resources/datasets.py">update</a>(dataset_id, \*\*<a href="src/scale_gp_beta/types/dataset_update_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/dataset.py">Dataset</a></code>
- <code title="get /v5/datasets">client.datasets.<a href="./src/scale_gp_beta/resources/datasets.py">list</a>(\*\*<a href="src/scale_gp_beta/types/dataset_list_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/dataset.py">SyncCursorPage[Dataset]</a></code>
- <code title="delete /v5/datasets/{dataset_id}">client.datasets.<a href="./src/scale_gp_beta/resources/datasets.py">delete</a>(dataset_id) -> <a href="./src/scale_gp_beta/types/dataset_delete_response.py">DatasetDeleteResponse</a></code>

# Evaluations

Types:

```python
from scale_gp_beta.types import (
    Evaluation,
    EvaluationTask,
    ItemLocator,
    ItemLocatorTemplate,
    EvaluationDeleteResponse,
)
```

Methods:

- <code title="post /v5/evaluations">client.evaluations.<a href="./src/scale_gp_beta/resources/evaluations.py">create</a>(\*\*<a href="src/scale_gp_beta/types/evaluation_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/evaluation.py">Evaluation</a></code>
- <code title="get /v5/evaluations/{evaluation_id}">client.evaluations.<a href="./src/scale_gp_beta/resources/evaluations.py">retrieve</a>(evaluation_id, \*\*<a href="src/scale_gp_beta/types/evaluation_retrieve_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/evaluation.py">Evaluation</a></code>
- <code title="patch /v5/evaluations/{evaluation_id}">client.evaluations.<a href="./src/scale_gp_beta/resources/evaluations.py">update</a>(evaluation_id, \*\*<a href="src/scale_gp_beta/types/evaluation_update_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/evaluation.py">Evaluation</a></code>
- <code title="get /v5/evaluations">client.evaluations.<a href="./src/scale_gp_beta/resources/evaluations.py">list</a>(\*\*<a href="src/scale_gp_beta/types/evaluation_list_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/evaluation.py">SyncCursorPage[Evaluation]</a></code>
- <code title="delete /v5/evaluations/{evaluation_id}">client.evaluations.<a href="./src/scale_gp_beta/resources/evaluations.py">delete</a>(evaluation_id) -> <a href="./src/scale_gp_beta/types/evaluation_delete_response.py">EvaluationDeleteResponse</a></code>

# DatasetItems

Types:

```python
from scale_gp_beta.types import (
    DatasetItem,
    DatasetItemDeleteResponse,
    DatasetItemBatchCreateResponse,
)
```

Methods:

- <code title="get /v5/dataset-items/{dataset_item_id}">client.dataset_items.<a href="./src/scale_gp_beta/resources/dataset_items.py">retrieve</a>(dataset_item_id, \*\*<a href="src/scale_gp_beta/types/dataset_item_retrieve_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/dataset_item.py">DatasetItem</a></code>
- <code title="patch /v5/dataset-items/{dataset_item_id}">client.dataset_items.<a href="./src/scale_gp_beta/resources/dataset_items.py">update</a>(dataset_item_id, \*\*<a href="src/scale_gp_beta/types/dataset_item_update_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/dataset_item.py">DatasetItem</a></code>
- <code title="get /v5/dataset-items">client.dataset_items.<a href="./src/scale_gp_beta/resources/dataset_items.py">list</a>(\*\*<a href="src/scale_gp_beta/types/dataset_item_list_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/dataset_item.py">SyncCursorPage[DatasetItem]</a></code>
- <code title="delete /v5/dataset-items/{dataset_item_id}">client.dataset_items.<a href="./src/scale_gp_beta/resources/dataset_items.py">delete</a>(dataset_item_id) -> <a href="./src/scale_gp_beta/types/dataset_item_delete_response.py">DatasetItemDeleteResponse</a></code>
- <code title="post /v5/dataset-items/batch">client.dataset_items.<a href="./src/scale_gp_beta/resources/dataset_items.py">batch_create</a>(\*\*<a href="src/scale_gp_beta/types/dataset_item_batch_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/dataset_item_batch_create_response.py">DatasetItemBatchCreateResponse</a></code>

# EvaluationItems

Types:

```python
from scale_gp_beta.types import Component, Container, EvaluationItem
```

Methods:

- <code title="get /v5/evaluation-items/{evaluation_item_id}">client.evaluation_items.<a href="./src/scale_gp_beta/resources/evaluation_items.py">retrieve</a>(evaluation_item_id, \*\*<a href="src/scale_gp_beta/types/evaluation_item_retrieve_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/evaluation_item.py">EvaluationItem</a></code>
- <code title="get /v5/evaluation-items">client.evaluation_items.<a href="./src/scale_gp_beta/resources/evaluation_items.py">list</a>(\*\*<a href="src/scale_gp_beta/types/evaluation_item_list_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/evaluation_item.py">SyncCursorPage[EvaluationItem]</a></code>

# Spans

Types:

```python
from scale_gp_beta.types import Span, SpanBatchResponse, SpanUpsertBatchResponse
```

Methods:

- <code title="post /v5/spans">client.spans.<a href="./src/scale_gp_beta/resources/spans.py">create</a>(\*\*<a href="src/scale_gp_beta/types/span_create_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/span.py">Span</a></code>
- <code title="get /v5/spans/{span_id}">client.spans.<a href="./src/scale_gp_beta/resources/spans.py">retrieve</a>(span_id) -> <a href="./src/scale_gp_beta/types/span.py">Span</a></code>
- <code title="patch /v5/spans/{span_id}">client.spans.<a href="./src/scale_gp_beta/resources/spans.py">update</a>(span_id, \*\*<a href="src/scale_gp_beta/types/span_update_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/span.py">Span</a></code>
- <code title="post /v5/spans/batch">client.spans.<a href="./src/scale_gp_beta/resources/spans.py">batch</a>(\*\*<a href="src/scale_gp_beta/types/span_batch_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/span_batch_response.py">SpanBatchResponse</a></code>
- <code title="post /v5/spans/search">client.spans.<a href="./src/scale_gp_beta/resources/spans.py">search</a>(\*\*<a href="src/scale_gp_beta/types/span_search_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/span.py">SyncCursorPage[Span]</a></code>
- <code title="put /v5/spans/batch">client.spans.<a href="./src/scale_gp_beta/resources/spans.py">upsert_batch</a>(\*\*<a href="src/scale_gp_beta/types/span_upsert_batch_params.py">params</a>) -> <a href="./src/scale_gp_beta/types/span_upsert_batch_response.py">SpanUpsertBatchResponse</a></code>

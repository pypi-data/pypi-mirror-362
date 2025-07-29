# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Dict, Union, Mapping, cast
from typing_extensions import Self, Literal, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import (
    spans,
    models,
    datasets,
    inference,
    questions,
    completions,
    evaluations,
    dataset_items,
    evaluation_items,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError, SGPClientError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.chat import chat
from .resources.files import files

__all__ = [
    "ENVIRONMENTS",
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "SGPClient",
    "AsyncSGPClient",
    "Client",
    "AsyncClient",
]

ENVIRONMENTS: Dict[str, str] = {
    "production": "https://api.egp.scale.com",
    "development": "http://127.0.0.1:5003/public",
}


class SGPClient(SyncAPIClient):
    completions: completions.CompletionsResource
    chat: chat.ChatResource
    inference: inference.InferenceResource
    questions: questions.QuestionsResource
    files: files.FilesResource
    models: models.ModelsResource
    datasets: datasets.DatasetsResource
    evaluations: evaluations.EvaluationsResource
    dataset_items: dataset_items.DatasetItemsResource
    evaluation_items: evaluation_items.EvaluationItemsResource
    spans: spans.SpansResource
    with_raw_response: SGPClientWithRawResponse
    with_streaming_response: SGPClientWithStreamedResponse

    # client options
    api_key: str
    account_id: str

    _environment: Literal["production", "development"] | NotGiven

    def __init__(
        self,
        *,
        api_key: str | None = None,
        account_id: str | None = None,
        environment: Literal["production", "development"] | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous SGPClient client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `SGP_API_KEY`
        - `account_id` from `SGP_ACCOUNT_ID`
        """
        if api_key is None:
            api_key = os.environ.get("SGP_API_KEY")
        if api_key is None:
            raise SGPClientError(
                "The api_key client option must be set either by passing api_key to the client or by setting the SGP_API_KEY environment variable"
            )
        self.api_key = api_key

        if account_id is None:
            account_id = os.environ.get("SGP_ACCOUNT_ID")
        if account_id is None:
            raise SGPClientError(
                "The account_id client option must be set either by passing account_id to the client or by setting the SGP_ACCOUNT_ID environment variable"
            )
        self.account_id = account_id

        self._environment = environment

        base_url_env = os.environ.get("SGP_CLIENT_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `SGP_CLIENT_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.completions = completions.CompletionsResource(self)
        self.chat = chat.ChatResource(self)
        self.inference = inference.InferenceResource(self)
        self.questions = questions.QuestionsResource(self)
        self.files = files.FilesResource(self)
        self.models = models.ModelsResource(self)
        self.datasets = datasets.DatasetsResource(self)
        self.evaluations = evaluations.EvaluationsResource(self)
        self.dataset_items = dataset_items.DatasetItemsResource(self)
        self.evaluation_items = evaluation_items.EvaluationItemsResource(self)
        self.spans = spans.SpansResource(self)
        self.with_raw_response = SGPClientWithRawResponse(self)
        self.with_streaming_response = SGPClientWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"x-api-key": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            "x-selected-account-id": self.account_id,
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        account_id: str | None = None,
        environment: Literal["production", "development"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            account_id=account_id or self.account_id,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncSGPClient(AsyncAPIClient):
    completions: completions.AsyncCompletionsResource
    chat: chat.AsyncChatResource
    inference: inference.AsyncInferenceResource
    questions: questions.AsyncQuestionsResource
    files: files.AsyncFilesResource
    models: models.AsyncModelsResource
    datasets: datasets.AsyncDatasetsResource
    evaluations: evaluations.AsyncEvaluationsResource
    dataset_items: dataset_items.AsyncDatasetItemsResource
    evaluation_items: evaluation_items.AsyncEvaluationItemsResource
    spans: spans.AsyncSpansResource
    with_raw_response: AsyncSGPClientWithRawResponse
    with_streaming_response: AsyncSGPClientWithStreamedResponse

    # client options
    api_key: str
    account_id: str

    _environment: Literal["production", "development"] | NotGiven

    def __init__(
        self,
        *,
        api_key: str | None = None,
        account_id: str | None = None,
        environment: Literal["production", "development"] | NotGiven = NOT_GIVEN,
        base_url: str | httpx.URL | None | NotGiven = NOT_GIVEN,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncSGPClient client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `SGP_API_KEY`
        - `account_id` from `SGP_ACCOUNT_ID`
        """
        if api_key is None:
            api_key = os.environ.get("SGP_API_KEY")
        if api_key is None:
            raise SGPClientError(
                "The api_key client option must be set either by passing api_key to the client or by setting the SGP_API_KEY environment variable"
            )
        self.api_key = api_key

        if account_id is None:
            account_id = os.environ.get("SGP_ACCOUNT_ID")
        if account_id is None:
            raise SGPClientError(
                "The account_id client option must be set either by passing account_id to the client or by setting the SGP_ACCOUNT_ID environment variable"
            )
        self.account_id = account_id

        self._environment = environment

        base_url_env = os.environ.get("SGP_CLIENT_BASE_URL")
        if is_given(base_url) and base_url is not None:
            # cast required because mypy doesn't understand the type narrowing
            base_url = cast("str | httpx.URL", base_url)  # pyright: ignore[reportUnnecessaryCast]
        elif is_given(environment):
            if base_url_env and base_url is not None:
                raise ValueError(
                    "Ambiguous URL; The `SGP_CLIENT_BASE_URL` env var and the `environment` argument are given. If you want to use the environment, you must pass base_url=None",
                )

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc
        elif base_url_env is not None:
            base_url = base_url_env
        else:
            self._environment = environment = "production"

            try:
                base_url = ENVIRONMENTS[environment]
            except KeyError as exc:
                raise ValueError(f"Unknown environment: {environment}") from exc

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.completions = completions.AsyncCompletionsResource(self)
        self.chat = chat.AsyncChatResource(self)
        self.inference = inference.AsyncInferenceResource(self)
        self.questions = questions.AsyncQuestionsResource(self)
        self.files = files.AsyncFilesResource(self)
        self.models = models.AsyncModelsResource(self)
        self.datasets = datasets.AsyncDatasetsResource(self)
        self.evaluations = evaluations.AsyncEvaluationsResource(self)
        self.dataset_items = dataset_items.AsyncDatasetItemsResource(self)
        self.evaluation_items = evaluation_items.AsyncEvaluationItemsResource(self)
        self.spans = spans.AsyncSpansResource(self)
        self.with_raw_response = AsyncSGPClientWithRawResponse(self)
        self.with_streaming_response = AsyncSGPClientWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"x-api-key": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            "x-selected-account-id": self.account_id,
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        account_id: str | None = None,
        environment: Literal["production", "development"] | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            account_id=account_id or self.account_id,
            base_url=base_url or self.base_url,
            environment=environment or self._environment,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class SGPClientWithRawResponse:
    def __init__(self, client: SGPClient) -> None:
        self.completions = completions.CompletionsResourceWithRawResponse(client.completions)
        self.chat = chat.ChatResourceWithRawResponse(client.chat)
        self.inference = inference.InferenceResourceWithRawResponse(client.inference)
        self.questions = questions.QuestionsResourceWithRawResponse(client.questions)
        self.files = files.FilesResourceWithRawResponse(client.files)
        self.models = models.ModelsResourceWithRawResponse(client.models)
        self.datasets = datasets.DatasetsResourceWithRawResponse(client.datasets)
        self.evaluations = evaluations.EvaluationsResourceWithRawResponse(client.evaluations)
        self.dataset_items = dataset_items.DatasetItemsResourceWithRawResponse(client.dataset_items)
        self.evaluation_items = evaluation_items.EvaluationItemsResourceWithRawResponse(client.evaluation_items)
        self.spans = spans.SpansResourceWithRawResponse(client.spans)


class AsyncSGPClientWithRawResponse:
    def __init__(self, client: AsyncSGPClient) -> None:
        self.completions = completions.AsyncCompletionsResourceWithRawResponse(client.completions)
        self.chat = chat.AsyncChatResourceWithRawResponse(client.chat)
        self.inference = inference.AsyncInferenceResourceWithRawResponse(client.inference)
        self.questions = questions.AsyncQuestionsResourceWithRawResponse(client.questions)
        self.files = files.AsyncFilesResourceWithRawResponse(client.files)
        self.models = models.AsyncModelsResourceWithRawResponse(client.models)
        self.datasets = datasets.AsyncDatasetsResourceWithRawResponse(client.datasets)
        self.evaluations = evaluations.AsyncEvaluationsResourceWithRawResponse(client.evaluations)
        self.dataset_items = dataset_items.AsyncDatasetItemsResourceWithRawResponse(client.dataset_items)
        self.evaluation_items = evaluation_items.AsyncEvaluationItemsResourceWithRawResponse(client.evaluation_items)
        self.spans = spans.AsyncSpansResourceWithRawResponse(client.spans)


class SGPClientWithStreamedResponse:
    def __init__(self, client: SGPClient) -> None:
        self.completions = completions.CompletionsResourceWithStreamingResponse(client.completions)
        self.chat = chat.ChatResourceWithStreamingResponse(client.chat)
        self.inference = inference.InferenceResourceWithStreamingResponse(client.inference)
        self.questions = questions.QuestionsResourceWithStreamingResponse(client.questions)
        self.files = files.FilesResourceWithStreamingResponse(client.files)
        self.models = models.ModelsResourceWithStreamingResponse(client.models)
        self.datasets = datasets.DatasetsResourceWithStreamingResponse(client.datasets)
        self.evaluations = evaluations.EvaluationsResourceWithStreamingResponse(client.evaluations)
        self.dataset_items = dataset_items.DatasetItemsResourceWithStreamingResponse(client.dataset_items)
        self.evaluation_items = evaluation_items.EvaluationItemsResourceWithStreamingResponse(client.evaluation_items)
        self.spans = spans.SpansResourceWithStreamingResponse(client.spans)


class AsyncSGPClientWithStreamedResponse:
    def __init__(self, client: AsyncSGPClient) -> None:
        self.completions = completions.AsyncCompletionsResourceWithStreamingResponse(client.completions)
        self.chat = chat.AsyncChatResourceWithStreamingResponse(client.chat)
        self.inference = inference.AsyncInferenceResourceWithStreamingResponse(client.inference)
        self.questions = questions.AsyncQuestionsResourceWithStreamingResponse(client.questions)
        self.files = files.AsyncFilesResourceWithStreamingResponse(client.files)
        self.models = models.AsyncModelsResourceWithStreamingResponse(client.models)
        self.datasets = datasets.AsyncDatasetsResourceWithStreamingResponse(client.datasets)
        self.evaluations = evaluations.AsyncEvaluationsResourceWithStreamingResponse(client.evaluations)
        self.dataset_items = dataset_items.AsyncDatasetItemsResourceWithStreamingResponse(client.dataset_items)
        self.evaluation_items = evaluation_items.AsyncEvaluationItemsResourceWithStreamingResponse(
            client.evaluation_items
        )
        self.spans = spans.AsyncSpansResourceWithStreamingResponse(client.spans)


Client = SGPClient

AsyncClient = AsyncSGPClient

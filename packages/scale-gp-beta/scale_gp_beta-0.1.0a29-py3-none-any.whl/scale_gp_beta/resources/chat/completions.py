# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, List, Union, Iterable, cast
from typing_extensions import Literal, overload

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import required_args, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._streaming import Stream, AsyncStream
from ...types.chat import completion_create_params, completion_models_params
from ..._base_client import make_request_options
from ...types.chat.chat_completion_chunk import ChatCompletionChunk
from ...types.chat.completion_create_response import CompletionCreateResponse
from ...types.chat.completion_models_response import CompletionModelsResponse

__all__ = ["CompletionsResource", "AsyncCompletionsResource"]


class CompletionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CompletionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return CompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompletionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return CompletionsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        messages: Iterable[Dict[str, object]],
        model: str,
        audio: Dict[str, object] | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        function_call: Dict[str, object] | NotGiven = NOT_GIVEN,
        functions: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        modalities: List[str] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: Dict[str, object] | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        reasoning_effort: str | NotGiven = NOT_GIVEN,
        response_format: Dict[str, object] | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        store: bool | NotGiven = NOT_GIVEN,
        stream: Literal[False] | NotGiven = NOT_GIVEN,
        stream_options: Dict[str, object] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, Dict[str, object]] | NotGiven = NOT_GIVEN,
        tools: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionCreateResponse:
        """
        Chat Completions

        Args:
          messages: openai standard message format

          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          audio: Parameters for audio output. Required when audio output is requested with
              modalities: ['audio'].

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far.

          function_call: Deprecated in favor of tool_choice. Controls which function is called by the
              model.

          functions: Deprecated in favor of tools. A list of functions the model may generate JSON
              inputs for.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Maps
              tokens to bias values from -100 to 100.

          logprobs: Whether to return log probabilities of the output tokens or not.

          max_completion_tokens: An upper bound for the number of tokens that can be generated, including visible
              output tokens and reasoning tokens.

          max_tokens: Deprecated in favor of max_completion_tokens. The maximum number of tokens to
              generate.

          metadata: Developer-defined tags and values used for filtering completions in the
              dashboard.

          modalities: Output types that you would like the model to generate for this request.

          n: How many chat completion choices to generate for each input message.

          parallel_tool_calls: Whether to enable parallel function calling during tool use.

          prediction: Static predicted output content, such as the content of a text file being
              regenerated.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize tokens based on whether
              they appear in the text so far.

          reasoning_effort: For o1 models only. Constrains effort on reasoning. Values: low, medium, high.

          response_format: An object specifying the format that the model must output.

          seed: If specified, system will attempt to sample deterministically for repeated
              requests with same seed.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          store: Whether to store the output for use in model distillation or evals products.

          stream: If true, partial message deltas will be sent as server-sent events.

          stream_options: Options for streaming response. Only set this when stream is true.

          temperature: What sampling temperature to use. Higher values make output more random, lower
              more focused.

          tool_choice: Controls which tool is called by the model. Values: none, auto, required, or
              specific tool.

          tools: A list of tools the model may call. Currently, only functions are supported. Max
              128 functions.

          top_k: Only sample from the top K options for each subsequent token

          top_logprobs: Number of most likely tokens to return at each position, with associated log
              probability.

          top_p: Alternative to temperature. Only tokens comprising top_p probability mass are
              considered.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        messages: Iterable[Dict[str, object]],
        model: str,
        stream: Literal[True],
        audio: Dict[str, object] | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        function_call: Dict[str, object] | NotGiven = NOT_GIVEN,
        functions: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        modalities: List[str] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: Dict[str, object] | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        reasoning_effort: str | NotGiven = NOT_GIVEN,
        response_format: Dict[str, object] | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        store: bool | NotGiven = NOT_GIVEN,
        stream_options: Dict[str, object] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, Dict[str, object]] | NotGiven = NOT_GIVEN,
        tools: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Stream[ChatCompletionChunk]:
        """
        Chat Completions

        Args:
          messages: openai standard message format

          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          stream: If true, partial message deltas will be sent as server-sent events.

          audio: Parameters for audio output. Required when audio output is requested with
              modalities: ['audio'].

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far.

          function_call: Deprecated in favor of tool_choice. Controls which function is called by the
              model.

          functions: Deprecated in favor of tools. A list of functions the model may generate JSON
              inputs for.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Maps
              tokens to bias values from -100 to 100.

          logprobs: Whether to return log probabilities of the output tokens or not.

          max_completion_tokens: An upper bound for the number of tokens that can be generated, including visible
              output tokens and reasoning tokens.

          max_tokens: Deprecated in favor of max_completion_tokens. The maximum number of tokens to
              generate.

          metadata: Developer-defined tags and values used for filtering completions in the
              dashboard.

          modalities: Output types that you would like the model to generate for this request.

          n: How many chat completion choices to generate for each input message.

          parallel_tool_calls: Whether to enable parallel function calling during tool use.

          prediction: Static predicted output content, such as the content of a text file being
              regenerated.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize tokens based on whether
              they appear in the text so far.

          reasoning_effort: For o1 models only. Constrains effort on reasoning. Values: low, medium, high.

          response_format: An object specifying the format that the model must output.

          seed: If specified, system will attempt to sample deterministically for repeated
              requests with same seed.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          store: Whether to store the output for use in model distillation or evals products.

          stream_options: Options for streaming response. Only set this when stream is true.

          temperature: What sampling temperature to use. Higher values make output more random, lower
              more focused.

          tool_choice: Controls which tool is called by the model. Values: none, auto, required, or
              specific tool.

          tools: A list of tools the model may call. Currently, only functions are supported. Max
              128 functions.

          top_k: Only sample from the top K options for each subsequent token

          top_logprobs: Number of most likely tokens to return at each position, with associated log
              probability.

          top_p: Alternative to temperature. Only tokens comprising top_p probability mass are
              considered.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        messages: Iterable[Dict[str, object]],
        model: str,
        stream: bool,
        audio: Dict[str, object] | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        function_call: Dict[str, object] | NotGiven = NOT_GIVEN,
        functions: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        modalities: List[str] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: Dict[str, object] | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        reasoning_effort: str | NotGiven = NOT_GIVEN,
        response_format: Dict[str, object] | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        store: bool | NotGiven = NOT_GIVEN,
        stream_options: Dict[str, object] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, Dict[str, object]] | NotGiven = NOT_GIVEN,
        tools: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionCreateResponse | Stream[ChatCompletionChunk]:
        """
        Chat Completions

        Args:
          messages: openai standard message format

          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          stream: If true, partial message deltas will be sent as server-sent events.

          audio: Parameters for audio output. Required when audio output is requested with
              modalities: ['audio'].

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far.

          function_call: Deprecated in favor of tool_choice. Controls which function is called by the
              model.

          functions: Deprecated in favor of tools. A list of functions the model may generate JSON
              inputs for.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Maps
              tokens to bias values from -100 to 100.

          logprobs: Whether to return log probabilities of the output tokens or not.

          max_completion_tokens: An upper bound for the number of tokens that can be generated, including visible
              output tokens and reasoning tokens.

          max_tokens: Deprecated in favor of max_completion_tokens. The maximum number of tokens to
              generate.

          metadata: Developer-defined tags and values used for filtering completions in the
              dashboard.

          modalities: Output types that you would like the model to generate for this request.

          n: How many chat completion choices to generate for each input message.

          parallel_tool_calls: Whether to enable parallel function calling during tool use.

          prediction: Static predicted output content, such as the content of a text file being
              regenerated.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize tokens based on whether
              they appear in the text so far.

          reasoning_effort: For o1 models only. Constrains effort on reasoning. Values: low, medium, high.

          response_format: An object specifying the format that the model must output.

          seed: If specified, system will attempt to sample deterministically for repeated
              requests with same seed.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          store: Whether to store the output for use in model distillation or evals products.

          stream_options: Options for streaming response. Only set this when stream is true.

          temperature: What sampling temperature to use. Higher values make output more random, lower
              more focused.

          tool_choice: Controls which tool is called by the model. Values: none, auto, required, or
              specific tool.

          tools: A list of tools the model may call. Currently, only functions are supported. Max
              128 functions.

          top_k: Only sample from the top K options for each subsequent token

          top_logprobs: Number of most likely tokens to return at each position, with associated log
              probability.

          top_p: Alternative to temperature. Only tokens comprising top_p probability mass are
              considered.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["messages", "model"], ["messages", "model", "stream"])
    def create(
        self,
        *,
        messages: Iterable[Dict[str, object]],
        model: str,
        audio: Dict[str, object] | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        function_call: Dict[str, object] | NotGiven = NOT_GIVEN,
        functions: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        modalities: List[str] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: Dict[str, object] | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        reasoning_effort: str | NotGiven = NOT_GIVEN,
        response_format: Dict[str, object] | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        store: bool | NotGiven = NOT_GIVEN,
        stream: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
        stream_options: Dict[str, object] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, Dict[str, object]] | NotGiven = NOT_GIVEN,
        tools: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionCreateResponse | Stream[ChatCompletionChunk]:
        return self._post(
            "/v5/chat/completions",
            body=maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "audio": audio,
                    "frequency_penalty": frequency_penalty,
                    "function_call": function_call,
                    "functions": functions,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_completion_tokens": max_completion_tokens,
                    "max_tokens": max_tokens,
                    "metadata": metadata,
                    "modalities": modalities,
                    "n": n,
                    "parallel_tool_calls": parallel_tool_calls,
                    "prediction": prediction,
                    "presence_penalty": presence_penalty,
                    "reasoning_effort": reasoning_effort,
                    "response_format": response_format,
                    "seed": seed,
                    "stop": stop,
                    "store": store,
                    "stream": stream,
                    "stream_options": stream_options,
                    "temperature": temperature,
                    "tool_choice": tool_choice,
                    "tools": tools,
                    "top_k": top_k,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                },
                completion_create_params.CompletionCreateParamsStreaming
                if stream
                else completion_create_params.CompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=cast(
                Any, CompletionCreateResponse
            ),  # Union types cannot be passed in as arguments in the type system
            stream=stream or False,
            stream_cls=Stream[ChatCompletionChunk],
        )

    def models(
        self,
        *,
        ending_before: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        model_vendor: Literal[
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
        ]
        | NotGiven = NOT_GIVEN,
        sort_order: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionModelsResponse:
        """
        List Chat Completion Models

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v5/chat/completions/models",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "model_vendor": model_vendor,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    completion_models_params.CompletionModelsParams,
                ),
            ),
            cast_to=CompletionModelsResponse,
        )


class AsyncCompletionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCompletionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncCompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompletionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncCompletionsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        messages: Iterable[Dict[str, object]],
        model: str,
        audio: Dict[str, object] | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        function_call: Dict[str, object] | NotGiven = NOT_GIVEN,
        functions: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        modalities: List[str] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: Dict[str, object] | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        reasoning_effort: str | NotGiven = NOT_GIVEN,
        response_format: Dict[str, object] | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        store: bool | NotGiven = NOT_GIVEN,
        stream: Literal[False] | NotGiven = NOT_GIVEN,
        stream_options: Dict[str, object] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, Dict[str, object]] | NotGiven = NOT_GIVEN,
        tools: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionCreateResponse:
        """
        Chat Completions

        Args:
          messages: openai standard message format

          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          audio: Parameters for audio output. Required when audio output is requested with
              modalities: ['audio'].

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far.

          function_call: Deprecated in favor of tool_choice. Controls which function is called by the
              model.

          functions: Deprecated in favor of tools. A list of functions the model may generate JSON
              inputs for.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Maps
              tokens to bias values from -100 to 100.

          logprobs: Whether to return log probabilities of the output tokens or not.

          max_completion_tokens: An upper bound for the number of tokens that can be generated, including visible
              output tokens and reasoning tokens.

          max_tokens: Deprecated in favor of max_completion_tokens. The maximum number of tokens to
              generate.

          metadata: Developer-defined tags and values used for filtering completions in the
              dashboard.

          modalities: Output types that you would like the model to generate for this request.

          n: How many chat completion choices to generate for each input message.

          parallel_tool_calls: Whether to enable parallel function calling during tool use.

          prediction: Static predicted output content, such as the content of a text file being
              regenerated.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize tokens based on whether
              they appear in the text so far.

          reasoning_effort: For o1 models only. Constrains effort on reasoning. Values: low, medium, high.

          response_format: An object specifying the format that the model must output.

          seed: If specified, system will attempt to sample deterministically for repeated
              requests with same seed.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          store: Whether to store the output for use in model distillation or evals products.

          stream: If true, partial message deltas will be sent as server-sent events.

          stream_options: Options for streaming response. Only set this when stream is true.

          temperature: What sampling temperature to use. Higher values make output more random, lower
              more focused.

          tool_choice: Controls which tool is called by the model. Values: none, auto, required, or
              specific tool.

          tools: A list of tools the model may call. Currently, only functions are supported. Max
              128 functions.

          top_k: Only sample from the top K options for each subsequent token

          top_logprobs: Number of most likely tokens to return at each position, with associated log
              probability.

          top_p: Alternative to temperature. Only tokens comprising top_p probability mass are
              considered.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        messages: Iterable[Dict[str, object]],
        model: str,
        stream: Literal[True],
        audio: Dict[str, object] | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        function_call: Dict[str, object] | NotGiven = NOT_GIVEN,
        functions: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        modalities: List[str] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: Dict[str, object] | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        reasoning_effort: str | NotGiven = NOT_GIVEN,
        response_format: Dict[str, object] | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        store: bool | NotGiven = NOT_GIVEN,
        stream_options: Dict[str, object] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, Dict[str, object]] | NotGiven = NOT_GIVEN,
        tools: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncStream[ChatCompletionChunk]:
        """
        Chat Completions

        Args:
          messages: openai standard message format

          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          stream: If true, partial message deltas will be sent as server-sent events.

          audio: Parameters for audio output. Required when audio output is requested with
              modalities: ['audio'].

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far.

          function_call: Deprecated in favor of tool_choice. Controls which function is called by the
              model.

          functions: Deprecated in favor of tools. A list of functions the model may generate JSON
              inputs for.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Maps
              tokens to bias values from -100 to 100.

          logprobs: Whether to return log probabilities of the output tokens or not.

          max_completion_tokens: An upper bound for the number of tokens that can be generated, including visible
              output tokens and reasoning tokens.

          max_tokens: Deprecated in favor of max_completion_tokens. The maximum number of tokens to
              generate.

          metadata: Developer-defined tags and values used for filtering completions in the
              dashboard.

          modalities: Output types that you would like the model to generate for this request.

          n: How many chat completion choices to generate for each input message.

          parallel_tool_calls: Whether to enable parallel function calling during tool use.

          prediction: Static predicted output content, such as the content of a text file being
              regenerated.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize tokens based on whether
              they appear in the text so far.

          reasoning_effort: For o1 models only. Constrains effort on reasoning. Values: low, medium, high.

          response_format: An object specifying the format that the model must output.

          seed: If specified, system will attempt to sample deterministically for repeated
              requests with same seed.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          store: Whether to store the output for use in model distillation or evals products.

          stream_options: Options for streaming response. Only set this when stream is true.

          temperature: What sampling temperature to use. Higher values make output more random, lower
              more focused.

          tool_choice: Controls which tool is called by the model. Values: none, auto, required, or
              specific tool.

          tools: A list of tools the model may call. Currently, only functions are supported. Max
              128 functions.

          top_k: Only sample from the top K options for each subsequent token

          top_logprobs: Number of most likely tokens to return at each position, with associated log
              probability.

          top_p: Alternative to temperature. Only tokens comprising top_p probability mass are
              considered.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        messages: Iterable[Dict[str, object]],
        model: str,
        stream: bool,
        audio: Dict[str, object] | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        function_call: Dict[str, object] | NotGiven = NOT_GIVEN,
        functions: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        modalities: List[str] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: Dict[str, object] | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        reasoning_effort: str | NotGiven = NOT_GIVEN,
        response_format: Dict[str, object] | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        store: bool | NotGiven = NOT_GIVEN,
        stream_options: Dict[str, object] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, Dict[str, object]] | NotGiven = NOT_GIVEN,
        tools: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionCreateResponse | AsyncStream[ChatCompletionChunk]:
        """
        Chat Completions

        Args:
          messages: openai standard message format

          model: model specified as `model_vendor/model`, for example `openai/gpt-4o`

          stream: If true, partial message deltas will be sent as server-sent events.

          audio: Parameters for audio output. Required when audio output is requested with
              modalities: ['audio'].

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far.

          function_call: Deprecated in favor of tool_choice. Controls which function is called by the
              model.

          functions: Deprecated in favor of tools. A list of functions the model may generate JSON
              inputs for.

          logit_bias: Modify the likelihood of specified tokens appearing in the completion. Maps
              tokens to bias values from -100 to 100.

          logprobs: Whether to return log probabilities of the output tokens or not.

          max_completion_tokens: An upper bound for the number of tokens that can be generated, including visible
              output tokens and reasoning tokens.

          max_tokens: Deprecated in favor of max_completion_tokens. The maximum number of tokens to
              generate.

          metadata: Developer-defined tags and values used for filtering completions in the
              dashboard.

          modalities: Output types that you would like the model to generate for this request.

          n: How many chat completion choices to generate for each input message.

          parallel_tool_calls: Whether to enable parallel function calling during tool use.

          prediction: Static predicted output content, such as the content of a text file being
              regenerated.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize tokens based on whether
              they appear in the text so far.

          reasoning_effort: For o1 models only. Constrains effort on reasoning. Values: low, medium, high.

          response_format: An object specifying the format that the model must output.

          seed: If specified, system will attempt to sample deterministically for repeated
              requests with same seed.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          store: Whether to store the output for use in model distillation or evals products.

          stream_options: Options for streaming response. Only set this when stream is true.

          temperature: What sampling temperature to use. Higher values make output more random, lower
              more focused.

          tool_choice: Controls which tool is called by the model. Values: none, auto, required, or
              specific tool.

          tools: A list of tools the model may call. Currently, only functions are supported. Max
              128 functions.

          top_k: Only sample from the top K options for each subsequent token

          top_logprobs: Number of most likely tokens to return at each position, with associated log
              probability.

          top_p: Alternative to temperature. Only tokens comprising top_p probability mass are
              considered.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["messages", "model"], ["messages", "model", "stream"])
    async def create(
        self,
        *,
        messages: Iterable[Dict[str, object]],
        model: str,
        audio: Dict[str, object] | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        function_call: Dict[str, object] | NotGiven = NOT_GIVEN,
        functions: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        metadata: Dict[str, str] | NotGiven = NOT_GIVEN,
        modalities: List[str] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: Dict[str, object] | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        reasoning_effort: str | NotGiven = NOT_GIVEN,
        response_format: Dict[str, object] | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        store: bool | NotGiven = NOT_GIVEN,
        stream: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
        stream_options: Dict[str, object] | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: Union[str, Dict[str, object]] | NotGiven = NOT_GIVEN,
        tools: Iterable[Dict[str, object]] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionCreateResponse | AsyncStream[ChatCompletionChunk]:
        return await self._post(
            "/v5/chat/completions",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "audio": audio,
                    "frequency_penalty": frequency_penalty,
                    "function_call": function_call,
                    "functions": functions,
                    "logit_bias": logit_bias,
                    "logprobs": logprobs,
                    "max_completion_tokens": max_completion_tokens,
                    "max_tokens": max_tokens,
                    "metadata": metadata,
                    "modalities": modalities,
                    "n": n,
                    "parallel_tool_calls": parallel_tool_calls,
                    "prediction": prediction,
                    "presence_penalty": presence_penalty,
                    "reasoning_effort": reasoning_effort,
                    "response_format": response_format,
                    "seed": seed,
                    "stop": stop,
                    "store": store,
                    "stream": stream,
                    "stream_options": stream_options,
                    "temperature": temperature,
                    "tool_choice": tool_choice,
                    "tools": tools,
                    "top_k": top_k,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                },
                completion_create_params.CompletionCreateParamsStreaming
                if stream
                else completion_create_params.CompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=cast(
                Any, CompletionCreateResponse
            ),  # Union types cannot be passed in as arguments in the type system
            stream=stream or False,
            stream_cls=AsyncStream[ChatCompletionChunk],
        )

    async def models(
        self,
        *,
        ending_before: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        model_vendor: Literal[
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
        ]
        | NotGiven = NOT_GIVEN,
        sort_order: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionModelsResponse:
        """
        List Chat Completion Models

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v5/chat/completions/models",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "model_vendor": model_vendor,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    completion_models_params.CompletionModelsParams,
                ),
            ),
            cast_to=CompletionModelsResponse,
        )


class CompletionsResourceWithRawResponse:
    def __init__(self, completions: CompletionsResource) -> None:
        self._completions = completions

        self.create = to_raw_response_wrapper(
            completions.create,
        )
        self.models = to_raw_response_wrapper(
            completions.models,
        )


class AsyncCompletionsResourceWithRawResponse:
    def __init__(self, completions: AsyncCompletionsResource) -> None:
        self._completions = completions

        self.create = async_to_raw_response_wrapper(
            completions.create,
        )
        self.models = async_to_raw_response_wrapper(
            completions.models,
        )


class CompletionsResourceWithStreamingResponse:
    def __init__(self, completions: CompletionsResource) -> None:
        self._completions = completions

        self.create = to_streamed_response_wrapper(
            completions.create,
        )
        self.models = to_streamed_response_wrapper(
            completions.models,
        )


class AsyncCompletionsResourceWithStreamingResponse:
    def __init__(self, completions: AsyncCompletionsResource) -> None:
        self._completions = completions

        self.create = async_to_streamed_response_wrapper(
            completions.create,
        )
        self.models = async_to_streamed_response_wrapper(
            completions.models,
        )

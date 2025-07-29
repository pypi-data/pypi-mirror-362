# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional, overload
from typing_extensions import Literal

import httpx

from ..types import chat_completion_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    required_args,
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._streaming import Stream, AsyncStream
from .._base_client import (
    make_request_options,
)
from ..types.chat_completion_create_response import ChatCompletionCreateResponse
from ..types.chat_completion_create_chunk_response import ChatCompletionChunkResponse

__all__ = ["ChatCompletionsResource", "AsyncChatCompletionsResource"]


class ChatCompletionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChatCompletionsResourceWithRawResponse:
        return ChatCompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChatCompletionsResourceWithStreamingResponse:
        return ChatCompletionsResourceWithStreamingResponse(self)
    
    @overload
    def create(
        self,
        *,
        messages: Iterable[chat_completion_create_params.Message],
        model: Union[str, Literal["kilm-7b", "kilm-13b"]],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        response_format: chat_completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        bad_words: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        stream_options: Optional[chat_completion_create_params.StreamOptions] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        beam_width: Optional[int] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionCreateResponse:
        """
        Creates a model response for the given chat conversation.

        Args:
          messages: A list of messages comprising the conversation so far.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_format_inputs_to_chatgpt_models).

          model: ID of the model to use. See the
              [model endpoint compatibility](/docs/models/model-endpoint-compatibility) table
              for details on which models work with the Chat API.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

              [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

              [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the `content` of
              `message`.

          max_tokens: The maximum number of [tokens](/tokenizer) that can be generated in the chat
              completion.

              The total length of input tokens and generated tokens is limited by the model's
              context length.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_count_tokens_with_tiktoken)
              for counting tokens.

          response_format: An object specifying the format that the model must output. Compatible with
              [GPT-4 Turbo](/docs/models/gpt-4-and-gpt-4-turbo) and all GPT-3.5 Turbo models
              newer than `gpt-3.5-turbo-1106`.

              Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the
              message the model generates is valid JSON.

              **Important:** when using JSON mode, you **must** also instruct the model to
              produce JSON yourself via a system or user message. Without this, the model may
              generate an unending stream of whitespace until the generation reaches the token
              limit, resulting in a long-running and seemingly "stuck" request. Also note that
              the message content may be partially cut off if `finish_reason="length"`, which
              indicates the generation exceeded `max_tokens` or the conversation exceeded the
              max context length.

          seed: This feature is in Beta. If specified, our system will make a best effort to
              sample deterministically, such that repeated requests with the same `seed` and
              parameters should return the same result. Determinism is not guaranteed, and you
              should refer to the `system_fingerprint` response parameter to monitor changes
              in the backend.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream: If set, partial message deltas will be sent, like in ChatGPT. Tokens will be
              sent as data-only
              [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
              as they become available, with the stream terminated by a `data: [DONE]`
              message.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_stream_completions).

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic.

              We generally recommend altering this or `top_p` but not both.

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.
              `logprobs` must be set to `true` if this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              We generally recommend altering this or `temperature` but not both.

          top_k: An integer specifying the number of highest probability vocabulary tokens to keep
              for top-k-filtering.
              
          beam_width: An integer specifying the number of beams to use for beam search. Must be between 1 and 20.
              
          repetition_penalty: The parameter for repetition penalty. 1.0 means no penalty. See
              [this paper](https://arxiv.org/abs/1909.05858) for more details.

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
        messages: Iterable[chat_completion_create_params.Message],
        model: Union[str, Literal["kilm-7b", "kilm-13b"]],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        response_format: chat_completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        bad_words: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        stream: Literal[True],
        stream_options: Optional[chat_completion_create_params.StreamOptions] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        beam_width: Optional[int] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Stream[ChatCompletionChunkResponse]:
        """
        Creates a model response for the given chat conversation.

        Args:
          messages: A list of messages comprising the conversation so far.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_format_inputs_to_chatgpt_models).

          model: ID of the model to use. See the
              [model endpoint compatibility](/docs/models/model-endpoint-compatibility) table
              for details on which models work with the Chat API.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

              [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

              [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the `content` of
              `message`.

          max_tokens: The maximum number of [tokens](/tokenizer) that can be generated in the chat
              completion.

              The total length of input tokens and generated tokens is limited by the model's
              context length.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_count_tokens_with_tiktoken)
              for counting tokens.

          response_format: An object specifying the format that the model must output. Compatible with
              [GPT-4 Turbo](/docs/models/gpt-4-and-gpt-4-turbo) and all GPT-3.5 Turbo models
              newer than `gpt-3.5-turbo-1106`.

              Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the
              message the model generates is valid JSON.

              **Important:** when using JSON mode, you **must** also instruct the model to
              produce JSON yourself via a system or user message. Without this, the model may
              generate an unending stream of whitespace until the generation reaches the token
              limit, resulting in a long-running and seemingly "stuck" request. Also note that
              the message content may be partially cut off if `finish_reason="length"`, which
              indicates the generation exceeded `max_tokens` or the conversation exceeded the
              max context length.

          seed: This feature is in Beta. If specified, our system will make a best effort to
              sample deterministically, such that repeated requests with the same `seed` and
              parameters should return the same result. Determinism is not guaranteed, and you
              should refer to the `system_fingerprint` response parameter to monitor changes
              in the backend.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream: If set, partial message deltas will be sent, like in ChatGPT. Tokens will be
              sent as data-only
              [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
              as they become available, with the stream terminated by a `data: [DONE]`
              message.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_stream_completions).

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic.

              We generally recommend altering this or `top_p` but not both.

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.
              `logprobs` must be set to `true` if this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              We generally recommend altering this or `temperature` but not both.

          top_k: An integer specifying the number of highest probability vocabulary tokens to keep
              for top-k-filtering.
              
          beam_width: An integer specifying the number of beams to use for beam search. Must be between 1 and 20.
              
          repetition_penalty: The parameter for repetition penalty. 1.0 means no penalty. See
              [this paper](https://arxiv.org/abs/1909.05858) for more details.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """

    
    @overload
    def create(
        self,
        *,
        stream: bool,
        messages: Iterable[chat_completion_create_params.Message],
        model: Union[str, Literal["kilm-7b", "kilm-13b"]],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        response_format: chat_completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        bad_words: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        stream_options: Optional[chat_completion_create_params.StreamOptions] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        beam_width: Optional[int] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionCreateResponse | Stream[ChatCompletionChunkResponse]:
        """
        Creates a model response for the given chat conversation.

        Args:
          messages: A list of messages comprising the conversation so far.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_format_inputs_to_chatgpt_models).

          model: ID of the model to use. See the
              [model endpoint compatibility](/docs/models/model-endpoint-compatibility) table
              for details on which models work with the Chat API.

          frequency_penalty: Number between 0.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

              [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)

          presence_penalty: Number between 0.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

              [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the `content` of
              `message`.

          max_tokens: The maximum number of [tokens](/tokenizer) that can be generated in the chat
              completion.

              The total length of input tokens and generated tokens is limited by the model's
              context length.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_count_tokens_with_tiktoken)
              for counting tokens.

          response_format: An object specifying the format that the model must output. Compatible with
              [GPT-4 Turbo](/docs/models/gpt-4-and-gpt-4-turbo) and all GPT-3.5 Turbo models
              newer than `gpt-3.5-turbo-1106`.

              Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the
              message the model generates is valid JSON.

              **Important:** when using JSON mode, you **must** also instruct the model to
              produce JSON yourself via a system or user message. Without this, the model may
              generate an unending stream of whitespace until the generation reaches the token
              limit, resulting in a long-running and seemingly "stuck" request. Also note that
              the message content may be partially cut off if `finish_reason="length"`, which
              indicates the generation exceeded `max_tokens` or the conversation exceeded the
              max context length.

          seed: This feature is in Beta. If specified, our system will make a best effort to
              sample deterministically, such that repeated requests with the same `seed` and
              parameters should return the same result. Determinism is not guaranteed, and you
              should refer to the `system_fingerprint` response parameter to monitor changes
              in the backend.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream: If set, partial message deltas will be sent, like in ChatGPT. Tokens will be
              sent as data-only
              [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
              as they become available, with the stream terminated by a `data: [DONE]`
              message.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_stream_completions).

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic.

              We generally recommend altering this or `top_p` but not both.

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.
              `logprobs` must be set to `true` if this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              We generally recommend altering this or `temperature` but not both.

          top_k: An integer specifying the number of highest probability vocabulary tokens to keep
              for top-k-filtering.
              
          beam_width: An integer specifying the number of beams to use for beam search. Must be between 1 and 20.
              
          repetition_penalty: The parameter for repetition penalty. 1.0 means no penalty. See
              [this paper](https://arxiv.org/abs/1909.05858) for more details.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """

    @required_args(["messages", "model"], ["messages", "model", "stream"])
    def create(
        self,
        *,
        messages: Iterable[chat_completion_create_params.Message],
        model: Union[str, Literal["kilm-7b", "kilm-13b"]],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        response_format: chat_completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        bad_words: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        stream_options: Optional[chat_completion_create_params.StreamOptions] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        beam_width: Optional[int] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionCreateResponse | Stream[ChatCompletionChunkResponse]:
        return self._post(
            "/chat/completions/",
            body=maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "frequency_penalty": frequency_penalty,
                    "presence_penalty": presence_penalty,
                    "logprobs": logprobs,
                    "max_tokens": max_tokens,
                    "response_format": response_format,
                    "seed": seed,
                    "stop": stop,
                    "bad_words": bad_words,
                    "stream": stream,
                    "stream_options": stream_options,
                    "temperature": temperature,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                    "top_k": top_k,
                    "beam_width": beam_width,
                    "repetition_penalty": repetition_penalty,
                },
                chat_completion_create_params.ChatCompletionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCompletionCreateResponse,
            stream=stream or False,
            stream_cls=Stream[ChatCompletionChunkResponse],
        )


class AsyncChatCompletionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChatCompletionsResourceWithRawResponse:
        return AsyncChatCompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChatCompletionsResourceWithStreamingResponse:
        return AsyncChatCompletionsResourceWithStreamingResponse(self)
    
    @overload
    async def create(
        self,
        *,
        messages: Iterable[chat_completion_create_params.Message],
        model: Union[str, Literal["kilm-7b", "kilm-13b"]],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        response_format: chat_completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        bad_words: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        stream_options: Optional[chat_completion_create_params.StreamOptions] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        beam_width: Optional[int] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionCreateResponse:
        """
        Creates a model response for the given chat conversation.

        Args:
          messages: A list of messages comprising the conversation so far.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_format_inputs_to_chatgpt_models).

          model: ID of the model to use. See the
              [model endpoint compatibility](/docs/models/model-endpoint-compatibility) table
              for details on which models work with the Chat API.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

              [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

              [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the `content` of
              `message`.

          max_tokens: The maximum number of [tokens](/tokenizer) that can be generated in the chat
              completion.

              The total length of input tokens and generated tokens is limited by the model's
              context length.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_count_tokens_with_tiktoken)
              for counting tokens.

          response_format: An object specifying the format that the model must output. Compatible with
              [GPT-4 Turbo](/docs/models/gpt-4-and-gpt-4-turbo) and all GPT-3.5 Turbo models
              newer than `gpt-3.5-turbo-1106`.

              Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the
              message the model generates is valid JSON.

              **Important:** when using JSON mode, you **must** also instruct the model to
              produce JSON yourself via a system or user message. Without this, the model may
              generate an unending stream of whitespace until the generation reaches the token
              limit, resulting in a long-running and seemingly "stuck" request. Also note that
              the message content may be partially cut off if `finish_reason="length"`, which
              indicates the generation exceeded `max_tokens` or the conversation exceeded the
              max context length.

          seed: This feature is in Beta. If specified, our system will make a best effort to
              sample deterministically, such that repeated requests with the same `seed` and
              parameters should return the same result. Determinism is not guaranteed, and you
              should refer to the `system_fingerprint` response parameter to monitor changes
              in the backend.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream: If set, partial message deltas will be sent, like in ChatGPT. Tokens will be
              sent as data-only
              [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
              as they become available, with the stream terminated by a `data: [DONE]`
              message.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_stream_completions).

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic.

              We generally recommend altering this or `top_p` but not both.

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.
              `logprobs` must be set to `true` if this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              We generally recommend altering this or `temperature` but not both.

          top_k: An integer specifying the number of highest probability vocabulary tokens to keep
              for top-k-filtering.
              
          beam_width: An integer specifying the number of beams to use for beam search. Must be between 1 and 20.
              
          repetition_penalty: The parameter for repetition penalty. 1.0 means no penalty. See
              [this paper](https://arxiv.org/abs/1909.05858) for more details.

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
        messages: Iterable[chat_completion_create_params.Message],
        stream: Literal[True],
        model: Union[str, Literal["kilm-7b", "kilm-13b"]],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        response_format: chat_completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        bad_words: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        stream_options: Optional[chat_completion_create_params.StreamOptions] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        beam_width: Optional[int] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncStream[ChatCompletionChunkResponse]:
        """
        Creates a model response for the given chat conversation.

        Args:
          messages: A list of messages comprising the conversation so far.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_format_inputs_to_chatgpt_models).

          model: ID of the model to use. See the
              [model endpoint compatibility](/docs/models/model-endpoint-compatibility) table
              for details on which models work with the Chat API.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

              [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

              [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the `content` of
              `message`.

          max_tokens: The maximum number of [tokens](/tokenizer) that can be generated in the chat
              completion.

              The total length of input tokens and generated tokens is limited by the model's
              context length.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_count_tokens_with_tiktoken)
              for counting tokens.

          response_format: An object specifying the format that the model must output. Compatible with
              [GPT-4 Turbo](/docs/models/gpt-4-and-gpt-4-turbo) and all GPT-3.5 Turbo models
              newer than `gpt-3.5-turbo-1106`.

              Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the
              message the model generates is valid JSON.

              **Important:** when using JSON mode, you **must** also instruct the model to
              produce JSON yourself via a system or user message. Without this, the model may
              generate an unending stream of whitespace until the generation reaches the token
              limit, resulting in a long-running and seemingly "stuck" request. Also note that
              the message content may be partially cut off if `finish_reason="length"`, which
              indicates the generation exceeded `max_tokens` or the conversation exceeded the
              max context length.

          seed: This feature is in Beta. If specified, our system will make a best effort to
              sample deterministically, such that repeated requests with the same `seed` and
              parameters should return the same result. Determinism is not guaranteed, and you
              should refer to the `system_fingerprint` response parameter to monitor changes
              in the backend.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream: If set, partial message deltas will be sent, like in ChatGPT. Tokens will be
              sent as data-only
              [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
              as they become available, with the stream terminated by a `data: [DONE]`
              message.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_stream_completions).

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic.

              We generally recommend altering this or `top_p` but not both.

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.
              `logprobs` must be set to `true` if this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              We generally recommend altering this or `temperature` but not both.

          top_k: An integer specifying the number of highest probability vocabulary tokens to keep
              for top-k-filtering.
              
          beam_width: An integer specifying the number of beams to use for beam search. Must be between 1 and 20.
              
          repetition_penalty: The parameter for repetition penalty. 1.0 means no penalty. See
              [this paper](https://arxiv.org/abs/1909.05858) for more details.

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
        messages: Iterable[chat_completion_create_params.Message],
        model: Union[str, Literal["kilm-7b", "kilm-13b"]],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        stream: bool,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        response_format: chat_completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        bad_words: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        stream_options: Optional[chat_completion_create_params.StreamOptions] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        beam_width: Optional[int] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionCreateResponse | AsyncStream[ChatCompletionChunkResponse]:
        """
        Creates a model response for the given chat conversation.

        Args:
          messages: A list of messages comprising the conversation so far.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_format_inputs_to_chatgpt_models).

          model: ID of the model to use. See the
              [model endpoint compatibility](/docs/models/model-endpoint-compatibility) table
              for details on which models work with the Chat API.

          frequency_penalty: Number between 0.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

              [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)

          presence_penalty: Number between 0.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

              [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the `content` of
              `message`.

          max_tokens: The maximum number of [tokens](/tokenizer) that can be generated in the chat
              completion.

              The total length of input tokens and generated tokens is limited by the model's
              context length.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_count_tokens_with_tiktoken)
              for counting tokens.

          response_format: An object specifying the format that the model must output. Compatible with
              [GPT-4 Turbo](/docs/models/gpt-4-and-gpt-4-turbo) and all GPT-3.5 Turbo models
              newer than `gpt-3.5-turbo-1106`.

              Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the
              message the model generates is valid JSON.

              **Important:** when using JSON mode, you **must** also instruct the model to
              produce JSON yourself via a system or user message. Without this, the model may
              generate an unending stream of whitespace until the generation reaches the token
              limit, resulting in a long-running and seemingly "stuck" request. Also note that
              the message content may be partially cut off if `finish_reason="length"`, which
              indicates the generation exceeded `max_tokens` or the conversation exceeded the
              max context length.

          seed: This feature is in Beta. If specified, our system will make a best effort to
              sample deterministically, such that repeated requests with the same `seed` and
              parameters should return the same result. Determinism is not guaranteed, and you
              should refer to the `system_fingerprint` response parameter to monitor changes
              in the backend.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream: If set, partial message deltas will be sent, like in ChatGPT. Tokens will be
              sent as data-only
              [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
              as they become available, with the stream terminated by a `data: [DONE]`
              message.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_stream_completions).

          stream_options: Options for streaming response. Only set this when you set `stream: true`.

          temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic.

              We generally recommend altering this or `top_p` but not both.

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability.
              `logprobs` must be set to `true` if this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              We generally recommend altering this or `temperature` but not both.

          top_k: An integer specifying the number of highest probability vocabulary tokens to keep
              for top-k-filtering.
              
          beam_width: An integer specifying the number of beams to use for beam search. Must be between 1 and 20.
              
          repetition_penalty: The parameter for repetition penalty. 1.0 means no penalty. See
              [this paper](https://arxiv.org/abs/1909.05858) for more details.

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
        messages: Iterable[chat_completion_create_params.Message],
        model: Union[str, Literal["kilm-7b", "kilm-13b"]],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        response_format: chat_completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        bad_words: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        stream_options: Optional[chat_completion_create_params.StreamOptions] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        beam_width: Optional[int] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletionCreateResponse | AsyncStream[ChatCompletionChunkResponse]:
        return await self._post(
            "/chat/completions/",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "frequency_penalty": frequency_penalty,
                    "presence_penalty": presence_penalty,
                    "logprobs": logprobs,
                    "max_tokens": max_tokens,
                    "response_format": response_format,
                    "seed": seed,
                    "stop": stop,
                    "bad_words": bad_words,
                    "stream": stream,
                    "stream_options": stream_options,
                    "temperature": temperature,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                    "top_k": top_k,
                    "beam_width": beam_width,
                    "repetition_penalty": repetition_penalty,
                },
                chat_completion_create_params.ChatCompletionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCompletionCreateResponse,
            stream=stream or False,
            stream_cls=AsyncStream[ChatCompletionChunkResponse],
        )


class ChatCompletionsResourceWithRawResponse:
    def __init__(self, chat_completions: ChatCompletionsResource) -> None:
        self._chat_completions = chat_completions

        self.create = to_raw_response_wrapper(
            chat_completions.create,
        )


class AsyncChatCompletionsResourceWithRawResponse:
    def __init__(self, chat_completions: AsyncChatCompletionsResource) -> None:
        self._chat_completions = chat_completions

        self.create = async_to_raw_response_wrapper(
            chat_completions.create,
        )


class ChatCompletionsResourceWithStreamingResponse:
    def __init__(self, chat_completions: ChatCompletionsResource) -> None:
        self._chat_completions = chat_completions

        self.create = to_streamed_response_wrapper(
            chat_completions.create,
        )


class AsyncChatCompletionsResourceWithStreamingResponse:
    def __init__(self, chat_completions: AsyncChatCompletionsResource) -> None:
        self._chat_completions = chat_completions

        self.create = async_to_streamed_response_wrapper(
            chat_completions.create,
        )

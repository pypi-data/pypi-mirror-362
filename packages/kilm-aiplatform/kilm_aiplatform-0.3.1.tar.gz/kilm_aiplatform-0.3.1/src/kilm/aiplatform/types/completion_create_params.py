# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["CompletionCreateParams", "StreamOptions"]


class CompletionCreateParams(TypedDict, total=False):
    model: Required[Union[str, Literal["kilm-7b", "kilm-13b"]]]
    """ID of the model to use.

    You can use the [List models](/docs/api-reference/models/list) API to see all of
    your available models, or see our [Model overview](/docs/models/overview) for
    descriptions of them.
    """

    prompt: Required[object]
    """
    The prompt(s) to generate completions for, encoded as a string, array of
    strings, array of tokens, or array of token arrays.

    Note that <|endoftext|> is the document separator that the model sees during
    training, so if a prompt is not specified the model will generate as if from the
    beginning of a new document.
    """

    frequency_penalty: Optional[float]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on their existing frequency in the
    text so far, decreasing the model's likelihood to repeat the same line verbatim.

    [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)
    """

    logprobs: Optional[int]
    """
    Include the log probabilities on the `logprobs` most likely output tokens, as
    well the chosen tokens. For example, if `logprobs` is 5, the API will return a
    list of the 5 most likely tokens. The API will always return the `logprob` of
    the sampled token, so there may be up to `logprobs+1` elements in the response.

    The maximum value for `logprobs` is 5.
    """

    max_tokens: Optional[int]
    """
    The maximum number of [tokens](/tokenizer) that can be generated in the
    completion.

    The token count of your prompt plus `max_tokens` cannot exceed the model's
    context length.
    [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_count_tokens_with_tiktoken)
    for counting tokens.
    """

    presence_penalty: Optional[float]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on whether they appear in the text so
    far, increasing the model's likelihood to talk about new topics.

    [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)
    """

    seed: Optional[int]
    """
    If specified, our system will make a best effort to sample deterministically,
    such that repeated requests with the same `seed` and parameters should return
    the same result.

    Determinism is not guaranteed, and you should refer to the `system_fingerprint`
    response parameter to monitor changes in the backend.
    """

    stop: Union[Optional[str], List[str], None]
    """Up to 4 sequences where the API will stop generating further tokens.

    The returned text will not contain the stop sequence.
    """

    stream: Optional[bool]
    """Whether to stream back partial progress.

    If set, tokens will be sent as data-only
    [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
    as they become available, with the stream terminated by a `data: [DONE]`
    message.
    [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_stream_completions).
    """

    stream_options: Optional[StreamOptions]
    """Options for streaming response. Only set this when you set `stream: true`."""

    temperature: Optional[float]
    """What sampling temperature to use, between 0 and 2.

    Higher values like 0.8 will make the output more random, while lower values like
    0.2 will make it more focused and deterministic.

    We generally recommend altering this or `top_p` but not both.
    """

    top_p: Optional[float]
    """
    An alternative to sampling with temperature, called nucleus sampling, where the
    model considers the results of the tokens with top_p probability mass. So 0.1
    means only the tokens comprising the top 10% probability mass are considered.

    We generally recommend altering this or `temperature` but not both.
    """


class StreamOptions(TypedDict, total=False):
    include_usage: bool
    """If set, an additional chunk will be streamed before the `data: [DONE]` message.

    The `usage` field on this chunk shows the token usage statistics for the entire
    request, and the `choices` field will always be an empty array. All other chunks
    will also include a `usage` field, but with a null value.
    """

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "ChatCompletionCreateParams",
    "Message",
    "MessageChatCompletionRequestSystemMessage",
    "MessageChatCompletionRequestUserMessage",
    "MessageChatCompletionRequestUserMessageContentArrayOfContentPart",
    "MessageChatCompletionRequestAssistantMessage",
    "ResponseFormat",
    "StreamOptions",
]


class ChatCompletionCreateParams(TypedDict, total=False):
    messages: Required[Iterable[Message]]
    """A list of messages comprising the conversation so far.

    [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_format_inputs_to_chatgpt_models).
    """

    model: Required[Union[str, Literal["kilm-7b", "kilm-13b"]]]
    """ID of the model to use.

    See the
    [model endpoint compatibility](/docs/models/model-endpoint-compatibility) table
    for details on which models work with the Chat API.
    """
    
    frequency_penalty: Optional[float]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on their existing frequency in the
    text so far, decreasing the model's likelihood to repeat the same line verbatim.

    [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)
    """
    
    presence_penalty: Optional[float]
    """Number between -2.0 and 2.0.

    Positive values penalize new tokens based on whether they appear in the text so
    far, increasing the model's likelihood to talk about new topics.

    [See more information about frequency and presence penalties.](/docs/guides/text-generation/parameter-details)
    """

    logprobs: Optional[bool]
    """Whether to return log probabilities of the output tokens or not.

    If true, returns the log probabilities of each output token returned in the
    `content` of `message`.
    """

    max_tokens: Optional[int]
    """
    The maximum number of [tokens](/tokenizer) that can be generated in the chat
    completion.

    The total length of input tokens and generated tokens is limited by the model's
    context length.
    [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_count_tokens_with_tiktoken)
    for counting tokens.
    """

    response_format: ResponseFormat
    """An object specifying the format that the model must output.

    Compatible with [GPT-4 Turbo](/docs/models/gpt-4-and-gpt-4-turbo) and all
    GPT-3.5 Turbo models newer than `gpt-3.5-turbo-1106`.

    Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the
    message the model generates is valid JSON.

    **Important:** when using JSON mode, you **must** also instruct the model to
    produce JSON yourself via a system or user message. Without this, the model may
    generate an unending stream of whitespace until the generation reaches the token
    limit, resulting in a long-running and seemingly "stuck" request. Also note that
    the message content may be partially cut off if `finish_reason="length"`, which
    indicates the generation exceeded `max_tokens` or the conversation exceeded the
    max context length.
    """

    seed: Optional[int]
    """
    This feature is in Beta. If specified, our system will make a best effort to
    sample deterministically, such that repeated requests with the same `seed` and
    parameters should return the same result. Determinism is not guaranteed, and you
    should refer to the `system_fingerprint` response parameter to monitor changes
    in the backend.
    """

    stop: Union[Optional[str], List[str]]
    """Up to 4 sequences where the API will stop generating further tokens."""

    stream: Optional[bool]
    """If set, partial message deltas will be sent, like in ChatGPT.

    Tokens will be sent as data-only
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

    top_logprobs: Optional[int]
    """
    An integer between 0 and 20 specifying the number of most likely tokens to
    return at each token position, each with an associated log probability.
    `logprobs` must be set to `true` if this parameter is used.
    """

    top_p: Optional[float]
    """
    An alternative to sampling with temperature, called nucleus sampling, where the
    model considers the results of the tokens with top_p probability mass. So 0.1
    means only the tokens comprising the top 10% probability mass are considered.

    We generally recommend altering this or `temperature` but not both.
    """
    
    top_k: Optional[int]
    """An integer specifying the number of highest probability vocabulary tokens to keep
    for top-k-filtering.
    """
    
    beam_width: Optional[int]
    """An integer specifying the number of beams to use for beam search. Must be between 1 and 20.
    """
    
    repetition_penalty: Optional[float]
    """The parameter for repetition penalty. 1.0 means no penalty. See
    [this paper](https://arxiv.org/abs/1909.05858) for more details.
    """


class MessageChatCompletionRequestSystemMessage(TypedDict, total=False):
    content: Required[str]
    """The contents of the system message."""

    role: Required[Literal["system"]]
    """The role of the messages author, in this case `system`."""

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """


class MessageChatCompletionRequestUserMessageContentArrayOfContentPart(TypedDict, total=False):
    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
    """The type of the content part."""


class MessageChatCompletionRequestUserMessage(TypedDict, total=False):
    content: Required[Union[str, Iterable[MessageChatCompletionRequestUserMessageContentArrayOfContentPart]]]
    """The contents of the user message."""

    role: Required[Literal["user"]]
    """The role of the messages author, in this case `user`."""

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """


class MessageChatCompletionRequestAssistantMessage(TypedDict, total=False):
    role: Required[Literal["assistant"]]
    """The role of the messages author, in this case `assistant`."""

    content: Optional[str]
    """The contents of the assistant message.

    Required unless `tool_calls` or `function_call` is specified.
    """

    name: str
    """An optional name for the participant.

    Provides the model information to differentiate between participants of the same
    role.
    """


Message = Union[
    MessageChatCompletionRequestSystemMessage,
    MessageChatCompletionRequestUserMessage,
    MessageChatCompletionRequestAssistantMessage,
]


class ResponseFormat(TypedDict, total=False):
    type: Literal["text", "json_object"]
    """Must be one of `text` or `json_object`."""


class StreamOptions(TypedDict, total=False):
    include_usage: bool
    """If set, an additional chunk will be streamed before the `data: [DONE]` message.

    The `usage` field on this chunk shows the token usage statistics for the entire
    request, and the `choices` field will always be an empty array. All other chunks
    will also include a `usage` field, but with a null value.
    """

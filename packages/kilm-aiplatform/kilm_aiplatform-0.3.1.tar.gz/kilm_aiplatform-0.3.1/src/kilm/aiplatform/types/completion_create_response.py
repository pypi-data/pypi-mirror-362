# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "CompletionCreateResponse",
    "Choice",
    "ChoiceLogprobs",
    "ChoiceLogprobsContent",
    "ChoiceLogprobsContentTopLogprob",
    "Usage",
]


class ChoiceLogprobsContentTopLogprob(BaseModel):
    token: str
    """The token."""

    logprob: float
    """The log probability of this token, if it is within the top 20 most likely
    tokens.

    Otherwise, the value `-9999.0` is used to signify that the token is very
    unlikely.
    """


class ChoiceLogprobsContent(BaseModel):
    token: str
    """The token."""

    logprob: float
    """The log probability of this token, if it is within the top 20 most likely
    tokens.

    Otherwise, the value `-9999.0` is used to signify that the token is very
    unlikely.
    """

    top_logprobs: List[ChoiceLogprobsContentTopLogprob]
    """List of the most likely tokens and their log probability, at this token
    position.

    In rare cases, there may be fewer than the number of requested `top_logprobs`
    returned.
    """


class ChoiceLogprobs(BaseModel):
    content: Optional[List[ChoiceLogprobsContent]] = None
    """A list of message content tokens with log probability information."""


class Choice(BaseModel):
    finish_reason: Literal["stop", "length", "content_filter"]
    """The reason the model stopped generating tokens.

    This will be `stop` if the model hit a natural stop point or a provided stop
    sequence, `length` if the maximum number of tokens specified in the request was
    reached, or `content_filter` if content was omitted due to a flag from our
    content filters.
    """

    index: int

    logprobs: Optional[ChoiceLogprobs] = None
    """Log probability information for the choice."""

    text: str


class Usage(BaseModel):
    completion_tokens: int
    """Number of tokens in the generated completion."""

    prompt_tokens: int
    """Number of tokens in the prompt."""

    total_tokens: int
    """Total number of tokens used in the request (prompt + completion)."""


class CompletionCreateResponse(BaseModel):
    id: str
    """A unique identifier for the completion."""

    choices: List[Choice]
    """The list of completion choices the model generated for the input prompt."""

    created: int
    """The Unix timestamp (in seconds) of when the completion was created."""

    model: str
    """The model used for completion."""

    object: Literal["text_completion"]
    """The object type, which is always "text_completion" """

    system_fingerprint: Optional[str] = None
    """This fingerprint represents the backend configuration that the model runs with.

    Can be used in conjunction with the `seed` request parameter to understand when
    backend changes have been made that might impact determinism.
    """

    usage: Optional[Usage] = None
    """Usage statistics for the completion request."""

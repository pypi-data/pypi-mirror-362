# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["GenerationCreateResponse", "Data"]


class Data(BaseModel):
    b64_json: Optional[str] = None
    """
    The base64-encoded JSON of the generated image, if `response_format` is
    `b64_json`.
    """

    revised_prompt: Optional[str] = None
    """
    The prompt that was used to generate the image, if there was any revision to the
    prompt.
    """

    url: Optional[str] = None
    """The URL of the generated image, if `response_format` is `url` (default)."""


class GenerationCreateResponse(BaseModel):
    created: int

    data: List[Data]

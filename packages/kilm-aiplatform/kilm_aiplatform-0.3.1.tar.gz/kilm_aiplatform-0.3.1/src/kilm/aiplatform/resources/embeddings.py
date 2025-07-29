# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal

import httpx

from ..types import embedding_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
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
from .._base_client import (
    make_request_options,
)
from ..types.embedding_create_response import EmbeddingCreateResponse

__all__ = ["EmbeddingsResource", "AsyncEmbeddingsResource"]


class EmbeddingsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EmbeddingsResourceWithRawResponse:
        return EmbeddingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EmbeddingsResourceWithStreamingResponse:
        return EmbeddingsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        input: Union[str, List[str], Iterable[int], Iterable[Iterable[int]]],
        model: Union[str, Literal["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"]],
        dimensions: int | NotGiven = NOT_GIVEN,
        encoding_format: Literal["float", "base64"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EmbeddingCreateResponse:
        """
        Creates an embedding vector representing the input text.

        Args:
          input: Input text to embed, encoded as a string or array of tokens. To embed multiple
              inputs in a single request, pass an array of strings or array of token arrays.
              The input must not exceed the max input tokens for the model (8192 tokens for
              `text-embedding-ada-002`), cannot be an empty string, and any array must be 2048
              dimensions or less.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_count_tokens_with_tiktoken)
              for counting tokens.

          model: ID of the model to use. You can use the
              [List models](/docs/api-reference/models/list) API to see all of your available
              models, or see our [Model overview](/docs/models/overview) for descriptions of
              them.

          dimensions: The number of dimensions the resulting output embeddings should have. Only
              supported in `text-embedding-3` and later models.

          encoding_format: The format to return the embeddings in. Can be either `float` or
              [`base64`](https://pypi.org/project/pybase64/).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/embeddings/",
            body=maybe_transform(
                {
                    "input": input,
                    "model": model,
                    "dimensions": dimensions,
                    "encoding_format": encoding_format,
                },
                embedding_create_params.EmbeddingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmbeddingCreateResponse,
        )


class AsyncEmbeddingsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEmbeddingsResourceWithRawResponse:
        return AsyncEmbeddingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEmbeddingsResourceWithStreamingResponse:
        return AsyncEmbeddingsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        input: Union[str, List[str], Iterable[int], Iterable[Iterable[int]]],
        model: Union[str, Literal["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"]],
        dimensions: int | NotGiven = NOT_GIVEN,
        encoding_format: Literal["float", "base64"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EmbeddingCreateResponse:
        """
        Creates an embedding vector representing the input text.

        Args:
          input: Input text to embed, encoded as a string or array of tokens. To embed multiple
              inputs in a single request, pass an array of strings or array of token arrays.
              The input must not exceed the max input tokens for the model (8192 tokens for
              `text-embedding-ada-002`), cannot be an empty string, and any array must be 2048
              dimensions or less.
              [Example Python code](https://cookbook.api-gateway.kilm.zalo.services/examples/how_to_count_tokens_with_tiktoken)
              for counting tokens.

          model: ID of the model to use. You can use the
              [List models](/docs/api-reference/models/list) API to see all of your available
              models, or see our [Model overview](/docs/models/overview) for descriptions of
              them.

          dimensions: The number of dimensions the resulting output embeddings should have. Only
              supported in `text-embedding-3` and later models.

          encoding_format: The format to return the embeddings in. Can be either `float` or
              [`base64`](https://pypi.org/project/pybase64/).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/embeddings/",
            body=await async_maybe_transform(
                {
                    "input": input,
                    "model": model,
                    "dimensions": dimensions,
                    "encoding_format": encoding_format,
                },
                embedding_create_params.EmbeddingCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EmbeddingCreateResponse,
        )


class EmbeddingsResourceWithRawResponse:
    def __init__(self, embeddings: EmbeddingsResource) -> None:
        self._embeddings = embeddings

        self.create = to_raw_response_wrapper(
            embeddings.create,
        )


class AsyncEmbeddingsResourceWithRawResponse:
    def __init__(self, embeddings: AsyncEmbeddingsResource) -> None:
        self._embeddings = embeddings

        self.create = async_to_raw_response_wrapper(
            embeddings.create,
        )


class EmbeddingsResourceWithStreamingResponse:
    def __init__(self, embeddings: EmbeddingsResource) -> None:
        self._embeddings = embeddings

        self.create = to_streamed_response_wrapper(
            embeddings.create,
        )


class AsyncEmbeddingsResourceWithStreamingResponse:
    def __init__(self, embeddings: AsyncEmbeddingsResource) -> None:
        self._embeddings = embeddings

        self.create = async_to_streamed_response_wrapper(
            embeddings.create,
        )

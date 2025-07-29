# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import resources, _exceptions
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
from ._utils import (
    is_given,
    get_async_library,
)
from .version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError, AIPlatformError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "AIPlatform",
    "AsyncAIPlatform",
    "Client",
    "AsyncClient",
]


class AIPlatform(SyncAPIClient):
    chat_completions: resources.ChatCompletionsResource
    completions: resources.CompletionsResource
    images: resources.ImagesResource
    embeddings: resources.EmbeddingsResource
    models: resources.ModelsResource
    moderations: resources.ModerationsResource
    with_raw_response: AIPlatformWithRawResponse
    with_streaming_response: AIPlatformWithStreamedResponse

    # client options
    access_key: str
    access_secret_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        access_key: str | None = None,
        access_secret_key: str | None = None,
        base_url: str | httpx.URL | None = None,
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
        """Construct a new synchronous ai-platform client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `access_key` from `AI_PLATFORM_ACCESS_KEY`
        - `access_secret_key` from `AI_PLATFORM_ACCESS_SECRET_KEY`
        """
        self._use_api_key = False
        if api_key is None:
            api_key = os.environ.get("KILM_API_KEY")
        if api_key is not None:
            self._use_api_key = True
            self.api_key = api_key
        else:
            if access_key is None:
                access_key = os.environ.get("AI_PLATFORM_ACCESS_KEY")
            if access_key is None:
                raise AIPlatformError(
                    "The access_key client option must be set either by passing access_key to the client or by setting the AI_PLATFORM_ACCESS_KEY environment variable"
                )
            self.access_key = access_key

            if access_secret_key is None:
                access_secret_key = os.environ.get("AI_PLATFORM_ACCESS_SECRET_KEY")
            if access_secret_key is None:
                raise AIPlatformError(
                    "The access_secret_key client option must be set either by passing access_secret_key to the client or by setting the AI_PLATFORM_ACCESS_SECRET_KEY environment variable"
                )
            self.access_secret_key = access_secret_key

        if base_url is None:
            base_url = os.environ.get("AI_PLATFORM_BASE_URL")
        if base_url is None:
            base_url = f"https://kiki.zalo.ai/platform/api/v1"

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

        self.chat_completions = resources.ChatCompletionsResource(self)
        self.completions = resources.CompletionsResource(self)
        self.images = resources.ImagesResource(self)
        self.embeddings = resources.EmbeddingsResource(self)
        self.models = resources.ModelsResource(self)
        self.moderations = resources.ModerationsResource(self)
        self.with_raw_response = AIPlatformWithRawResponse(self)
        self.with_streaming_response = AIPlatformWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        if self._use_api_key:
            return {
                "Authorization": f"Bearer {self.api_key}",
            }
        return {
            "KILM-ACCESS-KEY": self.access_key,
            "KILM-ACCESS-SECRET-KEY": self.access_secret_key,
        }

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        access_key: str | None = None,
        access_secret_key: str | None = None,
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
            access_key=access_key or self.access_key,
            access_secret_key=access_secret_key or self.access_secret_key,
            base_url=base_url or self.base_url,
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


class AsyncAIPlatform(AsyncAPIClient):
    chat_completions: resources.AsyncChatCompletionsResource
    completions: resources.AsyncCompletionsResource
    images: resources.AsyncImagesResource
    embeddings: resources.AsyncEmbeddingsResource
    models: resources.AsyncModelsResource
    moderations: resources.AsyncModerationsResource
    with_raw_response: AsyncAIPlatformWithRawResponse
    with_streaming_response: AsyncAIPlatformWithStreamedResponse

    # client options
    access_key: str
    access_secret_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        access_key: str | None = None,
        access_secret_key: str | None = None,
        base_url: str | httpx.URL | None = None,
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
        """Construct a new async ai-platform client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `access_key` from `AI_PLATFORM_ACCESS_KEY`
        - `access_secret_key` from `AI_PLATFORM_ACCESS_SECRET_KEY`
        """
        self._use_api_key = False
        if api_key is None:
            api_key = os.environ.get("KILM_API_KEY")
        if api_key is not None:
            self._use_api_key = True
            self.api_key = api_key
        else:
            if access_key is None:
                access_key = os.environ.get("AI_PLATFORM_ACCESS_KEY")
            if access_key is None:
                raise AIPlatformError(
                    "The access_key client option must be set either by passing access_key to the client or by setting the AI_PLATFORM_ACCESS_KEY environment variable"
                )
            self.access_key = access_key

            if access_secret_key is None:
                access_secret_key = os.environ.get("AI_PLATFORM_ACCESS_SECRET_KEY")
            if access_secret_key is None:
                raise AIPlatformError(
                    "The access_secret_key client option must be set either by passing access_secret_key to the client or by setting the AI_PLATFORM_ACCESS_SECRET_KEY environment variable"
                )
            self.access_secret_key = access_secret_key

        if base_url is None:
            base_url = os.environ.get("AI_PLATFORM_BASE_URL")
        if base_url is None:
            base_url = f"https://kiki.zalo.ai/platform/api/v1"

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

        self.chat_completions = resources.AsyncChatCompletionsResource(self)
        self.completions = resources.AsyncCompletionsResource(self)
        self.images = resources.AsyncImagesResource(self)
        self.embeddings = resources.AsyncEmbeddingsResource(self)
        self.models = resources.AsyncModelsResource(self)
        self.moderations = resources.AsyncModerationsResource(self)
        self.with_raw_response = AsyncAIPlatformWithRawResponse(self)
        self.with_streaming_response = AsyncAIPlatformWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        if self._use_api_key:
            return {
                "Authorization": f"Bearer {self.api_key}",
            }
        return {
            "KILM-ACCESS-KEY": self.access_key,
            "KILM-ACCESS-SECRET-KEY": self.access_secret_key,
        }
        
    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        access_key: str | None = None,
        access_secret_key: str | None = None,
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
            access_key=access_key or self.access_key,
            access_secret_key=access_secret_key or self.access_secret_key,
            base_url=base_url or self.base_url,
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


class AIPlatformWithRawResponse:
    def __init__(self, client: AIPlatform) -> None:
        self.chat_completions = resources.ChatCompletionsResourceWithRawResponse(client.chat_completions)
        self.completions = resources.CompletionsResourceWithRawResponse(client.completions)
        self.images = resources.ImagesResourceWithRawResponse(client.images)
        self.embeddings = resources.EmbeddingsResourceWithRawResponse(client.embeddings)
        self.models = resources.ModelsResourceWithRawResponse(client.models)
        self.moderations = resources.ModerationsResourceWithRawResponse(client.moderations)


class AsyncAIPlatformWithRawResponse:
    def __init__(self, client: AsyncAIPlatform) -> None:
        self.chat_completions = resources.AsyncChatCompletionsResourceWithRawResponse(client.chat_completions)
        self.completions = resources.AsyncCompletionsResourceWithRawResponse(client.completions)
        self.images = resources.AsyncImagesResourceWithRawResponse(client.images)
        self.embeddings = resources.AsyncEmbeddingsResourceWithRawResponse(client.embeddings)
        self.models = resources.AsyncModelsResourceWithRawResponse(client.models)
        self.moderations = resources.AsyncModerationsResourceWithRawResponse(client.moderations)


class AIPlatformWithStreamedResponse:
    def __init__(self, client: AIPlatform) -> None:
        self.chat_completions = resources.ChatCompletionsResourceWithStreamingResponse(client.chat_completions)
        self.completions = resources.CompletionsResourceWithStreamingResponse(client.completions)
        self.images = resources.ImagesResourceWithStreamingResponse(client.images)
        self.embeddings = resources.EmbeddingsResourceWithStreamingResponse(client.embeddings)
        self.models = resources.ModelsResourceWithStreamingResponse(client.models)
        self.moderations = resources.ModerationsResourceWithStreamingResponse(client.moderations)


class AsyncAIPlatformWithStreamedResponse:
    def __init__(self, client: AsyncAIPlatform) -> None:
        self.chat_completions = resources.AsyncChatCompletionsResourceWithStreamingResponse(client.chat_completions)
        self.completions = resources.AsyncCompletionsResourceWithStreamingResponse(client.completions)
        self.images = resources.AsyncImagesResourceWithStreamingResponse(client.images)
        self.embeddings = resources.AsyncEmbeddingsResourceWithStreamingResponse(client.embeddings)
        self.models = resources.AsyncModelsResourceWithStreamingResponse(client.models)
        self.moderations = resources.AsyncModerationsResourceWithStreamingResponse(client.moderations)


Client = AIPlatform

AsyncClient = AsyncAIPlatform

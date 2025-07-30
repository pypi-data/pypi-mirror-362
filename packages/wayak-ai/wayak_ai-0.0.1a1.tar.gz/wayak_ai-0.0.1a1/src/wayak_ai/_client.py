# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

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
from .resources import files, agents, brains, threads, messages
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import WayakAIError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.users import users
from .resources.ontology import ontology
from .resources.projects import projects
from .resources.organizations import organizations

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "WayakAI", "AsyncWayakAI", "Client", "AsyncClient"]


class WayakAI(SyncAPIClient):
    users: users.UsersResource
    files: files.FilesResource
    projects: projects.ProjectsResource
    threads: threads.ThreadsResource
    brains: brains.BrainsResource
    messages: messages.MessagesResource
    agents: agents.AgentsResource
    organizations: organizations.OrganizationsResource
    ontology: ontology.OntologyResource
    with_raw_response: WayakAIWithRawResponse
    with_streaming_response: WayakAIWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
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
        """Construct a new synchronous WayakAI client instance.

        This automatically infers the `api_key` argument from the `WAYAK_AI_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("WAYAK_AI_API_KEY")
        if api_key is None:
            raise WayakAIError(
                "The api_key client option must be set either by passing api_key to the client or by setting the WAYAK_AI_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("WAYAK_AI_BASE_URL")
        if base_url is None:
            base_url = f"https://api.example.com"

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

        self.users = users.UsersResource(self)
        self.files = files.FilesResource(self)
        self.projects = projects.ProjectsResource(self)
        self.threads = threads.ThreadsResource(self)
        self.brains = brains.BrainsResource(self)
        self.messages = messages.MessagesResource(self)
        self.agents = agents.AgentsResource(self)
        self.organizations = organizations.OrganizationsResource(self)
        self.ontology = ontology.OntologyResource(self)
        self.with_raw_response = WayakAIWithRawResponse(self)
        self.with_streaming_response = WayakAIWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

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
        api_key: str | None = None,
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


class AsyncWayakAI(AsyncAPIClient):
    users: users.AsyncUsersResource
    files: files.AsyncFilesResource
    projects: projects.AsyncProjectsResource
    threads: threads.AsyncThreadsResource
    brains: brains.AsyncBrainsResource
    messages: messages.AsyncMessagesResource
    agents: agents.AsyncAgentsResource
    organizations: organizations.AsyncOrganizationsResource
    ontology: ontology.AsyncOntologyResource
    with_raw_response: AsyncWayakAIWithRawResponse
    with_streaming_response: AsyncWayakAIWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
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
        """Construct a new async AsyncWayakAI client instance.

        This automatically infers the `api_key` argument from the `WAYAK_AI_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("WAYAK_AI_API_KEY")
        if api_key is None:
            raise WayakAIError(
                "The api_key client option must be set either by passing api_key to the client or by setting the WAYAK_AI_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("WAYAK_AI_BASE_URL")
        if base_url is None:
            base_url = f"https://api.example.com"

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

        self.users = users.AsyncUsersResource(self)
        self.files = files.AsyncFilesResource(self)
        self.projects = projects.AsyncProjectsResource(self)
        self.threads = threads.AsyncThreadsResource(self)
        self.brains = brains.AsyncBrainsResource(self)
        self.messages = messages.AsyncMessagesResource(self)
        self.agents = agents.AsyncAgentsResource(self)
        self.organizations = organizations.AsyncOrganizationsResource(self)
        self.ontology = ontology.AsyncOntologyResource(self)
        self.with_raw_response = AsyncWayakAIWithRawResponse(self)
        self.with_streaming_response = AsyncWayakAIWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

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
        api_key: str | None = None,
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


class WayakAIWithRawResponse:
    def __init__(self, client: WayakAI) -> None:
        self.users = users.UsersResourceWithRawResponse(client.users)
        self.files = files.FilesResourceWithRawResponse(client.files)
        self.projects = projects.ProjectsResourceWithRawResponse(client.projects)
        self.threads = threads.ThreadsResourceWithRawResponse(client.threads)
        self.brains = brains.BrainsResourceWithRawResponse(client.brains)
        self.messages = messages.MessagesResourceWithRawResponse(client.messages)
        self.agents = agents.AgentsResourceWithRawResponse(client.agents)
        self.organizations = organizations.OrganizationsResourceWithRawResponse(client.organizations)
        self.ontology = ontology.OntologyResourceWithRawResponse(client.ontology)


class AsyncWayakAIWithRawResponse:
    def __init__(self, client: AsyncWayakAI) -> None:
        self.users = users.AsyncUsersResourceWithRawResponse(client.users)
        self.files = files.AsyncFilesResourceWithRawResponse(client.files)
        self.projects = projects.AsyncProjectsResourceWithRawResponse(client.projects)
        self.threads = threads.AsyncThreadsResourceWithRawResponse(client.threads)
        self.brains = brains.AsyncBrainsResourceWithRawResponse(client.brains)
        self.messages = messages.AsyncMessagesResourceWithRawResponse(client.messages)
        self.agents = agents.AsyncAgentsResourceWithRawResponse(client.agents)
        self.organizations = organizations.AsyncOrganizationsResourceWithRawResponse(client.organizations)
        self.ontology = ontology.AsyncOntologyResourceWithRawResponse(client.ontology)


class WayakAIWithStreamedResponse:
    def __init__(self, client: WayakAI) -> None:
        self.users = users.UsersResourceWithStreamingResponse(client.users)
        self.files = files.FilesResourceWithStreamingResponse(client.files)
        self.projects = projects.ProjectsResourceWithStreamingResponse(client.projects)
        self.threads = threads.ThreadsResourceWithStreamingResponse(client.threads)
        self.brains = brains.BrainsResourceWithStreamingResponse(client.brains)
        self.messages = messages.MessagesResourceWithStreamingResponse(client.messages)
        self.agents = agents.AgentsResourceWithStreamingResponse(client.agents)
        self.organizations = organizations.OrganizationsResourceWithStreamingResponse(client.organizations)
        self.ontology = ontology.OntologyResourceWithStreamingResponse(client.ontology)


class AsyncWayakAIWithStreamedResponse:
    def __init__(self, client: AsyncWayakAI) -> None:
        self.users = users.AsyncUsersResourceWithStreamingResponse(client.users)
        self.files = files.AsyncFilesResourceWithStreamingResponse(client.files)
        self.projects = projects.AsyncProjectsResourceWithStreamingResponse(client.projects)
        self.threads = threads.AsyncThreadsResourceWithStreamingResponse(client.threads)
        self.brains = brains.AsyncBrainsResourceWithStreamingResponse(client.brains)
        self.messages = messages.AsyncMessagesResourceWithStreamingResponse(client.messages)
        self.agents = agents.AsyncAgentsResourceWithStreamingResponse(client.agents)
        self.organizations = organizations.AsyncOrganizationsResourceWithStreamingResponse(client.organizations)
        self.ontology = ontology.AsyncOntologyResourceWithStreamingResponse(client.ontology)


Client = WayakAI

AsyncClient = AsyncWayakAI

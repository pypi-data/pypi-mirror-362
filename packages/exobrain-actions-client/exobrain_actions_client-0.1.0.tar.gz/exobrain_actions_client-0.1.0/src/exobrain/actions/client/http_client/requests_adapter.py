"""
Requests client adapter implementation
"""
# mypy: ignore-errors

import typing as t

import requests
from exobrain.actions.client.http_client.interfaces import (
    HTTPClientFacade,
    HTTPRequest,
    HTTPResponse,
)

__all__ = ["RequestsRequestAdapter", "RequestsResponseAdapter", "RequestsClientAdapter"]


class RequestsRequestAdapter(HTTPRequest):
    """Requests request wrapper"""

    def __init__(self, request: requests.PreparedRequest):
        self._request = request

    @property
    def method(self) -> str:
        return self._request.method or ""

    @property
    def url(self) -> str:
        return self._request.url or ""

    @property
    def headers(self) -> t.Mapping[str, str]:
        return dict(self._request.headers or {})

    @property
    def content(self) -> bytes | None:
        return t.cast(bytes | None, self._request.body)


class RequestsResponseAdapter(HTTPResponse):
    """Requests response wrapper"""

    def __init__(self, response: requests.Response):
        self._response = response

    @property
    def request(self) -> RequestsRequestAdapter:
        return RequestsRequestAdapter(self._response.request)

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def headers(self) -> t.Mapping[str, str]:
        return dict(self._response.headers)

    @property
    def content(self) -> bytes:
        return self._response.content

    @property
    def text(self) -> str:
        return self._response.text

    def json(self) -> t.Any:
        return self._response.json()


class RequestsClientAdapter(HTTPClientFacade):
    """Requests session client implementation"""

    client: requests.Session

    def __init__(
        self,
        client: requests.Session,
        *,
        base_url: str = "",
        **kwargs: t.Any,
    ):
        super().__init__(client)
        self._base_url = base_url
        self._kwargs = kwargs

    def _build_url(self, url: str) -> str:
        if not self._base_url or url.startswith(("http://", "https://")):
            return url
        return f"{self._base_url.rstrip('/')}/{url.lstrip('/')}"

    def get(self, url: str, **kwargs: t.Any) -> RequestsResponseAdapter:
        kwargs.update({**self._kwargs, **kwargs})
        response = self.client.get(self._build_url(url), **kwargs)
        return RequestsResponseAdapter(response)

    def post(self, url: str, **kwargs: t.Any) -> RequestsResponseAdapter:
        kwargs.update({**self._kwargs, **kwargs})
        response = self.client.post(self._build_url(url), **kwargs)
        return RequestsResponseAdapter(response)

    def put(self, url: str, **kwargs: t.Any) -> RequestsResponseAdapter:
        kwargs.update({**self._kwargs, **kwargs})
        response = self.client.put(self._build_url(url), **kwargs)
        return RequestsResponseAdapter(response)

    def patch(self, url: str, **kwargs: t.Any) -> RequestsResponseAdapter:
        kwargs.update({**self._kwargs, **kwargs})
        response = self.client.patch(self._build_url(url), **kwargs)
        return RequestsResponseAdapter(response)

    def delete(self, url: str, **kwargs: t.Any) -> RequestsResponseAdapter:
        kwargs.update({**self._kwargs, **kwargs})
        response = self.client.delete(self._build_url(url), **kwargs)
        return RequestsResponseAdapter(response)

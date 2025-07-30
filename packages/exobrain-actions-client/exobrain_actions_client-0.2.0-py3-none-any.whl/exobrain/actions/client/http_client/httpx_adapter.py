"""
HTTPX client adapter implementation
"""
# mypy: ignore-errors

import typing as t

import httpx
from exobrain.actions.client.http_client.interfaces import (
    HTTPClientFacade,
    HTTPRequest,
    HTTPResponse,
)

__all__ = ["HTTPXRequestAdapter", "HTTPXResponseAdapter", "HTTPXClientAdapter"]


class HTTPXRequestAdapter(HTTPRequest):
    """HTTPX request wrapper"""

    def __init__(self, request: httpx.Request):
        self._request = request

    @property
    def method(self) -> str:
        return self._request.method

    @property
    def url(self) -> str:
        return str(self._request.url)

    @property
    def headers(self) -> t.Mapping[str, str]:
        return dict(self._request.headers)

    @property
    def content(self) -> bytes | None:
        return self._request.content


class HTTPXResponseAdapter(HTTPResponse):
    """HTTPX response wrapper"""

    def __init__(self, response: httpx.Response):
        self._response = response

    @property
    def request(self) -> HTTPXRequestAdapter:
        return HTTPXRequestAdapter(self._response.request)

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


class HTTPXClientAdapter(HTTPClientFacade):
    """HTTPX client implementation"""

    client: httpx.Client

    def __init__(self, client: httpx.Client):
        super().__init__(client)

    def get(self, url: str, **kwargs: t.Any) -> HTTPXResponseAdapter:
        response = self.client.get(url, **kwargs)
        return HTTPXResponseAdapter(response)

    def post(self, url: str, **kwargs: t.Any) -> HTTPXResponseAdapter:
        response = self.client.post(url, **kwargs)
        return HTTPXResponseAdapter(response)

    def put(self, url: str, **kwargs: t.Any) -> HTTPXResponseAdapter:
        response = self.client.put(url, **kwargs)
        return HTTPXResponseAdapter(response)

    def patch(self, url: str, **kwargs: t.Any) -> HTTPXResponseAdapter:
        response = self.client.patch(url, **kwargs)
        return HTTPXResponseAdapter(response)

    def delete(self, url: str, **kwargs: t.Any) -> HTTPXResponseAdapter:
        response = self.client.delete(url, **kwargs)
        return HTTPXResponseAdapter(response)

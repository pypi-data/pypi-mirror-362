"""
Flask test client adapter implementation
"""
# mypy: ignore-errors

import typing as t

from exobrain.actions.client.http_client.interfaces import (
    HTTPClientFacade,
    HTTPRequest,
    HTTPResponse,
)
from flask.testing import FlaskClient
from werkzeug.test import TestResponse

__all__ = ["FlaskRequestAdapter", "FlaskResponseAdapter", "FlaskClientAdapter"]


class FlaskRequestAdapter(HTTPRequest):
    """Flask request wrapper (limited support)"""

    def __init__(
        self,
        method: str,
        url: str,
        headers: t.Mapping[str, str] | None = None,
        content: bytes | None = None,
    ):
        self._method = method
        self._url = url
        self._headers = headers or {}
        self._content = content

    @property
    def method(self) -> str:
        return self._method

    @property
    def url(self) -> str:
        return self._url

    @property
    def headers(self) -> t.Mapping[str, str]:
        return self._headers

    @property
    def content(self) -> bytes | None:
        return self._content


class FlaskResponseAdapter(HTTPResponse):
    """Flask test client response wrapper"""

    def __init__(self, response: TestResponse, method: str = "GET"):
        self._response = response
        self._method = method

    @property
    def request(self) -> FlaskRequestAdapter:
        # Flask's test client does not provide a direct request object,
        # so we create a minimal request representation.
        return FlaskRequestAdapter(
            method=self._method,
            url=self._response.request.path,
            headers=dict(self._response.headers),
            content=self._response.get_data(),
        )

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def headers(self) -> t.Mapping[str, str]:
        return dict(self._response.headers)

    @property
    def content(self) -> bytes:
        return self._response.get_data()

    @property
    def text(self) -> str:
        return self._response.get_data(as_text=True)

    def json(self) -> t.Any:
        return self._response.get_json()


class FlaskClientAdapter(HTTPClientFacade):
    """Flask test client implementation"""

    client: FlaskClient

    def __init__(self, client: FlaskClient):
        super().__init__(client)

    def get(self, url: str, **kwargs: t.Any) -> FlaskResponseAdapter:
        response = self.client.get(url, **kwargs)
        return FlaskResponseAdapter(response, method="get")

    def post(self, url: str, **kwargs: t.Any) -> FlaskResponseAdapter:
        response = self.client.post(url, **kwargs)
        return FlaskResponseAdapter(response, method="post")

    def put(self, url: str, **kwargs: t.Any) -> FlaskResponseAdapter:
        response = self.client.put(url, **kwargs)
        return FlaskResponseAdapter(response, method="put")

    def patch(self, url: str, **kwargs: t.Any) -> FlaskResponseAdapter:
        response = self.client.patch(url, **kwargs)
        return FlaskResponseAdapter(response, method="patch")

    def delete(self, url: str, **kwargs: t.Any) -> FlaskResponseAdapter:
        response = self.client.delete(url, **kwargs)
        return FlaskResponseAdapter(response, method="delete")

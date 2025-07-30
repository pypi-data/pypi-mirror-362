"""
Core interfaces for HTTP client facade
"""

import typing as t
from abc import ABC, abstractmethod

from exobrain.actions.client.http_client.exceptions import HTTPClientError

__all__ = ["HTTPClientFacade", "HTTPRequest", "HTTPResponse", "HTTPStatusError"]


STATUS_CLIENT_ERROR = 400
STATUS_ERROR = 600


class HTTPStatusError(HTTPClientError):
    """
    The response had an error HTTP status of 4xx or 5xx.
    """

    def __init__(self, message: str, *, request: "HTTPRequest", response: "HTTPResponse") -> None:
        super().__init__(message)
        self.request = request
        self.response = response


class HTTPRequest(ABC):
    """Common interface for HTTP request objects"""

    @property
    @abstractmethod
    def method(self) -> str:
        """HTTP method"""

    @property
    @abstractmethod
    def url(self) -> str:
        """Request URL"""

    @property
    @abstractmethod
    def headers(self) -> t.Mapping[str, str]:
        """Request headers"""

    @property
    @abstractmethod
    def content(self) -> bytes | None:
        """Request body content"""


class HTTPResponse(ABC):
    """Common interface for HTTP response objects"""

    @property
    @abstractmethod
    def request(self) -> HTTPRequest:
        """The request that generated this response"""

    @property
    @abstractmethod
    def status_code(self) -> int:
        """HTTP status code"""

    @property
    @abstractmethod
    def headers(self) -> t.Mapping[str, str]:
        """Response headers"""

    @property
    @abstractmethod
    def content(self) -> bytes:
        """Response body as bytes"""

    @property
    @abstractmethod
    def text(self) -> str:
        """Response body as text"""

    @abstractmethod
    def json(self) -> t.Any:
        """Parse response body as JSON"""

    def raise_for_status(self) -> None:
        """
        Check the response status code and raises an exception if it's an error.

        Raises:
            HTTPStatusError: If the status code indicates a client or server error (4xx or 5xx).
        """
        import json

        if STATUS_CLIENT_ERROR <= self.status_code < STATUS_ERROR:
            error_message = f"HTTP Error {self.status_code} for url: {self.request.url}"

            try:
                error_detail = self.json()
                error_message += f"\nResponse JSON: {json.dumps(error_detail, indent=2)}"
            except (json.JSONDecodeError, ValueError):
                error_message += f"\nResponse Text: {self.text}"

            raise HTTPStatusError(error_message, request=self.request, response=self)


class HTTPClientFacade(ABC):
    """Common interface for HTTP clients with context manager support"""

    def __init__(self, client: t.Any):
        self.client = client

    @abstractmethod
    def get(
        self,
        url: str,
        *,
        params: t.Mapping[str, t.Any] | None = None,
        headers: t.Mapping[str, str] | None = None,
        cookies: t.Mapping[str, str] | None = None,
        follow_redirects: bool = True,
        timeout: float | None = None,
    ) -> HTTPResponse:
        """Perform a GET request to the specified URL."""

    @abstractmethod
    def post(
        self,
        url: str,
        *,
        data: t.Any = None,
        json: t.Any = None,
        params: t.Mapping[str, t.Any] | None = None,
        headers: t.Mapping[str, str] | None = None,
        cookies: t.Mapping[str, str] | None = None,
        files: t.Mapping[str, t.Any] | None = None,
        follow_redirects: bool = True,
        timeout: float | None = None,
    ) -> HTTPResponse:
        """Perform a POST request to the specified URL."""

    @abstractmethod
    def put(
        self,
        url: str,
        *,
        data: t.Any = None,
        json: t.Any = None,
        params: t.Mapping[str, t.Any] | None = None,
        headers: t.Mapping[str, str] | None = None,
        cookies: t.Mapping[str, str] | None = None,
        files: t.Mapping[str, t.Any] | None = None,
        follow_redirects: bool = True,
        timeout: float | None = None,
    ) -> HTTPResponse:
        """Perform a PUT request to the specified URL."""

    @abstractmethod
    def patch(
        self,
        url: str,
        *,
        data: t.Any = None,
        json: t.Any = None,
        params: t.Mapping[str, t.Any] | None = None,
        headers: t.Mapping[str, str] | None = None,
        cookies: t.Mapping[str, str] | None = None,
        files: t.Mapping[str, t.Any] | None = None,
        follow_redirects: bool = True,
        timeout: float | None = None,
    ) -> HTTPResponse:
        """Perform a PATCH request to the specified URL."""

    @abstractmethod
    def delete(
        self,
        url: str,
        *,
        params: t.Mapping[str, t.Any] | None = None,
        headers: t.Mapping[str, str] | None = None,
        cookies: t.Mapping[str, str] | None = None,
        follow_redirects: bool = True,
        timeout: float | None = None,
    ) -> HTTPResponse:
        """Perform a DELETE request to the specified URL."""

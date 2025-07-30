"""
HTTP client factory module for creating different types of HTTP clients (HTTPX, Requests, Flask).

Example:
    Creating a requests client with custom configuration:

    >>> from exobrain.actions.client.http_client import ClientType, create_client
    >>> client = create_client(
    ...     ClientType.REQUESTS,
    ...     base_url="https://api.example.com",
    ...     timeout=30,
    ...     verify=True,
    ... )
    >>> response = client.get("/users")
    >>> users = response.json()

    Creating a Flask test client:

    >>> from flask import Flask
    >>> app = Flask(__name__)
    >>> client = create_client(ClientType.FLASK, app=app)
    >>> response = client.get("/health")
    >>> assert response.status_code == 200
"""

# mypy: ignore-errors
import enum
import typing as t

from exobrain.actions.client.http_client.exceptions import HTTPClientError

if t.TYPE_CHECKING:
    from exobrain.actions.client.http_client.interfaces import HTTPClientFacade


class ClientType(enum.StrEnum):
    HTTPX = "httpx"
    REQUESTS = "requests"
    FLASK = "flask"


class ClientCreationError(HTTPClientError):
    """
    Exception raised during the creation of an HTTP client adapter.
    """


class UnsupportedClientTypeError(ClientCreationError):
    """
    Exception raised during the creation of a client when the client type is not supported.
    """

    def __init__(self, client_type: ClientType) -> None:
        message = f"Unsupported client type: {client_type}"
        super().__init__(message)


class MissingArgumentError(ClientCreationError):
    """
    Exception raised when a required argument is missing for client creation.
    """

    def __init__(self) -> None:
        message = "Flask client requires either 'app' or 'client' argument"
        super().__init__(message)


def create_client(client_type: ClientType, **kwargs: t.Any) -> "HTTPClientFacade":
    """
    Create an HTTP client with its adapter based on client type and configuration.

    Args:
        client_type: Type of client to create (HTTPX, REQUESTS or FLASK)
        **kwargs: Client configuration parameters (base_url, verify, timeout, app, etc.)

    Returns:
        Configured HTTP client adapter

    Raises:
        UnsupportedClientTypeError: When client_type is not supported.
        ImportError: When required dependencies are not installed.
        MissingArgumentError: When 'app' or 'client' arguments are not provided for Flask's client.
        TypeError: When the provided 'app' argument is not an instance of Flask's class.
    """
    if client_type == ClientType.HTTPX:
        import httpx
        from exobrain.actions.client.http_client.httpx_adapter import HTTPXClientAdapter

        httpx_client = httpx.Client(**kwargs)
        return HTTPXClientAdapter(httpx_client)

    if client_type == ClientType.REQUESTS:
        import requests
        from exobrain.actions.client.http_client.requests_adapter import RequestsClientAdapter

        session = requests.Session()
        return RequestsClientAdapter(session, **kwargs)

    if client_type == ClientType.FLASK:
        import flask
        from exobrain.actions.client.http_client.flask_adapter import FlaskClientAdapter

        if "app" in kwargs:
            app = kwargs["app"]
            if not isinstance(app, flask.Flask):
                raise TypeError(repr(type(app)))
            flask_client = app.test_client(**kwargs)
        elif "client" in kwargs:
            flask_client = kwargs["client"]
        else:
            raise MissingArgumentError

        return FlaskClientAdapter(flask_client)

    raise UnsupportedClientTypeError(client_type)

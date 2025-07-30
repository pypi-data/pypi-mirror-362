class HTTPClientError(Exception):
    """
    Base class for HTTP-related errors.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)

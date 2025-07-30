from typing import Any


class SCIMClientError(Exception):
    """Base exception for scim2-client.

    :param message: The exception reason.
    :param source: The request payload or the response object that have
        caused the exception.
    """

    def __init__(self, message: str, source: Any = None, *args, **kwargs):
        self.message = message
        self.source = source
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.message or "UNKNOWN"


class SCIMRequestError(SCIMClientError):
    """Base exception for errors happening during request payload building."""


class RequestNetworkError(SCIMRequestError):
    """Error raised when a network error happened during request.

    This error is raised when a :class:`httpx.RequestError` has been caught while performing a request.
    The original :class:`~httpx.RequestError` is available with :attr:`~BaseException.__cause__`.
    """

    def __init__(self, *args, **kwargs):
        message = kwargs.pop("message", "Network error happened during request")
        super().__init__(message, *args, **kwargs)


class RequestPayloadValidationError(SCIMRequestError):
    """Error raised when an invalid request payload has been passed to SCIMClient.

    This error is raised when a :class:`pydantic.ValidationError` has been caught
    while validating the client request payload.
    The original :class:`~pydantic.ValidationError` is available with :attr:`~BaseException.__cause__`.

    .. code-block:: python

        try:
            scim.create(
                {
                    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
                    "active": "not-a-bool",
                }
            )
        except RequestPayloadValidationError as exc:
            print("Original validation error cause", exc.__cause__)
    """

    def __init__(self, *args, **kwargs):
        message = kwargs.pop("message", "Server request payload validation error")
        super().__init__(message, *args, **kwargs)


class SCIMResponseError(SCIMClientError):
    """Base exception for errors happening during response payload validation."""


class SCIMResponseErrorObject(SCIMResponseError):
    """The server response returned a :class:`scim2_models.Error` object.

    Those errors are only raised when the :code:`raise_scim_errors` parameter is :data:`True`.
    """

    def __init__(self, obj, *args, **kwargs):
        message = kwargs.pop(
            "message", f"The server returned a SCIM Error object: {obj}"
        )
        super().__init__(message, *args, **kwargs)


class UnexpectedStatusCode(SCIMResponseError):
    """Error raised when a server returned an unexpected status code for a given :class:`~scim2_models.Context`."""

    def __init__(self, status_code: int, *args, **kwargs):
        message = kwargs.pop(
            "message", f"Unexpected response status code: {status_code}"
        )
        super().__init__(message, *args, **kwargs)


class UnexpectedContentType(SCIMResponseError):
    """Error raised when a server returned an unexpected `Content-Type` header in a response."""

    def __init__(self, content_type, *args, **kwargs):
        message = kwargs.pop("message", f"Unexpected content type: {content_type}")
        super().__init__(message, *args, **kwargs)


class UnexpectedContentFormat(SCIMResponseError):
    """Error raised when a server returned a response in a non-JSON format."""

    def __init__(self, *args, **kwargs):
        message = kwargs.pop("message", "Unexpected response content format")
        super().__init__(message, *args, **kwargs)


class ResponsePayloadValidationError(SCIMResponseError):
    """Error raised when the server returned a payload that cannot be validated.

    This error is raised when a :class:`pydantic.ValidationError` has been caught
    while validating the server response payload.
    The original :class:`~pydantic.ValidationError` is available with :attr:`~BaseException.__cause__`.

    .. code-block:: python

        try:
            scim.query(User, "foobar")
        except ResponsePayloadValidationError as exc:
            print("Original validation error cause", exc.__cause__)
    """

    def __init__(self, *args, **kwargs):
        message = kwargs.pop("message", "Server response payload validation error")
        super().__init__(message, *args, **kwargs)

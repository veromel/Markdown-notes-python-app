from enum import Enum


class ExceptionGroups(Enum):
    """Domain exception groups."""

    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    NOT_FOUND = "not_found"
    UNPROCESSABLE_ENTITY = "unprocessable_entity"
    SERVICE_UNAVAILABLE = "service_unavailable"
    INTERNAL_SERVER_ERROR = "internal_server_error"


class DomainException(Exception):

    type: str
    detail: str
    group: ExceptionGroups

    def __init__(
        self,
        type: str | None = None,
        detail: str | None = None,
        group: ExceptionGroups | None = None,
    ):
        self.type = type or self.type
        self.detail = detail or self.detail
        self.group = group or self.group
        super().__init__(self.type, self.detail, self.group)

    def __str__(self):
        return f"{self.detail}"


class ValidationException(DomainException):
    type = "invalid_validation"
    detail = "Invalid field"
    group = ExceptionGroups.UNPROCESSABLE_ENTITY


class NotFoundException(DomainException):
    type = "not_found"
    detail = "Not found exception"
    group = ExceptionGroups.NOT_FOUND


class AuthenticationException(DomainException):
    type = "invalid_authentication"
    detail = "Invalid credentials for authentication"
    group = ExceptionGroups.UNAUTHORIZED


class AuthorizationException(DomainException):
    type = "invalid_authorization"
    detail = "Not authorized for the request"
    group = ExceptionGroups.FORBIDDEN


class UnexpectedError(DomainException):
    type = "unexpected_error"
    detail = "An unexpected error has occurred."
    group = ExceptionGroups.INTERNAL_SERVER_ERROR

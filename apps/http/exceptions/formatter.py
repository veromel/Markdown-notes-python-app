from dataclasses import dataclass, field
from http import HTTPStatus

from pydantic import create_model

from src.shared.domain.exceptions import DomainException

# Errores comunes de validación de Pydantic
PYDANTIC_ERRORS = [
    "uuid_parsing",
    "uuid_type",
    "url_type",
    "string_type",
    "int_type",
    "bool_type",
    "dict_type",
    "float_type",
    "list_type",
    "time_type",
    "json_invalid",
]


@dataclass
class HTTPExceptionResponses:
    exceptions: dict = field(default_factory=dict)

    def __post_init__(self):
        status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        for error_type in PYDANTIC_ERRORS:
            self.add(
                type=error_type,
                detail=f"Error de validación: {error_type}",
                status_code=status_code,
            )

    @property
    def model(self) -> dict:
        """Modelo base para las respuestas de error."""
        return {
            "model": create_model(
                "Error",
                type=(str, "string"),
                detail=(str, "string"),
            ),
            "content": {
                "application/json": {"examples": {}},
            },
        }

    def add(self, type: str, detail: str, status_code: int) -> None:
        if not self.exceptions.get(status_code):
            self.exceptions[status_code] = self.model

        self.exceptions[status_code]["content"]["application/json"]["examples"][
            type
        ] = {
            "summary": type.capitalize().replace("_", " "),
            "description": detail,
            "value": {
                "type": type,
                "detail": detail,
            },
        }

    def register(self, exc: DomainException) -> None:
        status_code = HTTPStatus[exc.group.name]
        self.add(
            type=exc.type,
            detail=exc.detail,
            status_code=status_code,
        )


def exception_responses(exceptions: list[DomainException]) -> dict:
    """
    Genera respuestas de excepciones formateadas para la documentación de API.

    Args:
        exceptions: Lista de excepciones de dominio a registrar.

    Returns:
        Diccionario con las respuestas de excepciones formateadas.
    """
    responses = HTTPExceptionResponses()
    for exception in exceptions:
        if isinstance(exception, DomainException):
            responses.register(exception)

    return responses.exceptions

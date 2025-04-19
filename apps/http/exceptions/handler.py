"""ExceptionHandler."""

from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse

from src.shared.domain.exceptions import DomainException, UnexpectedError
from apps.http.exceptions.formatter import HTTPExceptionResponses


class ExceptionHandler:
    def __new__(cls, app: FastAPI):
        @app.exception_handler(ValidationError)
        async def pydantic_exception_handler(_: Request, exc: ValidationError):
            errors = [
                {
                    "type": error["type"],
                    "detail": error["msg"],
                    "loc": error["loc"][0],
                    "field": error["loc"][-1],
                    "input": error["input"],
                }
                for error in exc.errors()
            ]
            return JSONResponse(status_code=422, content={"errors": errors})

        @app.exception_handler(RequestValidationError)
        async def pydantic_exception_handler(
            _: Request, exc: RequestValidationError
        ):  # noqa: F811
            errors = [
                {
                    "type": error["type"],
                    "detail": error["msg"],
                    "loc": error["loc"][0],
                    "field": error["loc"][-1],
                    "input": error["input"],
                }
                for error in exc.errors()
            ]
            return JSONResponse(status_code=422, content={"errors": errors})

        @app.exception_handler(DomainException)
        async def domain_exception_handler(_: Request, exc: DomainException):
            status_code = HTTPStatus[exc.group.name]
            return JSONResponse(
                status_code=status_code,
                content={"errors": [{"type": exc.type, "detail": exc.detail}]},
            )

        @app.exception_handler(Exception)
        async def unexpected_exception_handler(_: Request, _exc: Exception):
            return JSONResponse(
                status_code=500,
                content={
                    "errors": [
                        {"type": UnexpectedError.type, "detail": UnexpectedError.detail}
                    ]
                },
            )

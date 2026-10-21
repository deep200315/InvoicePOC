"""Domain exceptions and their mapping to HTTP error responses with stable codes.

Owner: Deeptanush (Tech Lead) · Task: T-101 (expanded in T-403)
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from invoice_api.schemas.common import ErrorBody

log = logging.getLogger(__name__)


class AppError(Exception):
    status_code = 400
    code = "BAD_REQUEST"

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class NotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"


class ConflictError(AppError):
    status_code = 409
    code = "CONFLICT"


class UnauthorizedError(AppError):
    status_code = 401
    code = "UNAUTHORIZED"


class ForbiddenError(AppError):
    status_code = 403
    code = "FORBIDDEN"


class FileTooLargeError(AppError):
    status_code = 413
    code = "FILE_TOO_LARGE"


class UnsupportedFileError(AppError):
    status_code = 415
    code = "UNSUPPORTED_FILE_TYPE"


class ValidationFailedError(AppError):
    status_code = 422
    code = "VALIDATION_FAILED"


def _body(code: str, message: str) -> dict[str, str]:
    return ErrorBody(code=code, message=message).model_dump()


async def _handle_app_error(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, AppError)
    return JSONResponse(status_code=exc.status_code, content=_body(exc.code, exc.message))


async def _handle_unexpected(_: Request, exc: Exception) -> JSONResponse:
    log.exception("Unhandled error", exc_info=exc)
    return JSONResponse(status_code=500, content=_body("INTERNAL_ERROR", "Something went wrong."))


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, _handle_app_error)
    app.add_exception_handler(Exception, _handle_unexpected)

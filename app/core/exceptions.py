from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StartleeteHTTPException
import logging

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: StartleeteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": str(exc.detail), "data": None},
    )


def verification_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation Error",
            "data": {"errors": errors},
        },
    )


async def global_exception_handler(request: Request, exc: Exception):
    # Exception: This catches unexpected exceptions that aren't already handled by more specific handlers.
    # logger.exception(): Records the exception and traceback in your application logs, helping you debug the actual problem.
    logger.exception("Unhandled exception occurred", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal Server Error", "data": None},
    )

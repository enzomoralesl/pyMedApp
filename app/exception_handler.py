from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from app.schemas.error import APIErrorResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import HTTPException
import logging
from http import HTTPStatus

logger = logging.getLogger("uvicorn.error")

# Map SQL constraint names to custom messages (adapt as needed)
CONSTRAINT_MESSAGES = {
    "tb_patient_email_key": ("Email ja cadastrado", 409, "CONFLICT")
}

def get_error_response(status_code, status_name, message, error_details=None):
    return APIErrorResponse(
        statusCode=status_code,
        status=status_name,
        message=message,
        errorDetails=error_details
    )

def get_status_name(status_code):
    try:
        return HTTPStatus(status_code).name
    except Exception:
        return "ERROR"

def add_exception_handlers(app):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.error(f"HTTPException: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": get_error_response(
                status_code=exc.status_code,
                status_name=get_status_name(exc.status_code),
                message=exc.detail,
                error_details=None
            ).dict()},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=400,
            content={"error": get_error_response(
                status_code=400,
                status_name="BAD_REQUEST",
                message="Erro de validação",
                error_details=str(exc)
            ).dict()},
        )

    @app.exception_handler(IntegrityError)
    async def sqlalchemy_integrity_error_handler(request: Request, exc: IntegrityError):
        logger.error(f"Integrity error: {exc}")
        # Usar str(exc) para garantir que a mensagem do constraint seja encontrada
        msg = str(exc)
        for constraint, (custom_msg, code, status_name) in CONSTRAINT_MESSAGES.items():
            if constraint in msg:
                return JSONResponse(
                    status_code=409,
                    content={"error": get_error_response(
                        statusCode=409,
                        status="CONFLICT",
                        message=custom_msg,
                        errorDetails=msg
                    ).dict()},
                )
        return JSONResponse(
            status_code=500,
            content={"error": get_error_response(
                statusCode=500,
                status="INTERNAL_SERVER_ERROR",
                message="Erro de violação de integridade na base de dados",
                errorDetails=msg
            ).dict()},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"error": get_error_response(
                status_code=500,
                status_name="INTERNAL_SERVER_ERROR",
                message="Erro inesperado",
                error_details=str(exc)
            ).dict()},
        )

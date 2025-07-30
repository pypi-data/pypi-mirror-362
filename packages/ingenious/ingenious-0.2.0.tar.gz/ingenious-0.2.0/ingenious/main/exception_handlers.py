"""
Exception handlers for the FastAPI application.

This module contains exception handlers for proper error responses
and logging of exceptions across the application.
"""

import os
import time
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from fastapi import Request
from fastapi.exceptions import RequestValidationError as FastAPIValidationError
from fastapi.responses import JSONResponse

from ingenious.core.structured_logging import get_logger
from ingenious.errors import (
    APIError,
    AuthenticationError,
    AuthorizationError,
    ConfigurationError,
    DatabaseError,
    IngeniousError,
    RateLimitError,
    RequestValidationError,
    ResourceError,
    ServiceError,
    WorkflowNotFoundError,
    handle_exception,
)

if TYPE_CHECKING:
    from fastapi import FastAPI

logger = get_logger(__name__)


class ExceptionHandlers:
    """Collection of exception handlers for FastAPI application."""

    @staticmethod
    async def generic_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle generic exceptions with proper error responses."""
        if os.environ.get("LOADENV") == "True":
            load_dotenv()

        # Handle Ingenious errors with proper status codes and user messages
        if isinstance(exc, IngeniousError):
            status_code = ExceptionHandlers._get_status_code_for_error(exc)

            logger.error(
                "Ingenious error in API",
                error_type=exc.__class__.__name__,
                error_code=exc.error_code,
                category=exc.category.value,
                severity=exc.severity.value,
                correlation_id=exc.context.correlation_id,
                request_path=str(request.url.path),
                request_method=request.method,
                user_id=exc.context.user_id,
                recoverable=exc.recoverable,
                exc_info=True,
            )

            response_content = {
                "error": {
                    "code": exc.error_code,
                    "message": exc.user_message,
                    "correlation_id": exc.context.correlation_id,
                    "recoverable": exc.recoverable,
                    "recovery_suggestion": exc.recovery_suggestion,
                }
            }

            response = JSONResponse(status_code=status_code, content=response_content)

            # Add rate limiting headers if applicable
            if hasattr(exc, "retry_after") and exc.retry_after:
                response.headers["Retry-After"] = str(exc.retry_after)
                response.headers["X-RateLimit-Reset"] = str(
                    int(time.time()) + exc.retry_after
                )

            return response

        # Convert generic exceptions to Ingenious errors
        else:
            ingenious_error = handle_exception(
                exc,
                operation="api_request",
                component="fastapi",
                request_path=str(request.url.path),
                request_method=request.method,
            )

            logger.error(
                "Unhandled exception converted to IngeniousError",
                error_type=type(exc).__name__,
                error_message=str(exc),
                correlation_id=ingenious_error.context.correlation_id,
                request_path=str(request.url.path),
                request_method=request.method,
                exc_info=True,
            )

            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": ingenious_error.error_code,
                        "message": ingenious_error.user_message,
                        "correlation_id": ingenious_error.context.correlation_id,
                        "recoverable": ingenious_error.recoverable,
                    }
                },
            )

    @staticmethod
    async def validation_exception_handler(
        request: Request, exc: FastAPIValidationError
    ) -> JSONResponse:
        """Handle FastAPI validation errors with structured format."""
        # Create structured validation error
        validation_error = RequestValidationError(
            "Request validation failed",
            context={
                "request_path": str(request.url.path),
                "request_method": request.method,
                "validation_errors": exc.errors() if hasattr(exc, "errors") else [],
                "request_body": getattr(exc, "body", None),
            },
            user_message="Invalid request format. Please check your input data.",
        )

        logger.warning(
            "Request validation error",
            error_type="RequestValidationError",
            error_code=validation_error.error_code,
            request_path=str(request.url.path),
            request_method=request.method,
            validation_errors=exc.errors() if hasattr(exc, "errors") else [],
            correlation_id=validation_error.context.correlation_id,
        )

        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": validation_error.error_code,
                    "message": validation_error.user_message,
                    "correlation_id": validation_error.context.correlation_id,
                    "details": exc.errors() if hasattr(exc, "errors") else [],
                    "recoverable": validation_error.recoverable,
                }
            },
        )

    @staticmethod
    def _get_status_code_for_error(error: IngeniousError) -> int:
        """Map Ingenious errors to appropriate HTTP status codes."""
        # Authentication and authorization errors
        if isinstance(error, AuthenticationError):
            return 401
        elif isinstance(error, AuthorizationError):
            return 403

        # Client errors (4xx)
        elif isinstance(error, RequestValidationError):
            return 422  # Unprocessable Entity for validation errors
        elif isinstance(error, ConfigurationError):
            return 400  # Bad Request for configuration issues
        elif isinstance(error, (WorkflowNotFoundError, ResourceError)):
            return 404
        elif isinstance(error, RateLimitError):
            return 429

        # Server errors (5xx)
        elif isinstance(error, DatabaseError):
            return 503  # Service Unavailable for database issues
        elif isinstance(error, ServiceError):
            return 502  # Bad Gateway for service issues
        elif isinstance(error, APIError):
            # Check if it's a client error based on message
            if "timeout" in error.message.lower():
                return 504  # Gateway Timeout
            elif "not found" in error.message.lower():
                return 404
            else:
                return 500

        # Default to internal server error
        else:
            return 500

    @classmethod
    def register_handlers(cls, app: "FastAPI") -> None:
        """Register all exception handlers with the FastAPI app."""
        app.add_exception_handler(Exception, cls.generic_exception_handler)
        app.add_exception_handler(
            FastAPIValidationError,
            cls.validation_exception_handler,  # type: ignore
        )

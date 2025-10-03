"""
Middleware for Resume Tailor AI application.

Contains middleware for:
- Request logging
- Correlation ID tracking
- Error handling and logging
"""

import logging
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger("resume_tailor.middleware")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log HTTP requests and responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log details."""
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())

        # Add correlation ID to request state
        request.state.correlation_id = correlation_id

        # Start timing
        start_time = time.time()

        # Log request
        await self._log_request(request, correlation_id)

        # Process request
        try:
            response = await call_next(request)

            # Calculate duration
            duration = round((time.time() - start_time) * 1000, 2)

            # Log response
            await self._log_response(request, response, correlation_id, duration)

            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id

            return response

        except Exception as exc:
            # Calculate duration
            duration = round((time.time() - start_time) * 1000, 2)

            # Log error
            logger.error(
                f"Request failed: {request.method} {request.url}",
                exc_info=True,
                extra={
                    "correlation_id": correlation_id,
                    "method": request.method,
                    "url": str(request.url),
                    "duration": duration,
                    "status_code": 500,
                }
            )

            # Return error response
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "correlation_id": correlation_id},
                headers={"X-Correlation-ID": correlation_id}
            )

    async def _log_request(self, request: Request, correlation_id: str) -> None:
        """Log incoming request details."""
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        logger.info(
            f"Incoming request: {request.method} {request.url}",
            extra={
                "correlation_id": correlation_id,
                "method": request.method,
                "url": str(request.url),
                "client_ip": client_ip,
                "user_agent": user_agent,
                "headers": dict(request.headers),
            }
        )

    async def _log_response(
        self, request: Request, response: Response, correlation_id: str, duration: float
    ) -> None:
        """Log response details."""
        logger.info(
            f"Response: {request.method} {request.url} - {response.status_code}",
            extra={
                "correlation_id": correlation_id,
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "duration": duration,
            }
        )


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware to handle and log uncaught exceptions."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Handle exceptions and provide structured error responses."""
        try:
            return await call_next(request)
        except Exception as exc:
            correlation_id = getattr(request.state, "correlation_id", str(uuid.uuid4()))

            logger.exception(
                f"Unhandled exception in {request.method} {request.url}",
                extra={
                    "correlation_id": correlation_id,
                    "method": request.method,
                    "url": str(request.url),
                    "exception_type": type(exc).__name__,
                }
            )

            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "message": "An unexpected error occurred",
                    "correlation_id": correlation_id
                },
                headers={"X-Correlation-ID": correlation_id}
            )
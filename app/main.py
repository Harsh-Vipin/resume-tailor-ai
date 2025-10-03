"""
Resume Tailor AI - FastAPI Application

A FastAPI application for AI-powered resume tailoring.
"""

import asyncio
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, AsyncGenerator
from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

# Import logging configuration and middleware
from .logging_config import setup_logging
from .middleware import LoggingMiddleware, ErrorHandlingMiddleware

# Set up logging before creating the app
# Get configuration from environment variables or use defaults
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/resume_tailor.log")
ENABLE_CONSOLE_LOGGING = os.getenv("ENABLE_CONSOLE_LOGGING", "true").lower() == "true"
ENABLE_JSON_LOGGING = os.getenv("ENABLE_JSON_LOGGING", "false").lower() == "true"

# Configure logging
setup_logging(
    log_level=LOG_LEVEL,
    log_file=LOG_FILE,
    enable_console=ENABLE_CONSOLE_LOGGING,
    enable_json=ENABLE_JSON_LOGGING
)

# Get logger for this module
logger = logging.getLogger("resume_tailor.main")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan event handler."""
    # Startup
    logger.info("Starting Resume Tailor AI application")
    logger.info(f"Log level: {LOG_LEVEL}")
    logger.info(f"Log file: {LOG_FILE}")
    logger.info(f"Console logging: {ENABLE_CONSOLE_LOGGING}")
    logger.info(f"JSON logging: {ENABLE_JSON_LOGGING}")

    yield

    # Shutdown
    logger.info("Shutting down Resume Tailor AI application")

# Create FastAPI app instance
app = FastAPI(
    title="Resume Tailor AI",
    description="AI-powered resume tailoring application",
    version="0.1.0"
)

# Create FastAPI app instance with lifespan
app = FastAPI(
    title="Resume Tailor AI",
    description="AI-powered resume tailoring application",
    version="0.1.0",
    lifespan=lifespan
)

# Add middleware (order matters - ErrorHandling should be first)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware)


@app.get("/")
async def root(request: Request):
    """Root endpoint returning a welcome message."""
    correlation_id = getattr(request.state, "correlation_id", "unknown")

    logger.info(
        "Root endpoint accessed",
        extra={"correlation_id": correlation_id}
    )

    return {
        "message": "Hello World", 
        "app": "Resume Tailor AI", 
        "version": "0.1.0",
        "correlation_id": correlation_id
    }


@app.get("/health", response_model=Dict[str, Any])
async def health_check(request: Request) -> Dict[str, Any]:
    """
    Health check endpoint that returns service status.

    Returns HTTP 200 with service status and optional dependency checks.
    This endpoint can be extended to include database and external service connectivity checks.

    Returns:
        Dict containing health status and metadata
    """
    start_time = time.time()
    correlation_id = getattr(request.state, "correlation_id", "unknown")

    logger.info(
        "Health check requested",
        extra={"correlation_id": correlation_id}
    )

    # Basic health response
    health_response = {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "Resume Tailor AI",
        "version": "0.1.0",
        "correlation_id": correlation_id
    }

    # Perform async dependency checks
    checks = await perform_health_checks()

    # Add checks to response
    health_response.update({
        "checks": checks,
        "response_time_ms": round((time.time() - start_time) * 1000, 2)
    })

    # Log health check result
    if all(check.get("status") == "healthy" for check in checks.values()):
        logger.info(
            f"Health check passed - response time: {health_response['response_time_ms']}ms",
            extra={"correlation_id": correlation_id}
        )
    else:
        logger.warning(
            f"Health check has issues - response time: {health_response['response_time_ms']}ms",
            extra={"correlation_id": correlation_id, "checks": checks}
        )

    return health_response


async def perform_health_checks() -> Dict[str, Dict[str, Any]]:
    """
    Perform asynchronous health checks for various dependencies.

    This function can be expanded to include:
    - Database connectivity checks
    - External API service checks
    - File system checks
    - Memory/CPU usage checks

    Returns:
        Dict containing results of various health checks
    """
    logger.debug("Performing health checks")

    checks = {}

    # Example: Application runtime check
    checks["application"] = {
        "status": "healthy",
        "message": "Application is running normally"
    }

    # Example: System resources check (basic)
    checks["system"] = {
        "status": "healthy",
        "message": "System resources available"
    }

    # Future expansion examples (commented out for now):

    # Database check
    # checks["database"] = await check_database_connection()

    # External API check  
    # checks["external_apis"] = await check_external_services()

    # File system check
    # checks["filesystem"] = await check_filesystem_access()

    return checks


# Example implementations for future use:

async def check_database_connection() -> Dict[str, Any]:
    """
    Check database connectivity (placeholder for future implementation).

    Returns:
        Dict containing database health status
    """
    logger.debug("Checking database connection")

    try:
        # Simulate database check with a small delay
        await asyncio.sleep(0.01)

        # In real implementation, this would be something like:
        # await database.execute("SELECT 1")

        logger.debug("Database connection check successful")
        return {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
        logger.error(
            f"Database connection check failed: {str(e)}",
            exc_info=True
        )
        return {
            "status": "unhealthy", 
            "message": f"Database connection failed: {str(e)}"
        }


async def check_external_services() -> Dict[str, Any]:
    """
    Check external service connectivity (placeholder for future implementation).

    Returns:
        Dict containing external services health status
    """
    logger.debug("Checking external services")

    try:
        # Simulate external service check
        await asyncio.sleep(0.01)

        # In real implementation, this would ping external APIs

        logger.debug("External services check successful")
        return {
            "status": "healthy",
            "message": "External services accessible"
        }
    except Exception as e:
        logger.error(
            f"External services check failed: {str(e)}",
            exc_info=True
        )
        return {
            "status": "unhealthy",
            "message": f"External service check failed: {str(e)}"
        }


async def check_filesystem_access() -> Dict[str, Any]:
    """
    Check filesystem access (placeholder for future implementation).

    Returns:
        Dict containing filesystem health status
    """
    logger.debug("Checking filesystem access")

    try:
        # Check if we can access required directories
        project_root = Path(__file__).parent.parent

        if project_root.exists() and project_root.is_dir():
            logger.debug("Filesystem access check successful")
            return {
                "status": "healthy",
                "message": "Filesystem access normal"
            }
        else:
            logger.warning("Cannot access project directory")
            return {
                "status": "unhealthy",
                "message": "Cannot access project directory"
            }
    except Exception as e:
        logger.error(
            f"Filesystem access check failed: {str(e)}",
            exc_info=True
        )
        return {
            "status": "unhealthy",
            "message": f"Filesystem check failed: {str(e)}"
        }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with proper logging."""
    correlation_id = getattr(request.state, "correlation_id", "unknown")

    logger.warning(
        f"HTTP exception: {exc.status_code} - {exc.detail}",
        extra={
            "correlation_id": correlation_id,
            "status_code": exc.status_code,
            "method": request.method,
            "url": str(request.url),
        }
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "correlation_id": correlation_id
        },
        headers={"X-Correlation-ID": correlation_id}
    )


def main():
    """CLI entry point for running the application."""
    import uvicorn

    logger.info("Starting Resume Tailor AI via CLI")

    # Add the project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    uvicorn.run(
        "app.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        reload_dirs=[str(project_root / "app")],
        log_level="info"
    )

if __name__ == "__main__":
    main()
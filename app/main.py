"""
Resume Tailor AI - FastAPI Application

A FastAPI application for AI-powered resume tailoring.
"""

import asyncio
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import FastAPI

# Create FastAPI app instance
app = FastAPI(
    title="Resume Tailor AI",
    description="AI-powered resume tailoring application",
    version="0.1.0"
)

@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Hello World", "app": "Resume Tailor AI", "version": "0.1.0"}


@app.get("/health", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint that returns service status.

    Returns HTTP 200 with service status and optional dependency checks.
    This endpoint can be extended to include database and external service connectivity checks.

    Returns:
        Dict containing health status and metadata
    """
    start_time = time.time()

    # Basic health response
    health_response = {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "Resume Tailor AI",
        "version": "0.1.0"
    }

    # Perform async dependency checks
    checks = await perform_health_checks()

    # Add checks to response
    health_response.update({
        "checks": checks,
        "response_time_ms": round((time.time() - start_time) * 1000, 2)
    })

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
    try:
        # Simulate database check with a small delay
        await asyncio.sleep(0.01)

        # In real implementation, this would be something like:
        # await database.execute("SELECT 1")

        return {
            "status": "healthy",
            "message": "Database connection successful"
        }
    except Exception as e:
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
    try:
        # Simulate external service check
        await asyncio.sleep(0.01)

        # In real implementation, this would ping external APIs

        return {
            "status": "healthy",
            "message": "External services accessible"
        }
    except Exception as e:
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
    try:
        # Check if we can access required directories
        project_root = Path(__file__).parent.parent

        if project_root.exists() and project_root.is_dir():
            return {
                "status": "healthy",
                "message": "Filesystem access normal"
            }
        else:
            return {
                "status": "unhealthy",
                "message": "Cannot access project directory"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Filesystem check failed: {str(e)}"
        }

def main():
    """CLI entry point for running the application."""
    import uvicorn

    # Add the project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    uvicorn.run(
        "app.main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        reload_dirs=[str(project_root / "app")]
    )

if __name__ == "__main__":
    main()
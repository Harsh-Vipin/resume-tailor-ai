"""
FastAPI main application module for Resume Tailor AI
"""

from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .health import HealthChecker

# Create FastAPI app instance
app = FastAPI(
    title="Resume Tailor AI",
    description="AI-powered resume tailoring application",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize health checker
health_checker = HealthChecker()

@app.get("/")
async def root():
    """Root endpoint returning a welcome message"""
    return {"message": "Hello World! Welcome to Resume Tailor AI"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint that returns comprehensive service status.

    Returns:
        JSONResponse: Health status with HTTP 200 for healthy, 503 for unhealthy
    """
    timestamp = datetime.utcnow().isoformat() + "Z"

    health_data = {
        "status": "ok",
        "timestamp": timestamp,
        "service": "resume-tailor-ai",
        "version": "0.1.0"
    }

    try:
        # Run all health checks
        dependency_results = await health_checker.run_all_checks()
        health_data["dependencies"] = dependency_results

        # Determine overall health status based on dependencies
        all_healthy = all(
            dep.get("status") == "healthy"
            for dep in dependency_results.values()
            if isinstance(dep, dict) and "status" in dep
        )

        if not all_healthy:
            health_data["status"] = "degraded"
            # Return 200 for degraded state, but indicate issues in response

    except Exception as e:
        health_data["status"] = "error"
        health_data["error"] = str(e)
        return JSONResponse(
            status_code=503,
            content=health_data
        )

    return JSONResponse(
        status_code=200,
        content=health_data
    )
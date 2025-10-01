"""
Resume Tailor AI - FastAPI Application

A FastAPI application for AI-powered resume tailoring.
"""

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
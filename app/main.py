"""
Resume Tailor AI - FastAPI Application

A FastAPI application for AI-powered resume tailoring.
"""

import sys
from pathlib import Path
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
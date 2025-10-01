# Development server startup script using UV (PowerShell)
Write-Host "Starting Resume Tailor AI development server..."
Write-Host "Installing dependencies with UV..."
uv sync
Write-Host "Starting FastAPI server..."
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

#!/bin/bash

# Development server startup script using UV
echo "Starting Resume Tailor AI development server..."
echo "Installing dependencies with UV..."
uv sync
echo "Starting FastAPI server..."
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
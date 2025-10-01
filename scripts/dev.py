#!/usr/bin/env python3
"""
Development server runner for Resume Tailor AI using UV

This script provides a development server with hot reload capabilities
optimized for UV package manager workflow.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Run the development server using UV."""
    project_root = Path(__file__).parent.parent

    try:
        # Use UV to run uvicorn with the app
        subprocess.run([
            "uv", "run", "uvicorn", "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload",
            "--reload-dir", str(project_root / "app")
        ], cwd=project_root, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running development server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down development server...")
        sys.exit(0)

if __name__ == "__main__":
    main()
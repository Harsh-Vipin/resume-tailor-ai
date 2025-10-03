# resume-tailor-ai

[![Hacktoberfest](https://img.shields.io/badge/Hacktoberfest-2025-orange.svg)](https://hacktoberfest.com/)

An AI-powered resume tailoring application built with FastAPI and modern Python tooling.

This project is open to contributions for Hacktoberfest!

## Flow

![Resume Tailor Flow](assets/resume-tailor-flow.excalidraw.png)

## Contributing

## 🚀 Quick Start

This project uses [UV](https://github.com/astral-sh/uv) as the package manager for fast dependency resolution and virtual environment management.

### Prerequisites

- Python 3.9+ (UV will manage Python versions automatically)
- [UV package manager](https://github.com/astral-sh/uv#installation)

### Installation

1. **Install UV** (if not already installed):
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # Using pip
   pip install uv
   ```

2. **Clone and set up the project**:
   ```bash
   git clone <repository-url>
   cd resume-tailor-ai

   # Install dependencies (creates virtual environment automatically)
   uv sync
   ```

### ⚙️ Configuration

The application can be configured using environment variables:

#### Logging Configuration
- `LOG_LEVEL` - Logging level (default: `INFO`)
  - Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- `LOG_FILE` - Path to log file (default: `logs/resume_tailor.log`)
- `ENABLE_CONSOLE_LOGGING` - Enable console output (default: `true`)
- `ENABLE_JSON_LOGGING` - Use JSON format for logs (default: `false`)

#### CORS Configuration
- `CORS_ORIGINS` - Comma-separated list of allowed origins (default: `*`)
  - Example: `http://localhost:3000,https://example.com`
  - Use `*` to allow all origins (not recommended for production)
- `CORS_ALLOW_CREDENTIALS` - Allow credentials in CORS requests (default: `true`)
- `CORS_ALLOW_METHODS` - Comma-separated list of allowed HTTP methods (default: `*`)
  - Example: `GET,POST,PUT,DELETE`
- `CORS_ALLOW_HEADERS` - Comma-separated list of allowed headers (default: `*`)
  - Example: `Content-Type,Authorization`

**Example `.env` file:**
```bash
# Logging
LOG_LEVEL=DEBUG
LOG_FILE=logs/app.log
ENABLE_CONSOLE_LOGGING=true
ENABLE_JSON_LOGGING=false

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_ALLOW_HEADERS=Content-Type,Authorization
```

### 🏃‍♂️ Running the Application

#### Option 1: Using UV directly
```bash
# Run the development server with hot reload
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Option 2: Using Make commands
```bash
# Run development server
make run

# Or use the custom script
make run-script
```

#### Option 3: Using the development script
```bash
uv run python scripts/dev.py
```

### 🛠️ Development Commands

```bash
# Install all dependencies including development tools
make dev

# Run tests
make test

# Code formatting
make format

# Linting
make lint

# Clean up cache and build artifacts
make clean
```

### 📡 API Endpoints

Once running, you can access:

- **Application**: http://127.0.0.1:8000/
- **API Documentation**: http://127.0.0.1:8000/docs
- **ReDoc Documentation**: http://127.0.0.1:8000/redoc

### 🏗️ Project Structure

```
resume-tailor-ai/
├── app/                    # FastAPI application
│   ├── __init__.py
│   ├── main.py            # Main application entry point
│   ├── middleware.py      # Custom middleware (Logging, Error handling)
│   └── logging_config.py  # Logging configuration
├── tests/                 # Test suite
│   ├── test_health.py     # Health endpoint tests
│   └── ...
├── scripts/               # Development scripts
│   └── dev.py            # Development server runner
├── pyproject.toml        # Project configuration and dependencies
├── Makefile             # Common development commands
└── README.md

We welcome contributions to resume-tailor-ai! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for more information on how to get started.

## Code of Conduct

Everyone participating in this project is expected to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
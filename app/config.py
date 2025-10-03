"""
Configuration management for Resume Tailor AI.

This module provides secure configuration handling using Pydantic Settings.
All configuration values are loaded from environment variables with proper
validation, type checking, and default values.

Security Features:
- Sensitive values are marked as secrets
- Environment variable validation
- Type safety with Pydantic models
- Centralized configuration management
"""

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional, List, Literal, Any
from pydantic import Field, validator, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
try:
    from pydantic import field_validator  # Pydantic v2
except ImportError:
    field_validator = None  # fallback for Pydantic v1


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    # Database connection
    database_url: Optional[str] = Field(
        default=None,
        description="Full database URL (e.g., postgresql://user:pass@localhost/db)"
    )
    database_host: str = Field(default="localhost", description="Database host")
    database_port: int = Field(default=5432, description="Database port")
    database_name: str = Field(default="resume_tailor", description="Database name")
    database_user: str = Field(default="postgres", description="Database user")
    database_password: SecretStr = Field(
        default=SecretStr(""),
        description="Database password"
    )

    # Connection settings
    database_pool_size: int = Field(default=10, description="Database connection pool size")
    database_max_connections: int = Field(default=20, description="Maximum database connections")
    database_timeout: int = Field(default=30, description="Database connection timeout (seconds)")

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        case_sensitive=False,
        env_file=".env",
        extra="ignore"
    )

    @property
    def connection_url(self) -> str:
        """Generate database connection URL."""
        if self.database_url:
            return self.database_url

        password = self.database_password.get_secret_value()
        if password:
            auth = f"{self.database_user}:{password}"
        else:
            auth = self.database_user

        return f"postgresql://{auth}@{self.database_host}:{self.database_port}/{self.database_name}"

class SecuritySettings(BaseSettings):
    """Security and authentication settings."""

    # JWT and authentication
    secret_key: SecretStr = Field(
        default=SecretStr("your-secret-key-change-in-production"),
        description="Secret key for JWT token generation"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration in minutes"
    )
    refresh_token_expire_days: int = Field(
        default=7,
        description="Refresh token expiration in days"
    )

    # API Keys and external services
    openai_api_key: Optional[SecretStr] = Field(
        default=None,
        description="OpenAI API key for AI features"
    )
    anthropic_api_key: Optional[SecretStr] = Field(
        default=None,
        description="Anthropic API key for Claude AI"
    )

    # CORS settings
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="Allowed CORS origins"
    )
    cors_credentials: bool = Field(default=True, description="Allow CORS credentials")
    cors_methods: List[str] = Field(
        default=["*"],
        description="Allowed CORS methods"
    )
    cors_headers: List[str] = Field(
        default=["*"],
        description="Allowed CORS headers"
    )

    model_config = SettingsConfigDict(
        env_prefix="SECURITY_",
        case_sensitive=False,
        env_file=".env",
        extra="ignore"
    )

    # Use field_validator if available (Pydantic v2), otherwise fallback to validator (Pydantic v1)
    if field_validator:
        # The validator will be attached after the class definition
        pass
    else:
        @validator("secret_key")
        def validate_secret_key(cls, v: SecretStr) -> SecretStr:
            """Validate secret key strength."""
            key = v.get_secret_value()
            if len(key) < 32:
                raise ValueError("Secret key must be at least 32 characters long")
            return v
        # The validator will be attached after the class definition
        pass


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
# Attach validators to SecuritySettings after its definition
if field_validator:
    SecuritySettings.validate_secret_key = field_validator("secret_key", mode="before")(classmethod(
        lambda cls, v: (
            v if len(v.get_secret_value()) >= 32 else (_ for _ in ()).throw(ValueError("Secret key must be at least 32 characters long"))
        )
    ))
else:
    SecuritySettings.validate_secret_key = SecuritySettings.validate_secret_key

class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    log_file: Optional[str] = Field(
        default="logs/resume_tailor.log",
        description="Log file path"
    )
    enable_console_logging: bool = Field(
        default=True,
        description="Enable console logging"
    )
    enable_json_logging: bool = Field(
        default=False,
        description="Enable JSON structured logging"
    )
    log_rotation_size: str = Field(
        default="10MB",
        description="Log file rotation size"
    )
    log_retention_count: int = Field(
        default=5,
        description="Number of log files to keep"
    )

    model_config = SettingsConfigDict(
        env_prefix="LOG_",
        case_sensitive=False,
        env_file=".env",
        extra="ignore"
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level value."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v.upper()


class AppSettings(BaseSettings):
    """Main application settings."""

    # Application metadata
    app_name: str = Field(default="Resume Tailor AI", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    app_description: str = Field(
        default="AI-powered resume tailoring application",
        description="Application description"
    )

    # Server settings
    host: str = Field(default="127.0.0.1", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=False, description="Debug mode")
    reload: bool = Field(default=False, description="Auto-reload on changes")

    # Environment
    environment: Literal["development", "testing", "staging", "production"] = Field(
        default="development",
        description="Application environment"
    )

    # Feature flags
    enable_ai_features: bool = Field(default=True, description="Enable AI-powered features")
    enable_metrics: bool = Field(default=False, description="Enable metrics collection")
    enable_tracing: bool = Field(default=False, description="Enable distributed tracing")

    # File upload settings
    max_upload_size: int = Field(default=10 * 1024 * 1024, description="Max file upload size (bytes)")
    allowed_file_types: List[str] = Field(
        default=[".pdf", ".doc", ".docx", ".txt"],
        description="Allowed file types for upload"
    )

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        case_sensitive=False,
        env_file=".env",
        extra="ignore"
    )

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"


class Settings:
    """Main settings class combining all configuration sections."""

    def __init__(self):
        """Initialize settings with sub-settings."""
        self.app = AppSettings()
        self.database = DatabaseSettings()
        self.security = SecuritySettings()
        self.logging = LoggingSettings()

    @property
    def project_root(self) -> Path:
        """Get project root directory."""
        return Path(__file__).parent.parent

    def get_secret_value(self, secret: SecretStr) -> str:
        """Safely get secret value."""
        return secret.get_secret_value() if secret else ""


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings singleton.

    Uses LRU cache to ensure settings are loaded only once.
    This is the recommended pattern for FastAPI dependency injection.
    """
    return Settings()


# Convenience function for direct access
settings = get_settings()
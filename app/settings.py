from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    APP_NAME: str = "Resume Tailor AI"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Agentic, open-source resume tailor that auto-optimizes your CV for any job description using AI agents."

settings = Settings()
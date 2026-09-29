from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "EduGenie"
    app_version: str = "1.0.0"
    debug: bool = False
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    request_timeout_seconds: float = 60.0
    use_local_explainer: bool = False
    local_explainer_model: str = "MBZUAI/LaMini-Flan-T5-783M"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

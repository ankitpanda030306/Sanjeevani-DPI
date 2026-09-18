from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Sanjeevani-DPI AI Gateway"
    environment: str = "development"  # development | staging | production
    log_level: str = "INFO"

    cors_allowed_origins: str = "*"

    cedar_policy_dir: str = "./policies"

    aws_region: str = "ap-south-1"
    bedrock_model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    bedrock_timeout_seconds: float = 30.0
    cedar_timeout_seconds: float = 5.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        if self.cors_allowed_origins.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton so .env is parsed only once."""
    return Settings()

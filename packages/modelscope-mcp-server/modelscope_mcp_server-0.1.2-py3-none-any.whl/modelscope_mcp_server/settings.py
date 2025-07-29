"""Global settings management for ModelScope MCP Server."""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import (
    DEFAULT_IMAGE_GENERATION_MODEL,
    MODELSCOPE_API_ENDPOINT,
    MODELSCOPE_API_INFERENCE_ENDPOINT,
    MODELSCOPE_OPENAPI_ENDPOINT,
)


class Settings(BaseSettings):
    """Global settings for ModelScope MCP Server."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="MODELSCOPE_",
        case_sensitive=False,
        extra="ignore",
    )

    # ModelScope API settings
    api_token: str | None = Field(
        default=None, description="ModelScope API token for authentication"
    )

    api_base_url: str = Field(
        default=MODELSCOPE_API_ENDPOINT,
        description="Base URL for ModelScope API",
    )

    openapi_base_url: str = Field(
        default=MODELSCOPE_OPENAPI_ENDPOINT,
        description="Base URL for ModelScope OpenAPI",
    )

    api_inference_base_url: str = Field(
        default=MODELSCOPE_API_INFERENCE_ENDPOINT,
        description="Base URL for ModelScope API Inference",
    )

    # Default model settings
    default_image_generation_model: str = Field(
        default=DEFAULT_IMAGE_GENERATION_MODEL,
        description="Default model for image generation",
    )

    # Logging settings
    log_level: str = Field(default="INFO", description="Logging level")

    @field_validator("api_token")
    @classmethod
    def validate_api_token(cls, v: str | None) -> str | None:
        """Validate API token format."""
        if v is not None:
            v = v.strip()
            if not v:
                return None
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in allowed_levels:
            raise ValueError(f"Log level must be one of {allowed_levels}")
        return v

    def is_api_token_configured(self) -> bool:
        """Check if API token is configured."""
        return self.api_token is not None and len(self.api_token) > 0


# Global settings instance
settings = Settings()

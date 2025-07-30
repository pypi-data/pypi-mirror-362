"""
Core configuration management for Open Logistics.

This module uses Pydantic's BaseSettings to manage application configuration,
allowing for type-safe settings loaded from environment variables or a .env file.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class MLXSettings(BaseSettings):
    """Configuration for MLX (Apple Silicon optimization)."""
    MLX_ENABLED: bool = False


class SecuritySettings(BaseSettings):
    """Security-related configurations."""
    SECRET_KEY: str = "default_secret_key_that_should_be_overridden"
    CLASSIFICATION_LEVEL: Literal["UNCLASSIFIED", "CONFIDENTIAL", "SECRET", "TOP_SECRET"] = "UNCLASSIFIED"


class SapBtpSettings(BaseSettings):
    """SAP BTP integration settings."""
    BTP_CLIENT_ID: str = ""
    BTP_CLIENT_SECRET: str = ""
    BTP_TOKEN_URL: str = ""
    BTP_AUTH_URL: str = "https://api.authentication.sap.hana.ondemand.com"
    BTP_AI_CORE_URL: str = "https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com"
    BTP_HANA_URL: str = "https://api.hana.ondemand.com"
    BTP_EVENT_MESH_URL: str = "https://api.eventmesh.sap.hana.ondemand.com"
    BTP_TENANT_ID: str = ""


class Settings(BaseSettings):
    """Main application settings."""
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # Feature flags
    ENABLE_AI_AGENTS: bool = True
    ENABLE_REAL_TIME_OPTIMIZATION: bool = True
    ENABLE_PREDICTIVE_ANALYTICS: bool = True

    # Integrations and services
    mlx: MLXSettings = MLXSettings()
    security: SecuritySettings = SecuritySettings()
    sap_btp: SapBtpSettings = SapBtpSettings()

    # Monitoring
    METRICS_ENABLED: bool = True
    TRACING_ENABLED: bool = True
    PROMETHEUS_NAMESPACE: str = "openlogistics"

    # Database
    DB_POSTGRES_SERVER: str = "localhost"
    DB_POSTGRES_USER: str = "openlogistics"
    DB_POSTGRES_PASSWORD: str = "openlogistics"
    DB_POSTGRES_DB: str = "openlogistics"
    DB_POSTGRES_PORT: int = 5432

    # Cache
    DB_REDIS_HOST: str = "localhost"
    DB_REDIS_PORT: int = 6379
    DB_REDIS_PASSWORD: str = ""


@lru_cache()
def get_settings() -> Settings:
    """
    Get the application settings.

    This function is cached to ensure that settings are loaded only once.
    """
    return Settings() 
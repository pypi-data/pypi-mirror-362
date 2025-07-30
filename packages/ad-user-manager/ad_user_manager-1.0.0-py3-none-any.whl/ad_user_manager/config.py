"""
Configuration management for AD User Manager.
"""

from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .models import (ConflictResolutionConfig, DCServerConfig,
                     LDAPServerConfig, UserAttributeMapping)

# Union type for server configuration
ServerConfig = Annotated[
    DCServerConfig | LDAPServerConfig, Field(discriminator="connection_type")
]


class ADConfig(BaseSettings):
    """Main configuration class for AD User Manager."""

    model_config = SettingsConfigDict(
        env_prefix="AD_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Server configuration (union of DC or LDAP config)
    server: ServerConfig

    # User attribute mapping
    attributes: UserAttributeMapping = Field(default_factory=UserAttributeMapping)

    # Conflict resolution
    conflict_resolution: ConflictResolutionConfig = Field(
        default_factory=ConflictResolutionConfig
    )

    # Connection settings
    connection_timeout: int = Field(30, description="Connection timeout in seconds")
    search_timeout: int = Field(30, description="Search timeout in seconds")
    pool_size: int = Field(5, description="Connection pool size")
    pool_keepalive: int = Field(60, description="Pool keepalive time in seconds")

    # Logging settings
    log_level: str = Field("INFO", description="Logging level")
    log_format: str = Field("json", description="Log format (json or console)")

    # Validation settings
    require_email: bool = Field(
        True, description="Require email address for user creation"
    )
    validate_username_format: bool = Field(True, description="Validate username format")
    username_min_length: int = Field(3, description="Minimum username length")
    username_max_length: int = Field(20, description="Maximum username length")

    @field_validator("server")
    @classmethod
    def validate_server_config(cls, v):
        """Validate server configuration based on type."""
        if isinstance(v, DCServerConfig):
            # Validate DC-specific requirements
            if not v.use_current_credentials and (
                not v.service_account or not v.service_password
            ):
                raise ValueError(
                    "Service account credentials required when not using current user"
                )
            if not v.base_dn and not v.auto_detect_base_dn:
                raise ValueError(
                    "Base DN is required for DC configuration when auto_detect_base_dn is False"
                )
        elif isinstance(v, LDAPServerConfig):
            # Validate LDAP-specific requirements
            if not v.host or not v.bind_dn or not v.bind_password or not v.base_dn:
                raise ValueError(
                    "LDAP configuration requires host, bind_dn, bind_password, and base_dn"
                )
        # Legacy configuration support
        elif not hasattr(v, "base_dn") or not v.base_dn:
            raise ValueError("Base DN is required")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {', '.join(valid_levels)}")
        return v.upper()

    @field_validator("log_format")
    @classmethod
    def validate_log_format(cls, v):
        """Validate log format."""
        valid_formats = ["json", "console"]
        if v.lower() not in valid_formats:
            raise ValueError(f"Log format must be one of: {', '.join(valid_formats)}")
        return v.lower()

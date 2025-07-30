"""
Data models for AD User Manager.
"""

from dataclasses import dataclass
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field


@dataclass
class UserCreationResult:
    """Result of user creation operation."""

    username: str
    created: bool
    original_username: str
    dn: str
    conflicts_resolved: int = 0
    message: str = ""


@dataclass
class UserInfo:
    """User information from AD."""

    username: str
    dn: str
    attributes: dict[str, Any]
    exists: bool = True


class ADServerConfig(BaseModel):
    """Base Active Directory server configuration."""

    model_config = ConfigDict(discriminator="connection_type")

    base_dn: str = Field(
        default="",
        description="Base DN for user operations (auto-detected for DC mode if empty)",
    )


class DCServerConfig(ADServerConfig):
    """Domain Controller configuration (PowerShell-based)."""

    connection_type: Literal["domain_controller"] = "domain_controller"

    # Optional for DC mode - can use current user credentials
    host: str = Field("", description="DC hostname (optional, auto-detected if empty)")
    use_current_credentials: bool = Field(
        True, description="Use current user credentials"
    )

    # Only needed if not using current credentials
    service_account: str = Field(
        "", description="Service account for PowerShell (optional)"
    )
    service_password: str = Field("", description="Service account password (optional)")

    # Smart OU selection options
    default_user_ou: str = Field(
        "", description="Preferred OU for new users (optional)"
    )
    fallback_to_users_container: bool = Field(
        True, description="Use default users container if preferred OU is not available"
    )
    validate_ou_has_users: bool = Field(
        True,
        description="Validate that target OU contains existing users before selection",
    )
    auto_detect_base_dn: bool = Field(
        True, description="Auto-detect base DN if not specified"
    )


class LDAPServerConfig(ADServerConfig):
    """LDAP server configuration (remote connections)."""

    connection_type: Literal["ldap"] = "ldap"

    # Required for LDAP connections
    host: str = Field(..., description="LDAP server hostname or IP")
    port: int = Field(389, description="LDAP port (389 for LDAP, 636 for LDAPS)")
    use_ssl: bool = Field(False, description="Use SSL/TLS connection")
    bind_dn: str = Field(..., description="Bind DN for authentication")
    bind_password: str = Field(..., description="Bind password for authentication")


# Union type for config validation
ServerConfig = Annotated[
    DCServerConfig | LDAPServerConfig, Field(discriminator="connection_type")
]


class UserAttributeMapping(BaseModel):
    """Mapping of user attributes to AD fields."""

    username_field: str = Field("sAMAccountName", description="AD field for username")
    first_name_field: str = Field("givenName", description="AD field for first name")
    last_name_field: str = Field("sn", description="AD field for last name")
    display_name_field: str = Field(
        "displayName", description="AD field for display name"
    )
    email_field: str = Field("mail", description="AD field for email")
    user_principal_name_field: str = Field(
        "userPrincipalName", description="AD field for UPN"
    )
    object_class: list[str] = Field(
        ["top", "person", "organizationalPerson", "user"],
        description="Object classes for user creation",
    )


class ConflictResolutionConfig(BaseModel):
    """Configuration for handling username conflicts."""

    enabled: bool = Field(True, description="Enable automatic conflict resolution")
    max_attempts: int = Field(
        100, description="Maximum attempts to generate unique username"
    )
    suffix_pattern: str = Field(
        "{username}{counter}", description="Pattern for generating unique usernames"
    )
    start_counter: int = Field(1, description="Starting counter for suffix generation")

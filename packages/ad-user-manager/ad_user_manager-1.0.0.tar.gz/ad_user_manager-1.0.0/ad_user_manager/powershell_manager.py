"""
PowerShell-based Active Directory User Manager for Domain Controllers.
"""

import json
import logging
import platform
import subprocess
from typing import Any

import structlog

from .config import ADConfig
from .exceptions import (PowerShellExecutionError, SearchError,
                         UserCreationError, UserExistsError)
from .models import UserCreationResult, UserInfo


class PowerShellADManager:
    """PowerShell-based Active Directory User Manager for Domain Controllers."""

    def __init__(self, config: ADConfig):
        """Initialize PowerShell AD Manager with configuration."""
        self.config = config
        self.logger = structlog.get_logger(__name__)
        self._setup_logging()

        # Check if running on Windows
        if platform.system() != "Windows":
            raise Exception("PowerShell AD Manager requires Windows")

        # Check if AD module is available, try to install if not
        if not self._check_ad_module():
            self.logger.info(
                "Active Directory PowerShell module not found, attempting to install..."
            )
            if self._install_ad_module():
                self.logger.info(
                    "Active Directory PowerShell module installed successfully"
                )
            else:
                raise Exception(
                    "Active Directory PowerShell module not available and could not be installed"
                )

    def _setup_logging(self):
        """Setup structured logging."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level), format="%(message)s"
        )

        if self.config.log_format == "json":
            structlog.configure(
                processors=[
                    structlog.stdlib.filter_by_level,
                    structlog.stdlib.add_logger_name,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.PositionalArgumentsFormatter(),
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.StackInfoRenderer(),
                    structlog.processors.format_exc_info,
                    structlog.processors.JSONRenderer(),
                ],
                wrapper_class=structlog.stdlib.BoundLogger,
                logger_factory=structlog.stdlib.LoggerFactory(),
                cache_logger_on_first_use=True,
            )
        else:
            structlog.configure(
                processors=[
                    structlog.stdlib.filter_by_level,
                    structlog.stdlib.add_logger_name,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.PositionalArgumentsFormatter(),
                    structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                    structlog.dev.ConsoleRenderer(),
                ],
                wrapper_class=structlog.stdlib.BoundLogger,
                logger_factory=structlog.stdlib.LoggerFactory(),
                cache_logger_on_first_use=True,
            )

    def _check_ad_module(self) -> bool:
        """Check if Active Directory PowerShell module is available."""
        try:
            cmd = [
                "powershell",
                "-Command",
                "Get-Module -ListAvailable -Name ActiveDirectory",
            ]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=10, check=False
            )
            return result.returncode == 0 and "ActiveDirectory" in result.stdout
        except Exception as e:
            self.logger.debug("AD module check failed", error=str(e))
            return False

    def _install_ad_module(self) -> bool:
        """Attempt to install the Active Directory PowerShell module."""
        try:
            # First check if running as administrator
            check_admin_cmd = [
                "powershell",
                "-Command",
                "([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] 'Administrator')",
            ]
            admin_result = subprocess.run(
                check_admin_cmd, capture_output=True, text=True, timeout=10, check=False
            )

            if (
                admin_result.returncode != 0
                or admin_result.stdout.strip().lower() != "true"
            ):
                self.logger.warning(
                    "Not running as administrator, cannot install AD module"
                )
                return False

            # Try to determine Windows version and install appropriately
            version_cmd = [
                "powershell",
                "-Command",
                "(Get-CimInstance Win32_OperatingSystem).Version",
            ]
            version_result = subprocess.run(
                version_cmd, capture_output=True, text=True, timeout=10, check=False
            )

            if version_result.returncode == 0:
                version = version_result.stdout.strip()
                self.logger.debug(f"Windows version: {version}")

            # Try Windows Server installation method first
            server_install_cmd = [
                "powershell",
                "-Command",
                "Install-WindowsFeature -Name RSAT-AD-PowerShell -IncludeAllSubFeature",
            ]
            server_result = subprocess.run(
                server_install_cmd,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )

            if server_result.returncode == 0:
                self.logger.info("AD module installed via Windows Server features")
                return self._check_ad_module()

            # Try Windows 10/11 installation method
            client_install_cmd = [
                "powershell",
                "-Command",
                "Add-WindowsCapability -Online -Name 'Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0'",
            ]
            client_result = subprocess.run(
                client_install_cmd,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )

            if client_result.returncode == 0:
                self.logger.info("AD module installed via Windows capabilities")
                return self._check_ad_module()

            self.logger.error(
                "Failed to install AD module",
                server_error=server_result.stderr,
                client_error=client_result.stderr,
            )
            return False

        except Exception as e:
            self.logger.error("Error installing AD module", error=str(e))
            return False

    def _run_powershell(self, command: str) -> subprocess.CompletedProcess:
        """Execute PowerShell command and return result."""
        cmd = ["powershell", "-Command", command]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.connection_timeout,
                check=False,
            )

            if result.returncode != 0:
                self.logger.error(
                    "PowerShell command failed",
                    command=command,
                    stderr=result.stderr,
                    stdout=result.stdout,
                )

            return result
        except subprocess.TimeoutExpired:
            self.logger.error("PowerShell command timed out", command=command)
            raise PowerShellExecutionError(
                command,
                -1,
                "Command timed out",
                {"timeout": self.config.connection_timeout},
            )
        except Exception as e:
            self.logger.error(
                "PowerShell execution failed", command=command, error=str(e)
            )
            raise PowerShellExecutionError(command, -1, str(e))

    def test_connection(self) -> bool:
        """Test AD connection by running a simple PowerShell command."""
        try:
            result = self._run_powershell("Get-ADDomain")
            success = result.returncode == 0
            if success:
                self.logger.info("PowerShell AD connection test successful")
            else:
                self.logger.error(
                    "PowerShell AD connection test failed", stderr=result.stderr
                )
            return success
        except Exception as e:
            self.logger.error("PowerShell AD connection test failed", error=str(e))
            return False

    def search_user(self, username: str) -> UserInfo | None:
        """Search for a user in AD using PowerShell."""
        try:
            # Use Get-ADUser to search for the user
            command = f"Get-ADUser -Filter \"SamAccountName -eq '{username}'\" -Properties * | ConvertTo-Json -Depth 3"
            result = self._run_powershell(command)

            if result.returncode != 0:
                if "Cannot find an object with identity" in result.stderr:
                    self.logger.debug("User not found", username=username)
                    return None
                raise SearchError(f"SamAccountName -eq '{username}'", result.stderr)

            if not result.stdout.strip():
                self.logger.debug("User not found", username=username)
                return None

            # Parse JSON output
            user_data = json.loads(result.stdout)

            user_info = UserInfo(
                username=username,
                dn=user_data.get("DistinguishedName", ""),
                attributes=user_data,
                exists=True,
            )

            self.logger.debug("User found", username=username, dn=user_info.dn)
            return user_info

        except json.JSONDecodeError as e:
            self.logger.error(
                "Failed to parse PowerShell output", username=username, error=str(e)
            )
            raise SearchError(
                f"SamAccountName -eq '{username}'", f"JSON parse error: {str(e)}"
            )
        except Exception as e:
            self.logger.error(
                "PowerShell user search failed", username=username, error=str(e)
            )
            raise SearchError(f"SamAccountName -eq '{username}'", str(e))

    def user_exists(self, username: str) -> bool:
        """Check if a user exists in AD."""
        user_info = self.search_user(username)
        return user_info is not None

    def create_user(
        self,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str | None = None,
        additional_attributes: dict[str, Any] | None = None,
        resolve_conflicts: bool = True,
        dry_run: bool = False,
    ) -> UserCreationResult:
        """Create a new user in AD using PowerShell."""
        original_username = username
        conflicts_resolved = 0

        # Check if user already exists and handle conflicts
        if resolve_conflicts and self.user_exists(username):
            from .validators import UserValidator

            validator = UserValidator(self.config)
            username, conflicts_resolved = validator.resolve_username_conflict(
                username, self
            )
        elif self.user_exists(username):
            raise UserExistsError(username)

        # Build display name and UPN
        display_name = f"{first_name} {last_name}"

        # Use host from server config for UPN
        if hasattr(self.config.server, "host") and self.config.server.host:
            domain = self.config.server.host
        else:
            # For DC mode, try to get domain from AD
            try:
                domain_result = self._run_powershell("(Get-ADDomain).DNSRoot")
                if domain_result.returncode == 0 and domain_result.stdout.strip():
                    domain = domain_result.stdout.strip()
                else:
                    domain = "local.domain"  # Fallback
            except Exception:
                domain = "local.domain"  # Fallback

        upn = f"{username}@{domain}"

        # Determine target OU for user creation
        target_ou = None

        # First check if a specific default_user_ou is configured
        if (
            hasattr(self.config.server, "default_user_ou")
            and self.config.server.default_user_ou
        ):
            if (
                hasattr(self.config.server, "validate_ou_has_users")
                and self.config.server.validate_ou_has_users
            ):
                # Validate the configured OU has users
                try:
                    check_result = self._run_powershell(
                        f"Get-ADUser -SearchBase '{self.config.server.default_user_ou}' -ResultSetSize 1 -Filter * | Select-Object -First 1"
                    )
                    if check_result.returncode == 0 and check_result.stdout.strip():
                        target_ou = self.config.server.default_user_ou
                        self.logger.info(
                            "Using configured default user OU", ou=target_ou
                        )
                    else:
                        self.logger.warning(
                            "Configured default user OU is empty",
                            ou=self.config.server.default_user_ou,
                        )
                except Exception as e:
                    self.logger.warning(
                        "Error validating configured default user OU",
                        ou=self.config.server.default_user_ou,
                        error=str(e),
                    )
            else:
                target_ou = self.config.server.default_user_ou
                self.logger.info(
                    "Using configured default user OU (no validation)", ou=target_ou
                )

        # If no target OU yet and fallback is enabled, use smart detection
        if (
            not target_ou
            and hasattr(self.config.server, "fallback_to_users_container")
            and self.config.server.fallback_to_users_container
        ):
            target_ou = self.get_optimal_user_ou()
            if target_ou:
                self.logger.info("Using auto-detected optimal OU", ou=target_ou)

        # Fallback to configured base_dn
        if not target_ou:
            if self.config.server.base_dn:
                target_ou = self.config.server.base_dn
                self.logger.info("Using configured base DN", base_dn=target_ou)
            elif (
                hasattr(self.config.server, "auto_detect_base_dn")
                and self.config.server.auto_detect_base_dn
            ):
                # Auto-detect base DN as last resort
                detected_base_dn = self.get_base_dn()
                if detected_base_dn:
                    target_ou = detected_base_dn
                    self.logger.info("Using auto-detected base DN", base_dn=target_ou)

        # Final validation
        if not target_ou:
            raise UserCreationError(
                username, "Could not determine target OU for user creation"
            )

        if dry_run:
            user_dn = f"CN={display_name},{target_ou}"
            self.logger.info(
                "Dry run - would create user", username=username, dn=user_dn
            )
            return UserCreationResult(
                username=username,
                created=False,
                original_username=original_username,
                dn=user_dn,
                conflicts_resolved=conflicts_resolved,
                message="Dry run - user would be created",
            )

        try:
            # Build PowerShell command for user creation
            ps_command_parts = [
                "New-ADUser",
                f"-Name '{display_name}'",
                f"-SamAccountName '{username}'",
                f"-UserPrincipalName '{upn}'",
                f"-GivenName '{first_name}'",
                f"-Surname '{last_name}'",
                f"-EmailAddress '{email}'",
                f"-Path '{target_ou}'",
                "-Enabled $true",
            ]

            # Add password if provided
            if password:
                # Escape single quotes in password
                escaped_password = password.replace("'", "''")
                ps_command_parts.append(
                    f"-AccountPassword (ConvertTo-SecureString '{escaped_password}' -AsPlainText -Force)"
                )

            # Add additional attributes if provided
            if additional_attributes:
                for key, value in additional_attributes.items():
                    if isinstance(value, str):
                        escaped_value = value.replace("'", "''")
                        ps_command_parts.append(f"-{key} '{escaped_value}'")
                    else:
                        ps_command_parts.append(f"-{key} {value}")

            ps_command = " ".join(ps_command_parts)

            result = self._run_powershell(ps_command)

            if result.returncode != 0:
                error_msg = f"Failed to create user: {result.stderr}"
                self.logger.error(
                    "User creation failed", username=username, error=error_msg
                )
                raise UserCreationError(username, error_msg)

            # Get the created user's DN
            user_info = self.search_user(username)
            user_dn = user_info.dn if user_info else f"CN={display_name},{target_ou}"

            self.logger.info("User created successfully", username=username, dn=user_dn)
            return UserCreationResult(
                username=username,
                created=True,
                original_username=original_username,
                dn=user_dn,
                conflicts_resolved=conflicts_resolved,
                message="User created successfully",
            )

        except Exception as e:
            self.logger.error(
                "PowerShell user creation failed", username=username, error=str(e)
            )
            raise UserCreationError(username, str(e))

    def close_connections(self):
        """Close connections (no-op for PowerShell manager)."""
        self.logger.debug("PowerShell manager connections closed (no-op)")

    def __enter__(self):
        """Context manager entry."""
        return self

    def get_base_dn(self) -> str | None:
        """Get the base DN for the current domain."""
        try:
            result = self._run_powershell("(Get-ADDomain).DistinguishedName")
            if result.returncode == 0 and result.stdout.strip():
                base_dn = result.stdout.strip()
                self.logger.debug("Auto-detected base DN", base_dn=base_dn)
                return base_dn
            self.logger.warning("Failed to auto-detect base DN", stderr=result.stderr)
            return None
        except Exception as e:
            self.logger.error("Error getting base DN", error=str(e))
            return None

    def get_default_users_container(self) -> str | None:
        """Get the default users container for the current domain."""
        try:
            result = self._run_powershell("(Get-ADDomain).UsersContainer")
            if result.returncode == 0 and result.stdout.strip():
                users_container = result.stdout.strip()
                self.logger.debug(
                    "Auto-detected users container", container=users_container
                )
                return users_container
            self.logger.warning(
                "Failed to auto-detect users container", stderr=result.stderr
            )
            return None
        except Exception as e:
            self.logger.error("Error getting users container", error=str(e))
            return None

    def find_user_ous(self, validate_has_users: bool = True) -> list[str]:
        """Find OUs that contain users."""
        try:
            # Get all OUs with 'User' in the name
            result = self._run_powershell(
                "Get-ADOrganizationalUnit -Filter \"Name -like '*User*'\" | Select-Object -ExpandProperty DistinguishedName"
            )

            if result.returncode != 0:
                self.logger.warning("Failed to find user OUs", stderr=result.stderr)
                return []

            ous = [ou.strip() for ou in result.stdout.strip().split("\n") if ou.strip()]

            if not validate_has_users:
                return ous

            # Validate that each OU actually contains users
            validated_ous = []
            for ou in ous:
                try:
                    # Check if OU contains at least one user
                    check_result = self._run_powershell(
                        f"Get-ADUser -SearchBase '{ou}' -ResultSetSize 1 -Filter * | Select-Object -First 1"
                    )
                    if check_result.returncode == 0 and check_result.stdout.strip():
                        validated_ous.append(ou)
                        self.logger.debug("Validated OU contains users", ou=ou)
                    else:
                        self.logger.debug("OU contains no users", ou=ou)
                except Exception as e:
                    self.logger.debug("Error validating OU", ou=ou, error=str(e))
                    continue

            return validated_ous

        except Exception as e:
            self.logger.error("Error finding user OUs", error=str(e))
            return []

    def get_optimal_user_ou(self) -> str | None:
        """Get the optimal OU for creating users with fallback logic."""
        # First try to get the default users container
        users_container = self.get_default_users_container()
        if users_container:
            # Validate it contains users
            try:
                check_result = self._run_powershell(
                    f"Get-ADUser -SearchBase '{users_container}' -ResultSetSize 1 -Filter * | Select-Object -First 1"
                )
                if check_result.returncode == 0 and check_result.stdout.strip():
                    self.logger.info(
                        "Using default users container", container=users_container
                    )
                    return users_container
                self.logger.debug(
                    "Default users container is empty", container=users_container
                )
            except Exception as e:
                self.logger.debug(
                    "Error validating default users container", error=str(e)
                )

        # Fallback to finding OUs with users
        user_ous = self.find_user_ous(validate_has_users=True)
        if user_ous:
            selected_ou = user_ous[0]  # Use the first validated OU
            self.logger.info("Using first validated user OU", ou=selected_ou)
            return selected_ou

        # Last resort - use base DN
        base_dn = self.get_base_dn()
        if base_dn:
            self.logger.warning("Using base DN as fallback", base_dn=base_dn)
            return base_dn

        self.logger.error("Could not determine optimal user OU")
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_connections()

"""
User validation and conflict resolution for AD User Manager.
"""

import re
from typing import TYPE_CHECKING

import structlog

from .config import ADConfig
from .exceptions import ValidationError

if TYPE_CHECKING:
    from .manager import ADUserManager


class UserValidator:
    """User data validator and conflict resolver."""

    def __init__(self, config: ADConfig):
        """Initialize validator with configuration."""
        self.config = config
        self.logger = structlog.get_logger(__name__)

    def validate_username(self, username: str) -> bool:
        """Validate username format and constraints."""
        if not self.config.validate_username_format:
            return True

        # Check length
        if len(username) < self.config.username_min_length:
            raise ValidationError(
                "username",
                f"Username must be at least {self.config.username_min_length} characters long",
            )

        if len(username) > self.config.username_max_length:
            raise ValidationError(
                "username",
                f"Username must be at most {self.config.username_max_length} characters long",
            )

        # Check format (alphanumeric and common special characters)
        if not re.match(r"^[a-zA-Z0-9._-]+$", username):
            raise ValidationError(
                "username",
                "Username can only contain letters, numbers, dots, underscores, and hyphens",
            )

        # Username cannot start or end with special characters
        if username.startswith((".", "_", "-")) or username.endswith((".", "_", "-")):
            raise ValidationError(
                "username",
                "Username cannot start or end with dots, underscores, or hyphens",
            )

        return True

    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        if not self.config.require_email and not email:
            return True

        if not email:
            raise ValidationError("email", "Email address is required")

        # Basic email validation with additional checks
        # Start with standard email pattern but add specific validations
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            raise ValidationError("email", "Invalid email format")

        # Additional checks for edge cases
        if ".." in email:
            raise ValidationError("email", "Invalid email format")

        # Check that local part doesn't start or end with dot
        local_part = email.split("@")[0]
        if local_part.startswith(".") or local_part.endswith("."):
            raise ValidationError("email", "Invalid email format")

        # Check that domain part doesn't start or end with dot
        domain_part = email.split("@")[1]
        if domain_part.startswith(".") or domain_part.endswith("."):
            raise ValidationError("email", "Invalid email format")

        return True

    def validate_name(self, name: str, field_name: str) -> bool:
        """Validate first name or last name."""
        if not name or not name.strip():
            raise ValidationError(field_name, f"{field_name} is required")

        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s'-]+$", name.strip()):
            raise ValidationError(
                field_name,
                f"{field_name} can only contain letters, spaces, hyphens, and apostrophes",
            )

        return True

    def validate_user_data(
        self, username: str, first_name: str, last_name: str, email: str
    ) -> bool:
        """Validate all user data."""
        self.validate_username(username)
        self.validate_name(first_name, "first_name")
        self.validate_name(last_name, "last_name")
        self.validate_email(email)
        return True

    def resolve_username_conflict(
        self, username: str, manager: "ADUserManager"
    ) -> tuple[str, int]:
        """Resolve username conflicts by generating unique username with PowerShell optimization."""
        if not self.config.conflict_resolution.enabled:
            return username, 0

        original_username = username
        attempts = 0
        counter = self.config.conflict_resolution.start_counter

        self.logger.info(
            "Resolving username conflict", original_username=original_username
        )

        # Enhanced conflict resolution for PowerShell managers
        if hasattr(manager, "_run_powershell"):
            self.logger.debug("Using PowerShell-optimized conflict resolution")
            return self._resolve_conflict_powershell(
                original_username, manager, counter, attempts
            )

        # Standard LDAP conflict resolution
        while attempts < self.config.conflict_resolution.max_attempts:
            if not manager.user_exists(username):
                self.logger.info(
                    "Username conflict resolved",
                    original_username=original_username,
                    new_username=username,
                    attempts=attempts,
                )
                return username, attempts

            # Generate new username using pattern
            username = self.config.conflict_resolution.suffix_pattern.format(
                username=original_username, counter=counter
            )

            counter += 1
            attempts += 1

            self.logger.debug(
                "Trying new username",
                original_username=original_username,
                new_username=username,
                attempt=attempts,
            )

        # If we've exhausted all attempts, raise an error
        raise ValidationError(
            "username",
            f"Could not resolve username conflict for '{original_username}' "
            f"after {self.config.conflict_resolution.max_attempts} attempts",
        )

    def _resolve_conflict_powershell(
        self,
        original_username: str,
        manager: "ADUserManager",
        counter: int,
        attempts: int,
    ) -> tuple[str, int]:
        """PowerShell-optimized conflict resolution using batch queries."""
        # Generate multiple candidate usernames
        candidates = []
        for i in range(min(10, self.config.conflict_resolution.max_attempts)):
            candidate = self.config.conflict_resolution.suffix_pattern.format(
                username=original_username, counter=counter + i
            )
            candidates.append(candidate)

        # Build PowerShell command to check multiple users at once
        filter_parts = []
        for candidate in candidates:
            filter_parts.append(f"SamAccountName -eq '{candidate}'")

        ps_filter = " -or ".join(filter_parts)
        command = f'Get-ADUser -Filter "({ps_filter})" | Select-Object SamAccountName'

        try:
            result = manager._run_powershell(command)

            if result.returncode == 0 and result.stdout.strip():
                # Parse existing usernames from PowerShell output
                existing_usernames = set()
                for line in result.stdout.split("\n"):
                    if (
                        line.strip()
                        and "SamAccountName" not in line
                        and "---" not in line
                    ):
                        existing_usernames.add(line.strip())

                # Find first available username
                for i, candidate in enumerate(candidates):
                    if candidate not in existing_usernames:
                        self.logger.info(
                            "Username conflict resolved via PowerShell batch query",
                            original_username=original_username,
                            new_username=candidate,
                            attempts=i + 1,
                        )
                        return candidate, i + 1
            else:
                # No existing users found, use first candidate
                self.logger.info(
                    "Username conflict resolved (no existing conflicts found)",
                    original_username=original_username,
                    new_username=candidates[0],
                    attempts=1,
                )
                return candidates[0], 1

        except Exception as e:
            self.logger.warning(
                "PowerShell batch conflict resolution failed, falling back to standard method",
                error=str(e),
            )
            # Fall back to standard method
            return self._resolve_conflict_standard(
                original_username, manager, counter, attempts
            )

        # If all candidates are taken, continue with standard method
        return self._resolve_conflict_standard(
            original_username,
            manager,
            counter + len(candidates),
            attempts + len(candidates),
        )

    def _resolve_conflict_standard(
        self,
        original_username: str,
        manager: "ADUserManager",
        counter: int,
        attempts: int,
    ) -> tuple[str, int]:
        """Standard conflict resolution method."""
        username = original_username

        while attempts < self.config.conflict_resolution.max_attempts:
            if not manager.user_exists(username):
                self.logger.info(
                    "Username conflict resolved",
                    original_username=original_username,
                    new_username=username,
                    attempts=attempts,
                )
                return username, attempts

            # Generate new username using pattern
            username = self.config.conflict_resolution.suffix_pattern.format(
                username=original_username, counter=counter
            )

            counter += 1
            attempts += 1

            self.logger.debug(
                "Trying new username",
                original_username=original_username,
                new_username=username,
                attempt=attempts,
            )

        # If we've exhausted all attempts, raise an error
        raise ValidationError(
            "username",
            f"Could not resolve username conflict for '{original_username}' "
            f"after {self.config.conflict_resolution.max_attempts} attempts",
        )

    def generate_username_suggestions(
        self, first_name: str, last_name: str, count: int = 5
    ) -> list[str]:
        """Generate username suggestions based on first and last name."""
        suggestions = []

        # Clean names
        first = re.sub(r"[^a-zA-Z]", "", first_name.lower())
        last = re.sub(r"[^a-zA-Z]", "", last_name.lower())

        if not first or not last:
            return suggestions

        # Common patterns
        patterns = [
            f"{first}.{last}",
            f"{first}{last}",
            f"{first[0]}{last}",
            f"{first}{last[0]}",
            f"{last}.{first}",
            f"{last}{first}",
            f"{first[0]}.{last}",
            f"{first}.{last[0]}",
        ]

        # Add numbered variations if needed
        for pattern in patterns[:count]:
            if len(suggestions) >= count:
                break

            if (
                len(pattern) >= self.config.username_min_length
                and len(pattern) <= self.config.username_max_length
            ):
                suggestions.append(pattern)

        # If we need more suggestions, add numbered versions
        base_pattern = f"{first}.{last}"
        if (
            len(base_pattern) <= self.config.username_max_length - 2
        ):  # Leave room for numbers
            counter = 1
            while len(suggestions) < count:
                numbered_username = f"{base_pattern}{counter}"
                if len(numbered_username) <= self.config.username_max_length:
                    suggestions.append(numbered_username)
                counter += 1
                if counter > 99:  # Prevent infinite loop
                    break

        return suggestions[:count]

"""
Custom exceptions for AD User Manager.
"""


class ADUserManagerError(Exception):
    """Base exception for AD User Manager."""


class ADConnectionError(ADUserManagerError):
    """Raised when AD connection fails."""

    def __init__(self, server: str, message: str = None):
        msg = message or f"Failed to connect to AD server '{server}'"
        super().__init__(msg)
        self.server = server


class AuthenticationError(ADUserManagerError):
    """Raised when AD authentication fails."""

    def __init__(self, user: str, message: str = None):
        msg = message or f"Authentication failed for user '{user}'"
        super().__init__(msg)
        self.user = user


class UserExistsError(ADUserManagerError):
    """Raised when a user already exists and no conflict resolution is requested."""

    def __init__(self, user: str):
        msg = f"User '{user}' already exists"
        super().__init__(msg)
        self.user = user


class UserNotFoundError(ADUserManagerError):
    """Raised when a user is not found."""

    def __init__(self, user: str):
        msg = f"User '{user}' not found"
        super().__init__(msg)
        self.user = user


class ValidationError(ADUserManagerError):
    """Raised when user data validation fails."""

    def __init__(self, field: str, message: str):
        msg = f"Validation failed for field '{field}': {message}"
        super().__init__(msg)
        self.field = field


class ConfigurationError(ADUserManagerError):
    """Raised when configuration is invalid."""

    def __init__(self, message: str):
        msg = f"Configuration error: {message}"
        super().__init__(msg)
        self.message = message


class LDAPOperationError(ADUserManagerError):
    """Raised when LDAP operation fails."""

    def __init__(self, operation: str, message: str = None):
        msg = message or f"LDAP operation '{operation}' failed"
        super().__init__(msg)
        self.operation = operation


class SearchError(ADUserManagerError):
    """Raised when user search operation fails."""

    def __init__(self, search_filter: str, message: str = None):
        msg = message or f"Search failed for filter '{search_filter}'"
        super().__init__(msg)
        self.search_filter = search_filter


class UserCreationError(ADUserManagerError):
    """Raised when user creation fails."""

    def __init__(self, username: str, message: str = None):
        msg = message or f"Failed to create user '{username}'"
        super().__init__(msg)
        self.username = username


class PowerShellExecutionError(ADUserManagerError):
    """Raised when PowerShell command execution fails."""

    def __init__(
        self, command: str, return_code: int, stderr: str = None, details: dict = None
    ):
        msg = f"PowerShell command failed with exit code {return_code}: {command}"
        if stderr:
            msg += f" (Error: {stderr})"
        super().__init__(msg)
        self.command = command
        self.return_code = return_code
        self.stderr = stderr
        self.details = details or {}


class RetryableError(ADUserManagerError):
    """Raised for errors that might succeed if retried."""

    def __init__(self, message: str, retry_after: int = None, details: dict = None):
        super().__init__(message)
        self.retry_after = retry_after  # seconds
        self.details = details or {}


class ADPermissionError(ADUserManagerError):
    """Raised when insufficient permissions for AD operations."""

    def __init__(
        self, operation: str, required_permission: str = None, details: dict = None
    ):
        msg = f"Insufficient permissions for operation: {operation}"
        if required_permission:
            msg += f" (Required: {required_permission})"
        super().__init__(msg)
        self.operation = operation
        self.required_permission = required_permission
        self.details = details or {}

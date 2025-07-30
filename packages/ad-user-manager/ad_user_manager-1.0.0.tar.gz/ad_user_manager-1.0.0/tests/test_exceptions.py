"""
Tests for AD User Manager custom exceptions.
"""

from ad_user_manager.exceptions import (ADConnectionError, ADPermissionError,
                                        ADUserManagerError,
                                        AuthenticationError,
                                        ConfigurationError, LDAPOperationError,
                                        PowerShellExecutionError,
                                        RetryableError, SearchError,
                                        UserCreationError, UserExistsError,
                                        UserNotFoundError, ValidationError)


class TestADUserManagerError:
    def test_base_exception(self):
        error = ADUserManagerError("Base error message")
        assert str(error) == "Base error message"
        assert isinstance(error, Exception)


class TestADConnectionError:
    def test_with_default_message(self):
        error = ADConnectionError("server.example.com")
        assert "Failed to connect to AD server 'server.example.com'" in str(error)
        assert error.server == "server.example.com"

    def test_with_custom_message(self):
        error = ADConnectionError("server.example.com", "Custom connection error")
        assert str(error) == "Custom connection error"
        assert error.server == "server.example.com"


class TestAuthenticationError:
    def test_with_default_message(self):
        error = AuthenticationError("admin@example.com")
        assert "Authentication failed for user 'admin@example.com'" in str(error)
        assert error.user == "admin@example.com"

    def test_with_custom_message(self):
        error = AuthenticationError("admin@example.com", "Invalid credentials")
        assert str(error) == "Invalid credentials"
        assert error.user == "admin@example.com"


class TestUserExistsError:
    def test_error_message(self):
        error = UserExistsError("test_user")
        assert str(error) == "User 'test_user' already exists"
        assert error.user == "test_user"


class TestUserNotFoundError:
    def test_error_message(self):
        error = UserNotFoundError("missing_user")
        assert str(error) == "User 'missing_user' not found"
        assert error.user == "missing_user"


class TestValidationError:
    def test_error_message(self):
        error = ValidationError("email", "Invalid email format")
        assert str(error) == "Validation failed for field 'email': Invalid email format"
        assert error.field == "email"


class TestConfigurationError:
    def test_error_message(self):
        error = ConfigurationError("Missing required field")
        assert str(error) == "Configuration error: Missing required field"
        assert error.message == "Missing required field"


class TestLDAPOperationError:
    def test_with_default_message(self):
        error = LDAPOperationError("bind")
        assert str(error) == "LDAP operation 'bind' failed"
        assert error.operation == "bind"

    def test_with_custom_message(self):
        error = LDAPOperationError("search", "Search returned no results")
        assert str(error) == "Search returned no results"
        assert error.operation == "search"


class TestSearchError:
    def test_with_default_message(self):
        error = SearchError("(sAMAccountName=testuser)")
        assert "Search failed for filter '(sAMAccountName=testuser)'" in str(error)
        assert error.search_filter == "(sAMAccountName=testuser)"

    def test_with_custom_message(self):
        error = SearchError("(uid=test)", "No results found")
        assert str(error) == "No results found"
        assert error.search_filter == "(uid=test)"


class TestUserCreationError:
    def test_with_default_message(self):
        error = UserCreationError("test_user")
        assert str(error) == "Failed to create user 'test_user'"
        assert error.username == "test_user"

    def test_with_custom_message(self):
        error = UserCreationError("test_user", "Insufficient permissions")
        assert str(error) == "Insufficient permissions"
        assert error.username == "test_user"


class TestPowerShellExecutionError:
    def test_basic_error(self):
        error = PowerShellExecutionError("Get-ADUser test", 1)
        assert "PowerShell command failed with exit code 1: Get-ADUser test" in str(
            error
        )
        assert error.command == "Get-ADUser test"
        assert error.return_code == 1
        assert error.stderr is None
        assert error.details == {}

    def test_with_stderr(self):
        error = PowerShellExecutionError("Get-ADUser test", 1, "User not found")
        assert "Error: User not found" in str(error)
        assert error.stderr == "User not found"

    def test_with_details(self):
        details = {"module": "ActiveDirectory", "error_type": "ObjectNotFound"}
        error = PowerShellExecutionError("Get-ADUser test", 1, details=details)
        assert error.details == details


class TestRetryableError:
    def test_basic_error(self):
        error = RetryableError("Temporary network error")
        assert str(error) == "Temporary network error"
        assert error.retry_after is None
        assert error.details == {}

    def test_with_retry_after(self):
        error = RetryableError("Rate limited", retry_after=60)
        assert error.retry_after == 60

    def test_with_details(self):
        details = {"rate_limit": "5 requests per minute"}
        error = RetryableError("Rate limited", details=details)
        assert error.details == details


class TestADPermissionError:
    def test_basic_error(self):
        error = ADPermissionError("create_user")
        assert "Insufficient permissions for operation: create_user" in str(error)
        assert error.operation == "create_user"
        assert error.required_permission is None
        assert error.details == {}

    def test_with_required_permission(self):
        error = ADPermissionError("create_user", "Account Operators")
        assert "Required: Account Operators" in str(error)
        assert error.required_permission == "Account Operators"

    def test_with_details(self):
        details = {"current_user": "test@example.com", "domain": "example.com"}
        error = ADPermissionError("create_user", details=details)
        assert error.details == details

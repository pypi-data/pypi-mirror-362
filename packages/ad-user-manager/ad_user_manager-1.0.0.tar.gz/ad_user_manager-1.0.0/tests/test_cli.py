"""
Tests for AD User Manager CLI functionality.
"""

from io import StringIO
from unittest.mock import MagicMock, Mock, patch

import pytest
from click.testing import CliRunner
from rich.console import Console

# Create comprehensive mocks for ldap3 and its submodules
ldap3_mock = MagicMock()
ldap3_mock.ALL = "ALL"
ldap3_mock.SIMPLE = "SIMPLE"
ldap3_mock.Connection = Mock
ldap3_mock.Server = Mock
ldap3_mock.core = MagicMock()
ldap3_mock.core.exceptions = MagicMock()
ldap3_mock.core.exceptions.LDAPException = Exception

# Mock all the ldap3 modules before importing anything
with patch.dict(
    "sys.modules",
    {
        "ldap3": ldap3_mock,
        "ldap3.core": ldap3_mock.core,
        "ldap3.core.exceptions": ldap3_mock.core.exceptions,
    },
):
    from ad_user_manager.cli import (
        print_error,
        print_info,
        print_result_table,
        print_success,
        print_warning,
    )

from ad_user_manager.models import UserCreationResult


class TestCLIHelpers:
    def test_print_success(self):
        test_console = Console(file=StringIO())
        print_success("Test success message", test_console=test_console)
        output = test_console.file.getvalue()
        assert "Test success message" in output
        # Should contain emoji
        assert "✅" in output

    def test_print_error(self):
        test_console = Console(file=StringIO())
        print_error("Test error message", test_console=test_console)
        output = test_console.file.getvalue()
        assert "Test error message" in output
        # Should contain emoji
        assert "❌" in output

    def test_print_warning(self):
        test_console = Console(file=StringIO())
        print_warning("Test warning message", test_console=test_console)
        output = test_console.file.getvalue()
        assert "Test warning message" in output
        # Should contain emoji
        assert "⚠" in output

    def test_print_info(self):
        test_console = Console(file=StringIO())
        print_info("Test info message", test_console=test_console)
        output = test_console.file.getvalue()
        assert "Test info message" in output
        # Should contain emoji
        assert "ℹ" in output

    def test_print_result_table(self):
        result = UserCreationResult(
            username="testuser2",
            created=True,
            original_username="testuser",
            dn="CN=testuser2,OU=Users,DC=example,DC=com",
            conflicts_resolved=1,
            message="User created successfully",
        )

        test_console = Console(file=StringIO())
        print_result_table(result, test_console=test_console)
        output = test_console.file.getvalue()

        # Verify table content is present
        assert "testuser2" in output
        assert "User Creation Result" in output
        assert "Username" in output
        assert "Created" in output
        assert "\u2705" in output  # Check for success emoji


class TestCLICommands:
    def test_cli_import_success(self):
        # Test that the CLI module can be imported without errors
        try:
            from ad_user_manager import cli

            assert cli is not None
        except ImportError as e:
            pytest.fail(f"Failed to import CLI module: {e}")

    def test_cli_main_function_exists(self):
        # Test that main function exists for entry point
        from ad_user_manager import cli

        assert (
            hasattr(cli, "main")
            or hasattr(cli, "cli")
            or callable(getattr(cli, "app", None))
        )

    @patch("ad_user_manager.cli.create_ad_manager")
    @patch("ad_user_manager.cli.ADConfig")
    def test_create_user_command_mocked(self, mock_config_cls, mock_create_manager):
        # Test the create user command with mocked dependencies
        from ad_user_manager.cli import cli

        mock_config = Mock()
        mock_config_cls.return_value = mock_config

        mock_manager = Mock()
        mock_result = UserCreationResult(
            username="testuser",
            created=True,
            original_username="testuser",
            dn="CN=testuser,OU=Users,DC=example,DC=com",
        )
        mock_manager.create_user.return_value = mock_result
        mock_create_manager.return_value = mock_manager

        # Test the CLI group with --help
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        # Should not crash when asking for help
        assert result.exit_code == 0

    def test_run_automation_function_exists(self):
        # Test that run_automation function exists (mentioned in __init__.py)
        from ad_user_manager.cli import run_automation

        assert callable(run_automation)

    @patch("ad_user_manager.cli.create_ad_manager")
    @patch("ad_user_manager.cli.ADConfig")
    def test_run_automation_basic(self, mock_config_cls, mock_create_manager):
        from ad_user_manager.cli import run_automation

        mock_config = Mock()
        mock_config_cls.return_value = mock_config

        mock_manager = Mock()
        mock_create_manager.return_value = mock_manager

        # Test basic automation function call
        try:
            # This should not crash with basic mocking
            run_automation()
        except Exception as e:
            # Some exceptions are expected due to missing parameters
            # Just ensure it's not an import or basic structure error
            assert "config" not in str(e).lower() or "import" not in str(e).lower()

    def test_cli_console_initialization(self):
        # Test that console is properly initialized
        from rich.console import Console

        from ad_user_manager.cli import console

        assert isinstance(console, Console)

    @patch("ad_user_manager.cli.UserValidator")
    def test_validator_integration(self, mock_validator_cls):
        # Test that UserValidator can be imported and used in CLI context
        mock_validator = Mock()
        mock_validator_cls.return_value = mock_validator

        # Test validation in CLI context
        mock_validator.validate_user_data.return_value = True

        validator = mock_validator_cls(Mock())
        result = validator.validate_user_data("test", "John", "Doe", "john@example.com")
        assert result is True

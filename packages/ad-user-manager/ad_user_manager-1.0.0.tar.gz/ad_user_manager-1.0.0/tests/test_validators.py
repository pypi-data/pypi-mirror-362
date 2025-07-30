"""
Tests for AD User Manager validators.
"""

from unittest.mock import Mock

import pytest

from ad_user_manager.config import ADConfig
from ad_user_manager.exceptions import ValidationError
from ad_user_manager.models import ConflictResolutionConfig
from ad_user_manager.validators import UserValidator


class TestUserValidator:
    def get_test_config(self, **overrides):
        base_config = {
            "server": {
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            },
            "validate_username_format": True,
            "username_min_length": 3,
            "username_max_length": 20,
            "require_email": True,
        }
        base_config.update(overrides)
        return ADConfig(**base_config)

    def test_init(self):
        config = self.get_test_config()
        validator = UserValidator(config)
        assert validator.config == config
        assert validator.logger is not None

    def test_validate_username_success(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        assert validator.validate_username("testuser") is True
        assert validator.validate_username("test.user") is True
        assert validator.validate_username("test_user") is True
        assert validator.validate_username("test-user") is True
        assert validator.validate_username("test123") is True

    def test_validate_username_disabled(self):
        config = self.get_test_config(validate_username_format=False)
        validator = UserValidator(config)

        assert validator.validate_username("") is True
        assert validator.validate_username("@#$%") is True

    def test_validate_username_too_short(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        with pytest.raises(ValidationError) as excinfo:
            validator.validate_username("ab")
        assert "at least 3 characters" in str(excinfo.value)

    def test_validate_username_too_long(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        with pytest.raises(ValidationError) as excinfo:
            validator.validate_username("a" * 21)
        assert "at most 20 characters" in str(excinfo.value)

    def test_validate_username_invalid_characters(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        with pytest.raises(ValidationError) as excinfo:
            validator.validate_username("test@user")
        assert "can only contain letters, numbers" in str(excinfo.value)

    def test_validate_username_invalid_start_end(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        invalid_usernames = [
            ".testuser",
            "_testuser",
            "-testuser",
            "testuser.",
            "testuser_",
            "testuser-",
        ]

        for username in invalid_usernames:
            with pytest.raises(ValidationError) as excinfo:
                validator.validate_username(username)
            assert "cannot start or end with" in str(excinfo.value)

    def test_validate_email_success(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        assert validator.validate_email("test@example.com") is True
        assert validator.validate_email("user.name+tag@domain.co.uk") is True

    def test_validate_email_not_required(self):
        config = self.get_test_config(require_email=False)
        validator = UserValidator(config)

        assert validator.validate_email("") is True
        assert validator.validate_email(None) is True

    def test_validate_email_required_but_empty(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        with pytest.raises(ValidationError) as excinfo:
            validator.validate_email("")
        assert "Email address is required" in str(excinfo.value)

    def test_validate_email_invalid_format(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        invalid_emails = [
            "invalid",
            "@example.com",
            "test@",
            "test@com",
            "test..user@example.com",
        ]

        for email in invalid_emails:
            with pytest.raises(ValidationError) as excinfo:
                validator.validate_email(email)
            assert "Invalid email format" in str(excinfo.value)

    def test_validate_name_success(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        assert validator.validate_name("John", "first_name") is True
        assert validator.validate_name("O'Connor", "last_name") is True
        assert validator.validate_name("Mary-Jane", "first_name") is True
        assert validator.validate_name("Van Der Berg", "last_name") is True

    def test_validate_name_empty(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        with pytest.raises(ValidationError) as excinfo:
            validator.validate_name("", "first_name")
        assert "first_name is required" in str(excinfo.value)

    def test_validate_name_invalid_characters(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        with pytest.raises(ValidationError) as excinfo:
            validator.validate_name("John123", "first_name")
        assert "can only contain letters, spaces" in str(excinfo.value)

    def test_validate_user_data_success(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        assert (
            validator.validate_user_data("testuser", "John", "Doe", "john@example.com")
            is True
        )

    def test_validate_user_data_failures(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        with pytest.raises(ValidationError):
            validator.validate_user_data("ab", "John", "Doe", "john@example.com")

    def test_resolve_username_conflict_disabled(self):
        conflict_config = ConflictResolutionConfig(enabled=False)
        config = self.get_test_config(conflict_resolution=conflict_config)
        validator = UserValidator(config)

        mock_manager = Mock()
        result_username, attempts = validator.resolve_username_conflict(
            "testuser", mock_manager
        )

        assert result_username == "testuser"
        assert attempts == 0

    def test_resolve_username_conflict_ldap_success(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        mock_manager = Mock()
        mock_manager.user_exists.side_effect = [
            True,
            False,
        ]  # First exists, second doesn't

        result_username, attempts = validator.resolve_username_conflict(
            "testuser", mock_manager
        )

        assert result_username == "testuser1"
        assert attempts == 1

    def test_resolve_username_conflict_powershell_success(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        mock_manager = Mock()
        mock_manager._run_powershell.return_value = Mock(
            returncode=0, stdout="SamAccountName\n--------------\ntestuser1"
        )

        result_username, attempts = validator.resolve_username_conflict(
            "testuser", mock_manager
        )

        assert result_username == "testuser2"
        assert attempts == 2

    def test_resolve_username_conflict_max_attempts(self):
        # Use the existing get_test_config method which works
        config = self.get_test_config()
        # Manually patch the max_attempts to 2 since we can't use conflicts in init
        config.conflict_resolution.max_attempts = 2
        validator = UserValidator(config)

        mock_manager = Mock()
        # Ensure this is treated as LDAP manager (no _run_powershell attribute)
        if hasattr(mock_manager, "_run_powershell"):
            delattr(mock_manager, "_run_powershell")
        mock_manager.user_exists.return_value = True  # Always exists

        with pytest.raises(ValidationError) as excinfo:
            validator.resolve_username_conflict("testuser", mock_manager)
        assert "Could not resolve username conflict" in str(excinfo.value)

    def test_generate_username_suggestions_basic(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        suggestions = validator.generate_username_suggestions("John", "Doe", 5)

        assert len(suggestions) == 5
        assert "john.doe" in suggestions
        assert "johndoe" in suggestions
        assert "jdoe" in suggestions

    def test_generate_username_suggestions_empty_names(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        suggestions = validator.generate_username_suggestions("", "Doe", 5)
        assert suggestions == []

        suggestions = validator.generate_username_suggestions("John", "", 5)
        assert suggestions == []

    def test_generate_username_suggestions_special_characters(self):
        config = self.get_test_config()
        validator = UserValidator(config)

        suggestions = validator.generate_username_suggestions(
            "Mary-Jane", "O'Connor", 3
        )

        # Should clean special characters
        assert len(suggestions) > 0
        for suggestion in suggestions:
            assert "'" not in suggestion
            assert "-" not in suggestion or suggestion.count("-") == 1  # Only separator

    def test_generate_username_suggestions_length_constraints(self):
        config = self.get_test_config(username_min_length=5, username_max_length=8)
        validator = UserValidator(config)

        suggestions = validator.generate_username_suggestions("John", "Doe", 5)

        for suggestion in suggestions:
            assert len(suggestion) >= 5
            assert len(suggestion) <= 8

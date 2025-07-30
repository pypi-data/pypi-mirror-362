"""
Tests for AD User Manager models.
"""

import pytest
from pydantic import ValidationError

from ad_user_manager.config import ADConfig
from ad_user_manager.models import (ConflictResolutionConfig, DCServerConfig,
                                    LDAPServerConfig, UserAttributeMapping,
                                    UserCreationResult, UserInfo)


class TestUserCreationResult:
    def test_basic_creation(self):
        result = UserCreationResult(
            username="test_user",
            created=True,
            original_username="test_user",
            dn="CN=test_user,OU=Users,DC=example,DC=com",
        )
        assert result.username == "test_user"
        assert result.created is True
        assert result.conflicts_resolved == 0
        assert result.message == ""

    def test_with_conflicts_resolved(self):
        result = UserCreationResult(
            username="test_user2",
            created=True,
            original_username="test_user",
            dn="CN=test_user2,OU=Users,DC=example,DC=com",
            conflicts_resolved=2,
            message="Username conflict resolved",
        )
        assert result.conflicts_resolved == 2
        assert result.message == "Username conflict resolved"


class TestUserInfo:
    def test_basic_creation(self):
        user_info = UserInfo(
            username="test_user",
            dn="CN=test_user,OU=Users,DC=example,DC=com",
            attributes={"sAMAccountName": "test_user", "mail": "test@example.com"},
        )
        assert user_info.username == "test_user"
        assert user_info.exists is True
        assert user_info.attributes["mail"] == "test@example.com"

    def test_non_existing_user(self):
        user_info = UserInfo(username="test_user", dn="", attributes={}, exists=False)
        assert user_info.exists is False


class TestDCServerConfig:
    def test_minimal_config(self):
        config = DCServerConfig(base_dn="DC=example,DC=com")
        assert config.connection_type == "domain_controller"
        assert config.base_dn == "DC=example,DC=com"
        assert config.use_current_credentials is True
        assert config.host == ""

    def test_full_config(self):
        config = DCServerConfig(
            base_dn="DC=example,DC=com",
            host="dc.example.com",
            use_current_credentials=False,
            service_account="admin@example.com",
            service_password="password123",
        )
        assert config.host == "dc.example.com"
        assert config.use_current_credentials is False
        assert config.service_account == "admin@example.com"

    def test_empty_base_dn_with_auto_detect(self):
        """Test that empty base_dn is allowed when auto_detect_base_dn is True."""
        config = DCServerConfig(base_dn="", auto_detect_base_dn=True)
        assert config.base_dn == ""
        assert config.auto_detect_base_dn is True
        assert config.connection_type == "domain_controller"

    def test_empty_base_dn_without_auto_detect(self):
        """Test that empty base_dn should be validated when auto_detect_base_dn is False."""
        # This test will pass at the model level, but will fail in ADConfig validation
        config = DCServerConfig(base_dn="", auto_detect_base_dn=False)
        assert config.base_dn == ""
        assert config.auto_detect_base_dn is False


class TestLDAPServerConfig:
    def test_minimal_config(self):
        config = LDAPServerConfig(
            base_dn="DC=example,DC=com",
            host="ldap.example.com",
            bind_dn="admin@example.com",
            bind_password="password123",
        )
        assert config.connection_type == "ldap"
        assert config.port == 389
        assert config.use_ssl is False

    def test_ssl_config(self):
        config = LDAPServerConfig(
            base_dn="DC=example,DC=com",
            host="ldap.example.com",
            port=636,
            use_ssl=True,
            bind_dn="admin@example.com",
            bind_password="password123",
        )
        assert config.port == 636
        assert config.use_ssl is True

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            LDAPServerConfig(base_dn="DC=example,DC=com")


class TestUserAttributeMapping:
    def test_default_mapping(self):
        mapping = UserAttributeMapping()
        assert mapping.username_field == "sAMAccountName"
        assert mapping.first_name_field == "givenName"
        assert mapping.last_name_field == "sn"
        assert mapping.email_field == "mail"
        assert mapping.object_class == ["top", "person", "organizationalPerson", "user"]

    def test_custom_mapping(self):
        mapping = UserAttributeMapping(
            username_field="uid",
            email_field="emailAddress",
            object_class=["top", "person", "inetOrgPerson"],
        )
        assert mapping.username_field == "uid"
        assert mapping.email_field == "emailAddress"
        assert mapping.object_class == ["top", "person", "inetOrgPerson"]


class TestConflictResolutionConfig:
    def test_default_config(self):
        config = ConflictResolutionConfig()
        assert config.enabled is True
        assert config.max_attempts == 100
        assert config.suffix_pattern == "{username}{counter}"
        assert config.start_counter == 1

    def test_custom_config(self):
        config = ConflictResolutionConfig(
            enabled=False,
            max_attempts=50,
            suffix_pattern="{username}_{counter}",
            start_counter=0,
        )
        assert config.enabled is False
        assert config.max_attempts == 50
        assert config.suffix_pattern == "{username}_{counter}"
        assert config.start_counter == 0


class TestADConfigIntegration:
    """Test ADConfig validation with different server configurations."""

    def test_dc_config_with_base_dn_and_auto_detect_true(self):
        """Test ADConfig accepts DC config with base_dn and auto_detect_base_dn=True."""
        server_config = DCServerConfig(
            base_dn="DC=example,DC=com", auto_detect_base_dn=True
        )
        config = ADConfig(server=server_config)
        assert config.server.base_dn == "DC=example,DC=com"
        assert config.server.auto_detect_base_dn is True

    def test_dc_config_with_base_dn_and_auto_detect_false(self):
        """Test ADConfig accepts DC config with base_dn and auto_detect_base_dn=False."""
        server_config = DCServerConfig(
            base_dn="DC=example,DC=com", auto_detect_base_dn=False
        )
        config = ADConfig(server=server_config)
        assert config.server.base_dn == "DC=example,DC=com"
        assert config.server.auto_detect_base_dn is False

    def test_dc_config_empty_base_dn_with_auto_detect_true(self):
        """Test ADConfig accepts DC config with empty base_dn when auto_detect_base_dn=True."""
        server_config = DCServerConfig(base_dn="", auto_detect_base_dn=True)
        config = ADConfig(server=server_config)
        assert config.server.base_dn == ""
        assert config.server.auto_detect_base_dn is True

    def test_dc_config_empty_base_dn_with_auto_detect_false_should_fail(self):
        """Test ADConfig rejects DC config with empty base_dn when auto_detect_base_dn=False."""
        server_config = DCServerConfig(base_dn="", auto_detect_base_dn=False)
        with pytest.raises(ValidationError) as exc_info:
            ADConfig(server=server_config)

        assert (
            "Base DN is required for DC configuration when auto_detect_base_dn is False"
            in str(exc_info.value)
        )

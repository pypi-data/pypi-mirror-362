"""
Tests for AD User Manager configuration.
"""

import pytest
from pydantic import ValidationError

from ad_user_manager.config import ADConfig
from ad_user_manager.models import (ConflictResolutionConfig,
                                    UserAttributeMapping)


class TestADConfig:
    def test_minimal_dc_config(self):
        config = ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            }
        )
        assert config.server.connection_type == "domain_controller"
        assert config.server.base_dn == "DC=example,DC=com"
        assert config.connection_timeout == 30
        assert config.log_level == "INFO"
        assert config.require_email is True

    def test_minimal_ldap_config(self):
        config = ADConfig(
            server={
                "connection_type": "ldap",
                "base_dn": "DC=example,DC=com",
                "host": "ldap.example.com",
                "bind_dn": "admin@example.com",
                "bind_password": "password123",
            }
        )
        assert config.server.connection_type == "ldap"
        assert config.server.host == "ldap.example.com"

    def test_custom_config_values(self):
        custom_attributes = UserAttributeMapping(username_field="uid")
        custom_conflict = ConflictResolutionConfig(enabled=False)

        config = ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            },
            attributes=custom_attributes,
            conflict_resolution=custom_conflict,
            connection_timeout=60,
            log_level="DEBUG",
            require_email=False,
        )

        assert config.attributes.username_field == "uid"
        assert config.conflict_resolution.enabled is False
        assert config.connection_timeout == 60
        assert config.log_level == "DEBUG"
        assert config.require_email is False

    def test_dc_config_validation_with_service_account(self):
        config = ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
                "use_current_credentials": False,
                "service_account": "admin@example.com",
                "service_password": "password123",
            }
        )
        assert config.server.use_current_credentials is False
        assert config.server.service_account == "admin@example.com"

    def test_dc_config_validation_fails_without_credentials(self):
        with pytest.raises(ValidationError) as excinfo:
            ADConfig(
                server={
                    "connection_type": "domain_controller",
                    "base_dn": "DC=example,DC=com",
                    "use_current_credentials": False,
                }
            )
        assert "Service account credentials required" in str(excinfo.value)

    def test_dc_config_validation_fails_without_base_dn(self):
        with pytest.raises(ValidationError) as excinfo:
            ADConfig(server={"connection_type": "domain_controller", "base_dn": ""})
        assert "Base DN is required" in str(excinfo.value)

    def test_ldap_config_validation_fails_missing_fields(self):
        with pytest.raises(ValidationError) as excinfo:
            ADConfig(server={"connection_type": "ldap", "base_dn": "DC=example,DC=com"})
        assert "Field required" in str(excinfo.value)

    def test_log_level_validation_success(self):
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            config = ADConfig(
                server={
                    "connection_type": "domain_controller",
                    "base_dn": "DC=example,DC=com",
                },
                log_level=level.lower(),
            )
            assert config.log_level == level

    def test_log_level_validation_fails(self):
        with pytest.raises(ValidationError) as excinfo:
            ADConfig(
                server={
                    "connection_type": "domain_controller",
                    "base_dn": "DC=example,DC=com",
                },
                log_level="INVALID",
            )
        assert "Log level must be one of" in str(excinfo.value)

    def test_log_format_validation_success(self):
        for format_type in ["json", "console"]:
            config = ADConfig(
                server={
                    "connection_type": "domain_controller",
                    "base_dn": "DC=example,DC=com",
                },
                log_format=format_type.upper(),
            )
            assert config.log_format == format_type

    def test_log_format_validation_fails(self):
        with pytest.raises(ValidationError) as excinfo:
            ADConfig(
                server={
                    "connection_type": "domain_controller",
                    "base_dn": "DC=example,DC=com",
                },
                log_format="xml",
            )
        assert "Log format must be one of" in str(excinfo.value)

    def test_default_factory_values(self):
        config = ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            }
        )

        assert isinstance(config.attributes, UserAttributeMapping)
        assert config.attributes.username_field == "sAMAccountName"

        assert isinstance(config.conflict_resolution, ConflictResolutionConfig)
        assert config.conflict_resolution.enabled is True

    def test_all_default_values(self):
        config = ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            }
        )

        assert config.connection_timeout == 30
        assert config.search_timeout == 30
        assert config.pool_size == 5
        assert config.pool_keepalive == 60
        assert config.log_level == "INFO"
        assert config.log_format == "json"
        assert config.require_email is True
        assert config.validate_username_format is True
        assert config.username_min_length == 3
        assert config.username_max_length == 20

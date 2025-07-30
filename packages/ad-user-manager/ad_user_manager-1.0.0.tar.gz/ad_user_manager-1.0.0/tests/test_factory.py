"""
Tests for AD User Manager factory function.
"""

from unittest.mock import Mock, patch

import pytest

from ad_user_manager.config import ADConfig
from ad_user_manager.factory import create_ad_manager


class TestCreateADManager:
    def test_create_powershell_manager_success(self):
        config = ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            }
        )

        with patch(
            "ad_user_manager.powershell_manager.PowerShellADManager"
        ) as mock_ps_manager:
            mock_instance = Mock()
            mock_ps_manager.return_value = mock_instance

            result = create_ad_manager(config)

            assert result == mock_instance
            mock_ps_manager.assert_called_once_with(config)

    def test_create_ldap_manager_success(self):
        config = ADConfig(
            server={
                "connection_type": "ldap",
                "base_dn": "DC=example,DC=com",
                "host": "ldap.example.com",
                "bind_dn": "admin@example.com",
                "bind_password": "password123",
            }
        )

        with patch("ad_user_manager.ldap_manager.ADUserManager") as mock_ldap_manager:
            mock_instance = Mock()
            mock_ldap_manager.return_value = mock_instance

            result = create_ad_manager(config)

            assert result == mock_instance
            mock_ldap_manager.assert_called_once_with(config)

    def test_create_powershell_manager_failure(self):
        config = ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            }
        )

        with patch(
            "ad_user_manager.powershell_manager.PowerShellADManager"
        ) as mock_ps_manager:
            mock_ps_manager.side_effect = Exception("PowerShell not available")

            with pytest.raises(Exception) as excinfo:
                create_ad_manager(config)

            assert "Failed to create PowerShell AD manager" in str(excinfo.value)

    def test_create_ldap_manager_failure(self):
        config = ADConfig(
            server={
                "connection_type": "ldap",
                "base_dn": "DC=example,DC=com",
                "host": "ldap.example.com",
                "bind_dn": "admin@example.com",
                "bind_password": "password123",
            }
        )

        with patch("ad_user_manager.ldap_manager.ADUserManager") as mock_ldap_manager:
            mock_ldap_manager.side_effect = Exception("LDAP connection failed")

            with pytest.raises(Exception) as excinfo:
                create_ad_manager(config)

            assert "Failed to create LDAP AD manager" in str(excinfo.value)

    def test_fallback_powershell_success(self):
        config = ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            }
        )

        # Mock an unknown server type by patching isinstance
        with patch("ad_user_manager.factory.isinstance") as mock_isinstance:
            mock_isinstance.return_value = (
                False  # Not DCServerConfig or LDAPServerConfig
            )

            with patch(
                "ad_user_manager.powershell_manager.PowerShellADManager"
            ) as mock_ps_manager:
                mock_instance = Mock()
                mock_ps_manager.return_value = mock_instance

                result = create_ad_manager(config)

                assert result == mock_instance

    def test_fallback_to_ldap_success(self):
        config = ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            }
        )

        with patch("ad_user_manager.factory.isinstance") as mock_isinstance:
            mock_isinstance.return_value = False

            with patch(
                "ad_user_manager.powershell_manager.PowerShellADManager"
            ) as mock_ps_manager:
                mock_ps_manager.side_effect = Exception("PowerShell not available")

                with patch(
                    "ad_user_manager.ldap_manager.ADUserManager"
                ) as mock_ldap_manager:
                    mock_instance = Mock()
                    mock_ldap_manager.return_value = mock_instance

                    result = create_ad_manager(config)

                    assert result == mock_instance

    def test_fallback_both_fail(self):
        config = ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            }
        )

        with patch("ad_user_manager.factory.isinstance") as mock_isinstance:
            mock_isinstance.return_value = False

            with patch(
                "ad_user_manager.powershell_manager.PowerShellADManager"
            ) as mock_ps_manager:
                mock_ps_manager.side_effect = Exception("PowerShell not available")

                with patch(
                    "ad_user_manager.ldap_manager.ADUserManager"
                ) as mock_ldap_manager:
                    mock_ldap_manager.side_effect = Exception("LDAP connection failed")

                    with pytest.raises(Exception) as excinfo:
                        create_ad_manager(config)

                    assert "Failed to create any AD manager" in str(excinfo.value)
                    assert "PowerShell: PowerShell not available" in str(excinfo.value)
                    assert "LDAP: LDAP connection failed" in str(excinfo.value)

    def test_logging_powershell_creation(self):
        config = ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            }
        )

        with patch(
            "ad_user_manager.powershell_manager.PowerShellADManager"
        ) as mock_ps_manager:
            mock_instance = Mock()
            mock_ps_manager.return_value = mock_instance

            with patch("ad_user_manager.factory.structlog.get_logger") as mock_logger:
                mock_log = Mock()
                mock_logger.return_value = mock_log

                create_ad_manager(config)

                mock_log.info.assert_called_with(
                    "Creating PowerShell AD manager for domain controller"
                )

    def test_logging_ldap_creation(self):
        config = ADConfig(
            server={
                "connection_type": "ldap",
                "base_dn": "DC=example,DC=com",
                "host": "ldap.example.com",
                "bind_dn": "admin@example.com",
                "bind_password": "password123",
            }
        )

        with patch("ad_user_manager.ldap_manager.ADUserManager") as mock_ldap_manager:
            mock_instance = Mock()
            mock_ldap_manager.return_value = mock_instance

            with patch("ad_user_manager.factory.structlog.get_logger") as mock_logger:
                mock_log = Mock()
                mock_logger.return_value = mock_log

                create_ad_manager(config)

                mock_log.info.assert_called_with(
                    "Creating LDAP AD manager for remote connection"
                )

    def test_logging_fallback_warning(self):
        config = ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            }
        )

        with patch("ad_user_manager.factory.isinstance") as mock_isinstance:
            mock_isinstance.return_value = False

            with patch(
                "ad_user_manager.powershell_manager.PowerShellADManager"
            ) as mock_ps_manager:
                mock_instance = Mock()
                mock_ps_manager.return_value = mock_instance

                with patch(
                    "ad_user_manager.factory.structlog.get_logger"
                ) as mock_logger:
                    mock_log = Mock()
                    mock_logger.return_value = mock_log

                    create_ad_manager(config)

                    mock_log.warning.assert_called_with(
                        "Unknown server configuration type, attempting auto-detection"
                    )

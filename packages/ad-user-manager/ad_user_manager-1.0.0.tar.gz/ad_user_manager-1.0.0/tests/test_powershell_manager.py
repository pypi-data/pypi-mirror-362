"""
Tests for AD User Manager PowerShell manager.
"""

from unittest.mock import MagicMock, Mock, patch

import pytest

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
    from ad_user_manager.config import ADConfig
    from ad_user_manager.exceptions import UserExistsError
    from ad_user_manager.models import UserCreationResult, UserInfo
    from ad_user_manager.powershell_manager import PowerShellADManager


class TestPowerShellADManager:
    def get_test_config(self):
        return ADConfig(
            server={
                "connection_type": "domain_controller",
                "base_dn": "DC=example,DC=com",
            },
            log_level="INFO",
        )

    @patch("ad_user_manager.powershell_manager.platform.system")
    def test_init_success_windows(self, mock_platform):
        mock_platform.return_value = "Windows"
        config = self.get_test_config()

        with patch.object(PowerShellADManager, "_check_ad_module", return_value=True):
            with patch.object(PowerShellADManager, "_setup_logging"):
                manager = PowerShellADManager(config)
                assert manager.config == config
                assert manager.logger is not None

    @patch("ad_user_manager.powershell_manager.platform.system")
    def test_init_fails_non_windows(self, mock_platform):
        mock_platform.return_value = "Linux"
        config = self.get_test_config()

        with pytest.raises(Exception) as excinfo:
            PowerShellADManager(config)
        assert "PowerShell AD Manager requires Windows" in str(excinfo.value)

    @patch("ad_user_manager.powershell_manager.platform.system")
    def test_init_fails_no_ad_module(self, mock_platform):
        mock_platform.return_value = "Windows"
        config = self.get_test_config()

        with patch.object(PowerShellADManager, "_check_ad_module", return_value=False):
            with pytest.raises(Exception) as excinfo:
                PowerShellADManager(config)
            assert "Active Directory PowerShell module not available" in str(
                excinfo.value
            )

    @patch("ad_user_manager.powershell_manager.platform.system")
    def test_check_ad_module_success(self, mock_platform):
        mock_platform.return_value = "Windows"
        config = self.get_test_config()

        with patch.object(PowerShellADManager, "_setup_logging"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = Mock(returncode=0, stdout="ActiveDirectory")
                manager = PowerShellADManager(config)

                # Test the method directly
                with patch.object(manager, "_run_powershell") as mock_ps:
                    mock_ps.return_value = Mock(returncode=0, stdout="ActiveDirectory")
                    assert manager._check_ad_module() is True

    @patch("ad_user_manager.powershell_manager.platform.system")
    def test_check_ad_module_failure(self, mock_platform):
        mock_platform.return_value = "Windows"
        config = self.get_test_config()

        with patch.object(PowerShellADManager, "_setup_logging"):
            with patch.object(
                PowerShellADManager, "_check_ad_module", return_value=True
            ):
                manager = PowerShellADManager(config)

        # Now test the real method without the mock
        with patch.object(manager, "_run_powershell") as mock_ps:
            mock_ps.return_value = Mock(returncode=1, stderr="Module not found")
            assert manager._check_ad_module() is False

    @patch("ad_user_manager.powershell_manager.platform.system")
    def test_run_powershell_success(self, mock_platform):
        mock_platform.return_value = "Windows"
        config = self.get_test_config()

        with patch.object(PowerShellADManager, "_check_ad_module", return_value=True):
            with patch.object(PowerShellADManager, "_setup_logging"):
                manager = PowerShellADManager(config)

                with patch("subprocess.run") as mock_run:
                    mock_run.return_value = Mock(
                        returncode=0, stdout="Command executed successfully", stderr=""
                    )

                    result = manager._run_powershell("Get-Command")
                    assert result.returncode == 0
                    assert "Command executed successfully" in result.stdout

    @patch("ad_user_manager.powershell_manager.platform.system")
    def test_run_powershell_failure(self, mock_platform):
        mock_platform.return_value = "Windows"
        config = self.get_test_config()

        with patch.object(PowerShellADManager, "_check_ad_module", return_value=True):
            with patch.object(PowerShellADManager, "_setup_logging"):
                manager = PowerShellADManager(config)

                with patch("subprocess.run") as mock_run:
                    mock_run.return_value = Mock(
                        returncode=1, stdout="", stderr="Command not found"
                    )

                    # _run_powershell doesn't raise on non-zero return codes, just logs
                    result = manager._run_powershell("Invalid-Command")
                    assert result.returncode == 1
                    assert result.stderr == "Command not found"

    @patch("ad_user_manager.powershell_manager.platform.system")
    def test_user_exists_true(self, mock_platform):
        mock_platform.return_value = "Windows"
        config = self.get_test_config()

        with patch.object(PowerShellADManager, "_check_ad_module", return_value=True):
            with patch.object(PowerShellADManager, "_setup_logging"):
                manager = PowerShellADManager(config)

                with patch.object(manager, "_run_powershell") as mock_ps:
                    mock_ps.return_value = Mock(
                        returncode=0,
                        stdout='{"SamAccountName": "testuser", "DistinguishedName": "CN=testuser,DC=example,DC=com"}',
                        stderr="",
                    )

                    assert manager.user_exists("testuser") is True

    @patch("ad_user_manager.powershell_manager.platform.system")
    def test_user_exists_false(self, mock_platform):
        mock_platform.return_value = "Windows"
        config = self.get_test_config()

        with patch.object(PowerShellADManager, "_check_ad_module", return_value=True):
            with patch.object(PowerShellADManager, "_setup_logging"):
                manager = PowerShellADManager(config)

                with patch.object(manager, "_run_powershell") as mock_ps:
                    mock_ps.return_value = Mock(
                        returncode=1,
                        stdout="",
                        stderr="Cannot find an object with identity",
                    )

                    assert manager.user_exists("nonexistent") is False

    @patch("ad_user_manager.powershell_manager.platform.system")
    def test_search_user_success(self, mock_platform):
        mock_platform.return_value = "Windows"
        config = self.get_test_config()

        with patch.object(PowerShellADManager, "_check_ad_module", return_value=True):
            with patch.object(PowerShellADManager, "_setup_logging"):
                manager = PowerShellADManager(config)

                json_output = '{"SamAccountName": "testuser", "DistinguishedName": "CN=testuser,OU=Users,DC=example,DC=com"}'

                with patch.object(manager, "_run_powershell") as mock_ps:
                    mock_ps.return_value = Mock(returncode=0, stdout=json_output)

                    user_info = manager.search_user("testuser")
                    assert isinstance(user_info, UserInfo)
                    assert user_info.username == "testuser"
                    assert user_info.exists is True

    @patch("ad_user_manager.powershell_manager.platform.system")
    def test_create_user_success(self, mock_platform):
        mock_platform.return_value = "Windows"
        config = self.get_test_config()

        with patch.object(PowerShellADManager, "_check_ad_module", return_value=True):
            with patch.object(PowerShellADManager, "_setup_logging"):
                manager = PowerShellADManager(config)

                # Mock the PowerShell command calls
                def mock_ps_side_effect(command):
                    if "New-ADUser" in command:
                        return Mock(returncode=0, stdout="User created successfully")
                    if "Get-ADUser" in command:
                        # Mock the search_user call made after creation
                        return Mock(
                            returncode=0,
                            stdout='{"SamAccountName": "testuser", "DistinguishedName": "CN=John Doe,DC=example,DC=com"}',
                        )
                    if "(Get-ADDomain).DNSRoot" in command:
                        return Mock(returncode=0, stdout="example.com")
                    return Mock(returncode=0, stdout="")

                with patch.object(
                    manager, "_run_powershell", side_effect=mock_ps_side_effect
                ):
                    with patch.object(manager, "user_exists", return_value=False):
                        result = manager.create_user(
                            "testuser", "John", "Doe", "john@example.com"
                        )

                        assert isinstance(result, UserCreationResult)
                        assert result.username == "testuser"
                        assert result.created is True

    @patch("ad_user_manager.powershell_manager.platform.system")
    def test_create_user_already_exists(self, mock_platform):
        mock_platform.return_value = "Windows"
        config = self.get_test_config()

        with patch.object(PowerShellADManager, "_check_ad_module", return_value=True):
            with patch.object(PowerShellADManager, "_setup_logging"):
                manager = PowerShellADManager(config)

                with patch.object(manager, "user_exists", return_value=True):
                    with pytest.raises(UserExistsError) as excinfo:
                        manager.create_user(
                            "testuser",
                            "John",
                            "Doe",
                            "john@example.com",
                            resolve_conflicts=False,
                        )
                    assert "already exists" in str(excinfo.value)

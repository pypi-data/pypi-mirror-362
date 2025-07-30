"""
Tests for AD User Manager utility functions.
"""

from unittest.mock import MagicMock, Mock, mock_open, patch

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
    from ad_user_manager.utils import get_version


class TestGetVersion:
    def test_get_version_success(self):
        mock_toml_content = b"""
[project]
name = "ad-user-manager"
version = "1.2.3"
"""
        with patch("builtins.open", mock_open(read_data=mock_toml_content)):
            with patch("tomllib.load") as mock_load:
                mock_load.return_value = {"project": {"version": "1.2.3"}}
                version = get_version()
                assert version == "1.2.3"

    def test_get_version_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            version = get_version()
            assert version == "0.1.0"

    def test_get_version_key_error_missing_project(self):
        with patch("builtins.open", mock_open(read_data=b"{}")):
            with patch("tomllib.load") as mock_load:
                mock_load.return_value = {}
                version = get_version()
                assert version == "0.1.0"

    def test_get_version_key_error_missing_version(self):
        with patch("builtins.open", mock_open(read_data=b'[project]\nname = "test"')):
            with patch("tomllib.load") as mock_load:
                mock_load.return_value = {"project": {"name": "test"}}
                version = get_version()
                assert version == "0.1.0"

    def test_get_version_path_construction(self):
        with patch("builtins.open", mock_open(read_data=b"")):
            with patch("tomllib.load") as mock_load:
                mock_load.return_value = {"project": {"version": "2.0.0"}}
                with patch(
                    "ad_user_manager.utils.__file__",
                    "/fake/path/ad_user_manager/utils.py",
                ):
                    version = get_version()
                    assert version == "2.0.0"

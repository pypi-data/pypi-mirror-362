"""
Tests for AD User Manager package imports and initialization.
"""

from unittest.mock import MagicMock, Mock, patch

# Create comprehensive mocks for ldap3 and its submodules
ldap3_mock = MagicMock()
ldap3_mock.ALL = "ALL"
ldap3_mock.SIMPLE = "SIMPLE"
ldap3_mock.Connection = Mock
ldap3_mock.Server = Mock
ldap3_mock.core = MagicMock()
ldap3_mock.core.exceptions = MagicMock()
ldap3_mock.core.exceptions.LDAPException = Exception

mock_modules = {
    "ldap3": ldap3_mock,
    "ldap3.core": ldap3_mock.core,
    "ldap3.core.exceptions": ldap3_mock.core.exceptions,
}


class TestPackageImports:
    def test_main_package_import(self):
        # Test that the main package can be imported
        with patch.dict("sys.modules", mock_modules):
            import ad_user_manager

            assert ad_user_manager is not None

    def test_version_import(self):
        # Test that version can be imported
        with patch.dict("sys.modules", mock_modules):
            from ad_user_manager import __version__

            assert __version__ is not None
            assert isinstance(__version__, str)
            assert len(__version__) > 0

    def test_basic_imports(self):
        # Test that basic classes can be imported
        with patch.dict("sys.modules", mock_modules):
            from ad_user_manager import (ADConfig, DCServerConfig,
                                         LDAPServerConfig, UserCreationResult,
                                         UserInfo, create_ad_manager)

            assert ADConfig is not None
            assert DCServerConfig is not None
            assert LDAPServerConfig is not None
            assert UserCreationResult is not None
            assert UserInfo is not None
            assert create_ad_manager is not None

    def test_exceptions_import(self):
        # Test that exceptions can be imported
        with patch.dict("sys.modules", mock_modules):
            from ad_user_manager import (ADUserManagerError, UserExistsError,
                                         ValidationError)

            assert ADUserManagerError is not None
            assert ValidationError is not None
            assert UserExistsError is not None
            # Verify they are exception classes
            assert issubclass(ADUserManagerError, Exception)
            assert issubclass(ValidationError, Exception)
            assert issubclass(UserExistsError, Exception)

    def test_version_format(self):
        # Test that version follows expected format
        with patch.dict("sys.modules", mock_modules):
            from ad_user_manager import __version__

            # Basic format check - should contain digits and dots
            assert any(c.isdigit() for c in __version__)
            assert "." in __version__

    def test_server_config_creation(self):
        # Test that ServerConfig types work
        with patch.dict("sys.modules", mock_modules):
            from ad_user_manager import DCServerConfig, LDAPServerConfig

            # Create instances to test the types
            dc_config = DCServerConfig(base_dn="DC=example,DC=com")
            ldap_config = LDAPServerConfig(
                base_dn="DC=example,DC=com",
                host="ldap.example.com",
                bind_dn="admin@example.com",
                bind_password="password123",
            )

            # Both should be valid
            assert isinstance(dc_config, DCServerConfig)
            assert isinstance(ldap_config, LDAPServerConfig)

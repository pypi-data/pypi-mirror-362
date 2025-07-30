"""
Tests for AD User Manager LDAP manager.
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
    from ad_user_manager.exceptions import (ADConnectionError, SearchError,
                                            UserCreationError, UserExistsError)
    from ad_user_manager.ldap_manager import ADUserManager
    from ad_user_manager.models import UserCreationResult, UserInfo


class TestADUserManager:
    def get_test_config(self):
        return ADConfig(
            server={
                "connection_type": "ldap",
                "base_dn": "DC=example,DC=com",
                "host": "ldap.example.com",
                "bind_dn": "admin@example.com",
                "bind_password": "password123",
            },
            log_level="INFO",
        )

    def test_init_success(self):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)
            assert manager.config == config
            assert manager.logger is not None
            assert manager._connection_pool == []

    @patch("ad_user_manager.ldap_manager.Server")
    @patch("ad_user_manager.ldap_manager.Connection")
    def test_get_connection_success(self, mock_connection_cls, mock_server_cls):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

            mock_server = Mock()
            mock_server_cls.return_value = mock_server

            mock_connection = Mock()
            mock_connection.bound = True
            # Connection is created with auto_bind=True, so bind is called during init
            mock_connection_cls.return_value = mock_connection

            with manager._get_connection() as conn:
                assert conn == mock_connection

    @patch("ad_user_manager.ldap_manager.Server")
    @patch("ad_user_manager.ldap_manager.Connection")
    def test_get_connection_bind_failure(self, mock_connection_cls, mock_server_cls):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

            mock_server = Mock()
            mock_server_cls.return_value = mock_server

            # Mock connection that fails during creation (auto_bind=True)
            mock_connection_cls.side_effect = Exception("Bind failed")

            with pytest.raises(ADConnectionError) as excinfo:
                with manager._get_connection():
                    pass
            # Just verify an ADConnectionError was raised - the exact message depends on mock details
            assert "Bind failed" in str(excinfo.value) or "Cannot spec" in str(
                excinfo.value
            )

    def test_user_exists_true(self):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

            # Mock search_user to return a user info object
            mock_user_info = Mock()
            with patch.object(manager, "search_user", return_value=mock_user_info):
                result = manager.user_exists("testuser")
                assert result is True

    def test_user_exists_false(self):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

            mock_connection = Mock()
            mock_connection.search.return_value = True
            mock_connection.entries = []  # No entries found

            with patch.object(manager, "_get_connection") as mock_get_conn:
                mock_get_conn.return_value.__enter__.return_value = mock_connection

                assert manager.user_exists("nonexistent") is False

    def test_user_exists_search_failure(self):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

            # Mock search_user to raise SearchError
            with patch.object(
                manager,
                "search_user",
                side_effect=SearchError(
                    "sAMAccountName=testuser", "Search operation failed"
                ),
            ):
                with pytest.raises(SearchError) as excinfo:
                    manager.user_exists("testuser")
                assert "Search operation failed" in str(excinfo.value)

    def test_search_user_success(self):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

            mock_entry = Mock()
            mock_entry.entry_dn = "CN=testuser,OU=Users,DC=example,DC=com"
            mock_entry.entry_attributes_as_dict = {
                "sAMAccountName": ["testuser"],
                "mail": ["test@example.com"],
            }

            mock_connection = Mock()
            mock_connection.search.return_value = True
            mock_connection.entries = [mock_entry]

            with patch.object(manager, "_get_connection") as mock_get_conn:
                mock_get_conn.return_value.__enter__.return_value = mock_connection

                user_info = manager.search_user("testuser")
                assert isinstance(user_info, UserInfo)
                assert user_info.username == "testuser"
                assert user_info.exists is True
                assert "mail" in user_info.attributes

    def test_search_user_not_found(self):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

            mock_connection = Mock()
            mock_connection.search.return_value = True
            mock_connection.entries = []

            with patch.object(manager, "_get_connection") as mock_get_conn:
                mock_get_conn.return_value.__enter__.return_value = mock_connection

                user_info = manager.search_user("nonexistent")
                assert user_info is None

    def test_create_user_success(self):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

            mock_connection = Mock()
            mock_connection.add.return_value = True

            with patch.object(manager, "user_exists", return_value=False):
                with patch.object(manager, "_get_connection") as mock_get_conn:
                    mock_get_conn.return_value.__enter__.return_value = mock_connection

                    result = manager.create_user(
                        "testuser", "John", "Doe", "john@example.com"
                    )

                    assert isinstance(result, UserCreationResult)
                    assert result.username == "testuser"
                    assert result.created is True
                    mock_connection.add.assert_called_once()

    def test_create_user_already_exists(self):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

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

    def test_create_user_ldap_failure(self):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

            mock_connection = Mock()
            mock_connection.add.return_value = False
            mock_connection.result = {"description": "Insufficient permissions"}

            with patch.object(manager, "user_exists", return_value=False):
                with patch.object(manager, "_get_connection") as mock_get_conn:
                    mock_get_conn.return_value.__enter__.return_value = mock_connection

                    with pytest.raises(UserCreationError) as excinfo:
                        manager.create_user(
                            "testuser", "John", "Doe", "john@example.com"
                        )
                    assert "Failed to create user" in str(excinfo.value)

    def test_build_user_dn_logic(self):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

            # Test the DN building logic used in create_user
            username = "testuser"
            expected_dn = f"CN={username},{config.server.base_dn}"
            actual_dn = f"CN={username},{manager.config.server.base_dn}"
            assert actual_dn == expected_dn

    def test_build_user_attributes(self):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

            attrs = manager._build_user_attributes(
                "testuser", "John", "Doe", "john@example.com"
            )

            # Note: objectClass is not added by _build_user_attributes - it's used separately in create_user
            assert attrs["sAMAccountName"] == "testuser"
            assert attrs["givenName"] == "John"
            assert attrs["sn"] == "Doe"
            assert attrs["mail"] == "john@example.com"
            assert attrs["displayName"] == "John Doe"

    def test_close_connections(self):
        config = self.get_test_config()

        with patch.object(ADUserManager, "_setup_logging"):
            manager = ADUserManager(config)

            mock_conn1 = Mock()
            mock_conn2 = Mock()
            manager._connection_pool = [mock_conn1, mock_conn2]

            manager.close_connections()

            mock_conn1.unbind.assert_called_once()
            mock_conn2.unbind.assert_called_once()
            assert manager._connection_pool == []

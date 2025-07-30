"""
LDAP-based Active Directory User Manager for remote connections.
"""

import logging
from contextlib import contextmanager
from typing import Any

import ldap3
import structlog
from ldap3 import ALL, SIMPLE, Connection, Server
from ldap3.core.exceptions import LDAPException

from .config import ADConfig
from .exceptions import (ADConnectionError, SearchError, UserCreationError,
                         UserExistsError)
from .models import UserCreationResult, UserInfo


class ADUserManager:
    """Active Directory User Manager (LDAP-based for remote connections)."""

    def __init__(self, config: ADConfig):
        """Initialize AD User Manager with configuration."""
        self.config = config
        self.logger = structlog.get_logger(__name__)
        self._connection_pool: list[Connection] = []
        self._setup_logging()

    def _setup_logging(self):
        """Setup structured logging."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level), format="%(message)s"
        )

        if self.config.log_format == "json":
            structlog.configure(
                processors=[
                    structlog.stdlib.filter_by_level,
                    structlog.stdlib.add_logger_name,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.PositionalArgumentsFormatter(),
                    structlog.processors.TimeStamper(fmt="iso"),
                    structlog.processors.StackInfoRenderer(),
                    structlog.processors.format_exc_info,
                    structlog.processors.JSONRenderer(),
                ],
                wrapper_class=structlog.stdlib.BoundLogger,
                logger_factory=structlog.stdlib.LoggerFactory(),
                cache_logger_on_first_use=True,
            )
        else:
            structlog.configure(
                processors=[
                    structlog.stdlib.filter_by_level,
                    structlog.stdlib.add_logger_name,
                    structlog.stdlib.add_log_level,
                    structlog.stdlib.PositionalArgumentsFormatter(),
                    structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                    structlog.dev.ConsoleRenderer(),
                ],
                wrapper_class=structlog.stdlib.BoundLogger,
                logger_factory=structlog.stdlib.LoggerFactory(),
                cache_logger_on_first_use=True,
            )

    def _create_server(self) -> Server:
        """Create LDAP server object."""
        return Server(
            host=self.config.server.host,
            port=self.config.server.port,
            use_ssl=self.config.server.use_ssl,
            get_info=ALL,
            connect_timeout=self.config.connection_timeout,
        )

    @contextmanager
    def _get_connection(self):
        """Get LDAP connection from pool or create new one."""
        connection = None
        try:
            if self._connection_pool:
                connection = self._connection_pool.pop()
                if not connection.bound:
                    connection.bind()
            else:
                server = self._create_server()
                connection = Connection(
                    server,
                    user=self.config.server.bind_dn,
                    password=self.config.server.bind_password,
                    authentication=SIMPLE,
                    auto_bind=True,
                    raise_exceptions=True,
                )

            yield connection

        except LDAPException as e:
            self.logger.error("LDAP connection error", error=str(e))
            raise ADConnectionError(self.config.server.host, str(e))
        except Exception as e:
            self.logger.error("Unexpected connection error", error=str(e))
            raise ADConnectionError(
                self.config.server.host, f"Unexpected error: {str(e)}"
            )
        finally:
            if connection and connection.bound:
                if len(self._connection_pool) < self.config.pool_size:
                    self._connection_pool.append(connection)
                else:
                    connection.unbind()

    def test_connection(self) -> bool:
        """Test AD connection."""
        try:
            with self._get_connection() as conn:
                self.logger.info(
                    "AD connection test successful", server=self.config.server.host
                )
                return True
        except Exception as e:
            self.logger.error("AD connection test failed", error=str(e))
            return False

    def search_user(self, username: str) -> UserInfo | None:
        """Search for a user in AD."""
        search_filter = f"({self.config.attributes.username_field}={username})"

        try:
            with self._get_connection() as conn:
                success = conn.search(
                    search_base=self.config.server.base_dn,
                    search_filter=search_filter,
                    search_scope=ldap3.SUBTREE,
                    attributes=ldap3.ALL_ATTRIBUTES,
                    time_limit=self.config.search_timeout,
                )

                if not success:
                    raise SearchError(search_filter, "Search operation failed")

                if len(conn.entries) == 0:
                    self.logger.debug("User not found", username=username)
                    return None

                entry = conn.entries[0]
                user_info = UserInfo(
                    username=username,
                    dn=entry.entry_dn,
                    attributes=dict(entry.entry_attributes_as_dict),
                    exists=True,
                )

                self.logger.debug("User found", username=username, dn=entry.entry_dn)
                return user_info

        except LDAPException as e:
            self.logger.error("LDAP search error", username=username, error=str(e))
            raise SearchError(search_filter, str(e))
        except Exception as e:
            self.logger.error(
                "Unexpected search error", username=username, error=str(e)
            )
            raise SearchError(search_filter, f"Unexpected error: {str(e)}")

    def user_exists(self, username: str) -> bool:
        """Check if a user exists in AD."""
        user_info = self.search_user(username)
        return user_info is not None

    def create_user(
        self,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        password: str | None = None,
        additional_attributes: dict[str, Any] | None = None,
        resolve_conflicts: bool = True,
        dry_run: bool = False,
    ) -> UserCreationResult:
        """Create a new user in AD."""
        original_username = username
        conflicts_resolved = 0

        # Check if user already exists and handle conflicts
        if resolve_conflicts and self.user_exists(username):
            from .validators import UserValidator

            validator = UserValidator(self.config)
            username, conflicts_resolved = validator.resolve_username_conflict(
                username, self
            )
        elif self.user_exists(username):
            raise UserExistsError(username)

        # Build user DN
        user_dn = f"CN={username},{self.config.server.base_dn}"

        # Build user attributes
        user_attributes = self._build_user_attributes(
            username, first_name, last_name, email, additional_attributes
        )

        if dry_run:
            self.logger.info(
                "Dry run - would create user", username=username, dn=user_dn
            )
            return UserCreationResult(
                username=username,
                created=False,
                original_username=original_username,
                dn=user_dn,
                conflicts_resolved=conflicts_resolved,
                message="Dry run - user would be created",
            )

        try:
            with self._get_connection() as conn:
                success = conn.add(
                    user_dn, self.config.attributes.object_class, user_attributes
                )

                if not success:
                    error_msg = f"Failed to create user: {conn.result}"
                    self.logger.error(
                        "User creation failed", username=username, error=error_msg
                    )
                    raise UserCreationError(username, error_msg)

                # Set password if provided
                if password:
                    self._set_user_password(conn, user_dn, password)

                self.logger.info(
                    "User created successfully", username=username, dn=user_dn
                )
                return UserCreationResult(
                    username=username,
                    created=True,
                    original_username=original_username,
                    dn=user_dn,
                    conflicts_resolved=conflicts_resolved,
                    message="User created successfully",
                )

        except LDAPException as e:
            self.logger.error(
                "LDAP user creation error", username=username, error=str(e)
            )
            raise UserCreationError(username, str(e))
        except Exception as e:
            self.logger.error(
                "Unexpected user creation error", username=username, error=str(e)
            )
            raise UserCreationError(username, f"Unexpected error: {str(e)}")

    def _build_user_attributes(
        self,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        additional_attributes: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build user attributes dictionary for AD."""
        display_name = f"{first_name} {last_name}"
        upn = f"{username}@{self.config.server.host}"

        attributes = {
            self.config.attributes.username_field: username,
            self.config.attributes.first_name_field: first_name,
            self.config.attributes.last_name_field: last_name,
            self.config.attributes.display_name_field: display_name,
            self.config.attributes.email_field: email,
            self.config.attributes.user_principal_name_field: upn,
        }

        if additional_attributes:
            attributes.update(additional_attributes)

        return attributes

    def _set_user_password(self, connection: Connection, user_dn: str, password: str):
        """Set user password."""
        try:
            success = connection.extend.microsoft.modify_password(user_dn, password)
            if not success:
                self.logger.warning("Failed to set user password", user_dn=user_dn)
        except Exception as e:
            self.logger.warning(
                "Error setting user password", user_dn=user_dn, error=str(e)
            )

    def close_connections(self):
        """Close all pooled connections."""
        for connection in self._connection_pool:
            if connection.bound:
                connection.unbind()
        self._connection_pool.clear()
        self.logger.debug("All connections closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_connections()

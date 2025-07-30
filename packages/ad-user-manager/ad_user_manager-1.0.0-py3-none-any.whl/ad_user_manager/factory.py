"""
Factory function for creating AD managers based on configuration.
"""

import structlog

from .config import ADConfig
from .models import DCServerConfig, LDAPServerConfig


def create_ad_manager(config: ADConfig):
    """
    Factory function to create the appropriate AD manager based on configuration.

    Args:
        config: ADConfig instance with server configuration

    Returns:
        Either PowerShellADManager or ADUserManager instance

    Raises:
        Exception: If no suitable manager can be created
    """
    logger = structlog.get_logger(__name__)

    # Import managers here to avoid circular imports
    from .ldap_manager import ADUserManager
    from .powershell_manager import PowerShellADManager

    # Determine manager type based on server config
    if isinstance(config.server, DCServerConfig):
        # Domain Controller configuration - use PowerShell manager
        try:
            logger.info("Creating PowerShell AD manager for domain controller")
            return PowerShellADManager(config)
        except Exception as e:
            logger.error("Failed to create PowerShell AD manager", error=str(e))
            raise Exception(f"Failed to create PowerShell AD manager: {e}")

    elif isinstance(config.server, LDAPServerConfig):
        # LDAP configuration - use LDAP manager
        try:
            logger.info("Creating LDAP AD manager for remote connection")
            return ADUserManager(config)
        except Exception as e:
            logger.error("Failed to create LDAP AD manager", error=str(e))
            raise Exception(f"Failed to create LDAP AD manager: {e}")

    else:
        # Fallback for legacy configurations or auto-detection
        logger.warning("Unknown server configuration type, attempting auto-detection")

        # Try PowerShell first (optimal for domain controllers)
        try:
            logger.info("Attempting to create PowerShell AD manager")
            return PowerShellADManager(config)
        except Exception as ps_error:
            logger.warning(
                "PowerShell AD manager not available, falling back to LDAP",
                error=str(ps_error),
            )

            # Fall back to LDAP manager
            try:
                logger.info("Creating LDAP AD manager as fallback")
                return ADUserManager(config)
            except Exception as ldap_error:
                logger.error(
                    "Both PowerShell and LDAP managers failed",
                    powershell_error=str(ps_error),
                    ldap_error=str(ldap_error),
                )
                raise Exception(
                    f"Failed to create any AD manager. "
                    f"PowerShell: {ps_error}, LDAP: {ldap_error}"
                )

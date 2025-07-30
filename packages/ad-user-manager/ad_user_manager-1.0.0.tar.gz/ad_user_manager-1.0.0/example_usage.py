"""
AD User Manager - Example Usage

This file demonstrates how to use the AD User Manager library with various configurations
and operations including user search, creation, and smart OU detection.
"""

from cw_rpa import Logger

from ad_user_manager import (ADConfig, DCServerConfig, LDAPServerConfig,
                             create_ad_manager, get_version_info)
from ad_user_manager.exceptions import (ADUserManagerError, UserExistsError,
                                        UserNotFoundError)

logger = Logger()

# SECTION - Domain Controller Mode (Recommended)
logger.info("=== Domain Controller Mode Examples ===")

version_info = get_version_info()
logger.info(f"[START] AD User Manager v{version_info['version']} - Example Usage")
logger.info(
    f"[INFO] Python {version_info['python_version']} on {version_info['system']} {version_info['architecture']}"
)


# Example 1: Minimal configuration with auto-detection
def example_dc_minimal():
    """Example using minimal DC configuration with auto-detection."""
    logger.info("\n--- Minimal DC Configuration (Auto-detect everything) ---")

    try:
        config = ADConfig(
            server=DCServerConfig(
                # No base_dn specified - will be auto-detected
                # No default_user_ou specified - will use smart detection
                # All auto-detection flags are True by default
            ),
            log_level="INFO",
        )
        logger.info(f"Configuration created: {config}")
    except Exception as e:
        config = ADConfig(
            server=DCServerConfig(
                # Fallback to minimal config if auto-detection fails
                base_dn="DC=lawsoncompanies,DC=com",
                fallback_to_users_container=True,
                validate_ou_has_users=True,
            ),
            log_level="INFO",
        )
        logger.error(
            f"[ERROR] Failed to create config, using fallback: {e} -> {config}"
        )

    try:
        with create_ad_manager(config) as manager:
            # Test connection
            if manager.test_connection():
                logger.info("[OK] Connected successfully to domain controller")

                # Auto-detect base DN
                base_dn = manager.get_base_dn()
                logger.info(f"[INFO] Auto-detected base DN: {base_dn}")

                # Auto-detect optimal user OU
                optimal_ou = manager.get_optimal_user_ou()
                logger.info(f"[TARGET] Optimal user OU: {optimal_ou}")

            else:
                logger.info("[ERROR] Failed to connect to domain controller")

    except ADUserManagerError as e:
        logger.exception(f"[ERROR] AD Error: {e}", stack_info=True)
    except Exception as e:
        logger.exception(f"[ERROR] Unexpected error: {e}", stack_info=True)


# Example 2: DC configuration with specific user OU
def example_dc_custom_ou():
    """Example using DC configuration with custom user OU."""
    logger.info("\n--- DC Configuration with Custom User OU ---")

    config = ADConfig(
        server=DCServerConfig(
            default_user_ou="OU=Users,DC=lawsoncompanies,DC=com",
            validate_ou_has_users=True,  # Validate OU contains users
            fallback_to_users_container=True,  # Fallback if OU invalid
        ),
        log_level="INFO",
    )

    try:
        with create_ad_manager(config) as manager:
            if manager.test_connection():
                logger.info("[OK] Connected to domain controller")

                # Show available user OUs
                user_ous = manager.find_user_ous(validate_has_users=True)
                # if the user ous is multiple items, log one per line else log all as one
                if isinstance(user_ous, list) and len(user_ous) > 1:
                    for ou in user_ous:
                        logger.info(f"[OU] Available User OU: {ou}")
                else:
                    logger.info(f"[LIST] Available user OUs: {user_ous}")

    except ADUserManagerError as e:
        logger.exception(f"[ERROR] AD Error: {e}", stack_info=True)


# SECTION - Get the base_dn for the domain
def example_get_base_dn():
    """Example showing how to get base DN automatically."""
    logger.info("\n--- Auto-detect Base DN ---")

    config = ADConfig(server=DCServerConfig(), log_level="INFO")

    try:
        with create_ad_manager(config) as manager:
            if manager.test_connection():
                # Get base DN
                base_dn = manager.get_base_dn()
                logger.info(f"[DOMAIN] Domain Base DN: {base_dn}")

                # Get default users container
                users_container = manager.get_default_users_container()
                logger.info(f"[USERS] Default Users Container: {users_container}")

                # Find all user OUs
                user_ous = manager.find_user_ous(validate_has_users=False)
                logger.info(f"[FOLDER] All User OUs: {user_ous}")

                # Find validated user OUs (contain actual users)
                validated_ous = manager.find_user_ous(validate_has_users=True)
                logger.info(f"[OK] Validated User OUs: {validated_ous}")

    except ADUserManagerError as e:
        logger.exception(f"[ERROR] AD Error: {e}", stack_info=True)


# SECTION - Search a user by username
def example_search_user():
    """Example showing how to search for users."""
    logger.info("\n--- Search Users ---")

    config = ADConfig(server=DCServerConfig(), log_level="INFO")

    try:
        with create_ad_manager(config) as manager:
            if manager.test_connection():
                logger.info("[OK] Connected to domain controller")

                # Search for a specific user
                test_username = "testuser"  # Change this to an existing username

                logger.info(f"[SEARCH] Searching for user: {test_username}")

                try:
                    user_info = manager.search_user(test_username)
                    logger.info("[USER] User found!")
                    try:
                        logger.info(f"   Username: {user_info.username}")
                        logger.info(f"   DN: {user_info.dn}")
                        logger.info(
                            f"   Display Name: {user_info.attributes.get('displayName', 'N/A')}"
                        )
                        logger.info(
                            f"   Email: {user_info.attributes.get('mail', 'N/A')}"
                        )
                        logger.info(
                            f"   UPN: {user_info.attributes.get('userPrincipalName', 'N/A')}"
                        )
                    except Exception as e:
                        logger.error(
                            f"[ERROR] Failed to access user attributes: {e} -> {user_info}"
                        )
                    logger.result_success_message(user_info)
                except UserNotFoundError:
                    logger.info(f"[NOT FOUND] User '{test_username}' not found")

                # Check if user exists (simpler boolean check)
                exists = manager.user_exists(test_username)
                logger.info(f"[CHECK] User exists check: {exists}")

    except ADUserManagerError as e:
        logger.exception(f"[ERROR] AD Error: {e}", stack_info=True)


# SECTION - Create a user
def example_create_user():
    """Example showing how to create users with smart OU detection."""
    logger.info("\n--- Create User ---")

    config = ADConfig(
        server=DCServerConfig(
            # Let the system auto-detect the best OU
            fallback_to_users_container=True,
            validate_ou_has_users=True,
        ),
        log_level="INFO",
    )

    try:
        with create_ad_manager(config) as manager:
            if manager.test_connection():
                logger.info("[OK] Connected to domain controller")

                # Dry run first to see what would happen
                logger.info("\n[TEST] Dry run - testing user creation...")
                dry_result = manager.create_user(
                    username="test.automation",
                    first_name="Test",
                    last_name="Automation",
                    email="test.automation@company.com",
                    password="$om3rAnd0m53<re+kEywEreno7u$!ng",
                    dry_run=True,
                )

                try:
                    logger.info(f"   Would create: {dry_result.username}")
                    logger.info(f"   Target DN: {dry_result.dn}")
                    logger.info(f"   Message: {dry_result.message}")
                except Exception as e:
                    logger.error(
                        f"[ERROR] Failed to access dry run result: {e} -> {dry_result}"
                    )

                logger.result_success_message(dry_result)

                # Uncomment below to actually create the user
                # logger.info("\n[CREATE] Creating user for real...")
                # result = manager.create_user(
                #     username="test.automation",
                #     first_name="Test",
                #     last_name="Automation",
                #     email="test.automation@company.com",
                #     password="$om3rAnd0m53<re+kEywEreno7u$!ng",
                #     resolve_conflicts=True  # Auto-resolve username conflicts
                # )
                #
                # if result.created:
                #     logger.info(f"[OK] User created successfully!")
                #     logger.info(f"   Username: {result.username}")
                #     logger.info(f"   DN: {result.dn}")
                #     if result.conflicts_resolved > 0:
                #         logger.info(f"   Conflicts resolved: {result.conflicts_resolved}")
                # else:
                #     logger.info(f"[ERROR] User creation failed: {result.message}")

    except UserExistsError as e:
        logger.info(f"[WARNING] User already exists: {e}")
    except ADUserManagerError as e:
        logger.exception(f"[ERROR] AD Error: {e}", stack_info=True)


# SECTION - LDAP Mode (Remote connections)
def example_ldap_mode():
    """Example using LDAP mode for remote AD connections."""
    logger.info("\n--- LDAP Mode (Remote Connection) ---")

    config = ADConfig(
        server=LDAPServerConfig(
            host="dc01.company.com",  # Replace with your domain controller
            port=389,  # Use 636 for LDAPS
            use_ssl=False,  # Set to True for LDAPS
            base_dn="DC=company,DC=com",  # Must be specified for LDAP mode
            bind_dn="CN=service-account,OU=Service Accounts,DC=company,DC=com",
            bind_password="ServiceAccountPassword",
        ),
        log_level="INFO",
    )

    try:
        with create_ad_manager(config) as manager:
            if manager.test_connection():
                logger.info("[OK] Connected via LDAP")

                # Search for a user
                try:
                    user_info = manager.search_user("testuser")
                    logger.info(f"[USER] Found user via LDAP: {user_info.username}")
                except UserNotFoundError:
                    logger.info("[NOT FOUND] User not found")

    except ADUserManagerError as e:
        logger.exception(f"[ERROR] LDAP Error: {e}", stack_info=True)


# SECTION - Configuration Examples
def example_configuration_options():
    """Example showing different configuration options."""
    logger.info("\n--- Configuration Options ---")

    # Full DC configuration
    dc_config = ADConfig(
        server=DCServerConfig(
            host="",  # Auto-detect
            base_dn="",  # Auto-detect
            default_user_ou="OU=Users,DC=lawsoncompanies,DC=com",
            fallback_to_users_container=True,
            validate_ou_has_users=True,
            auto_detect_base_dn=True,
            use_current_credentials=True,
        ),
        log_level="DEBUG",
        log_format="json",  # or "console"
        connection_timeout=30,
        search_timeout=15,
        pool_size=5,
    )

    logger.info("[CONFIG] DC Configuration created")
    try:
        logger.info(f"   Host: {dc_config.server.host or 'Auto-detect'}")
        logger.info(f"   Base DN: {dc_config.server.base_dn or 'Auto-detect'}")
        logger.info(
            f"   Default User OU: {dc_config.server.default_user_ou or 'Auto-detect'}"
        )
        logger.info(f"   Validate OU: {dc_config.server.validate_ou_has_users}")
        logger.info(f"   Auto-detect Base DN: {dc_config.server.auto_detect_base_dn}")
    except Exception as e:
        logger.error(f"[ERROR] Failed to access configuration: {e} -> {dc_config}")


# SECTION - Error Handling Examples
def example_error_handling():
    """Example showing proper error handling."""
    logger.info("\n--- Error Handling Examples ---")

    config = ADConfig(server=DCServerConfig(), log_level="INFO")

    try:
        with create_ad_manager(config) as manager:
            # Test connection with error handling
            if not manager.test_connection():
                logger.info(
                    "[ERROR] Connection failed - check AD connectivity and permissions"
                )
                return

            # Search with error handling
            try:
                user_info = manager.search_user("nonexistent-user")
                logger.info(f"[USER] Found: {user_info.username}")
            except UserNotFoundError:
                logger.info("[USER] User not found (this is normal)")
            except Exception as e:
                logger.exception(f"[SEARCH] Search error: {e}", stack_info=True)

            # Create user with error handling
            try:
                result = manager.create_user(
                    username="test.user",
                    first_name="Test",
                    last_name="User",
                    email="test.user@company.com",
                    dry_run=True,  # Safe dry run
                )
                try:
                    logger.info(f"[TEST] Dry run successful: {result.message}")
                except Exception as e:
                    logger.error(
                        f"[ERROR] Failed to access dry run result: {e} -> {result}"
                    )
            except UserExistsError:
                logger.info("[WARNING] User already exists")
            except Exception as e:
                logger.exception(f"[ERROR] Creation error: {e}", stack_info=True)

    except ADUserManagerError as e:
        logger.exception(f"[ERROR] AD Manager Error: {e}", stack_info=True)
    except Exception as e:
        logger.exception(f"[ERROR] Unexpected Error: {e}", stack_info=True)


# SECTION - Main execution
if __name__ == "__main__":
    logger.info("[START] AD User Manager - Example Usage\n")

    # Run examples (comment out any you don't want to run)
    try:
        example_dc_minimal()
        example_dc_custom_ou()
        example_get_base_dn()
        example_search_user()
        example_create_user()
        # example_ldap_mode()  # Uncomment if you have LDAP credentials
        example_configuration_options()
        example_error_handling()

        logger.info("\n[OK] All examples completed!")

    except KeyboardInterrupt:
        logger.info("\n[STOP] Examples interrupted by user")
    except Exception as e:
        logger.exception(
            f"\n[ERROR] Unexpected error in examples: {e}", stack_info=True
        )

    logger.info(
        "\n[NOTE] Note: Remember to uncomment actual user creation code when ready to create real users!"
    )

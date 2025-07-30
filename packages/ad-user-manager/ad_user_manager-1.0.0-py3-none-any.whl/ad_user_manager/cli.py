"""
Command Line Interface for AD User Manager.
"""

import os
import sys
from typing import Any

import click
from rich.console import Console
from rich.table import Table

from .config import ADConfig
from .exceptions import ADUserManagerError
from .factory import create_ad_manager
from .models import UserCreationResult
from .utils import get_version, get_version_info
from .validators import UserValidator

console = Console()


def print_success(message: str, test_console: Console | None = None):
    """Print success message with rich formatting."""
    target_console = test_console or console
    target_console.print(f"✅ {message}", style="green")


def print_error(message: str, test_console: Console | None = None):
    """Print error message with rich formatting."""
    target_console = test_console or console
    target_console.print(f"❌ {message}", style="red")


def print_warning(message: str, test_console: Console | None = None):
    """Print warning message with rich formatting."""
    target_console = test_console or console
    target_console.print(f"⚠️ {message}", style="yellow")


def print_info(message: str, test_console: Console | None = None):
    """Print info message with rich formatting."""
    target_console = test_console or console
    target_console.print(f"ℹ️ {message}", style="blue")


def print_result_table(result: UserCreationResult, test_console: Console | None = None):
    """Print user creation result in a formatted table."""
    table = Table(title="User Creation Result")
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Username", result.username)
    table.add_row("Original Username", result.original_username)
    table.add_row("Created", "✅ Yes" if result.created else "❌ No")
    table.add_row("DN", result.dn)
    table.add_row("Conflicts Resolved", str(result.conflicts_resolved))
    table.add_row("Message", result.message)

    target_console = test_console or console
    target_console.print(table)


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.version_option(get_version())
@click.pass_context
def cli(ctx, verbose):
    """AD User Manager - Modern Active Directory user management tool."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    if verbose:
        print_info("Verbose mode enabled")


@cli.command()
@click.option("--username", "-u", required=True, help="Username to create")
@click.option("--first-name", "-f", required=True, help="First name")
@click.option("--last-name", "-l", required=True, help="Last name")
@click.option("--email", "-e", required=True, help="Email address")
@click.option("--password", "-p", help="Initial password (optional)")
@click.option(
    "--resolve-conflicts",
    is_flag=True,
    default=True,
    help="Automatically resolve username conflicts",
)
@click.option(
    "--dry-run", is_flag=True, help="Show what would be done without making changes"
)
@click.option("--config-file", help="Path to configuration file")
@click.pass_context
def create_user(
    ctx,
    username,
    first_name,
    last_name,
    email,
    password,
    resolve_conflicts,
    dry_run,
    config_file,
):
    """Create a new user in Active Directory."""

    try:
        # Load configuration
        if config_file:
            os.environ["AD_CONFIG_FILE"] = config_file

        config = ADConfig()

        if ctx.obj["verbose"]:
            print_info(f"Connecting to AD server: {config.server.host}")

        # Create user manager (auto-detects PowerShell vs LDAP)
        with create_ad_manager(config) as manager:
            # Test connection
            if not manager.test_connection():
                print_error("Failed to connect to Active Directory server")
                sys.exit(1)

            # Validate user data
            validator = UserValidator(config)
            validator.validate_user_data(username, first_name, last_name, email)

            if dry_run:
                print_info("DRY RUN MODE - No changes will be made")

            # Create user
            result = manager.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                resolve_conflicts=resolve_conflicts,
                dry_run=dry_run,
            )

            # Print result
            print_result_table(result)

            if result.created:
                print_success(f"User '{result.username}' created successfully!")
            elif dry_run:
                print_info("Dry run completed - user would be created")
            else:
                print_warning("User was not created")

    except ADUserManagerError as e:
        print_error(f"AD User Manager Error: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if ctx.obj["verbose"]:
            console.print_exception()
        sys.exit(1)


@cli.command()
@click.option("--username", "-u", required=True, help="Username to search for")
@click.option("--config-file", help="Path to configuration file")
@click.pass_context
def search_user(ctx, username, config_file):
    """Search for a user in Active Directory."""

    try:
        # Load configuration
        if config_file:
            os.environ["AD_CONFIG_FILE"] = config_file

        config = ADConfig()

        if ctx.obj["verbose"]:
            print_info(f"Connecting to AD server: {config.server.host}")

        # Create user manager (auto-detects PowerShell vs LDAP)
        with create_ad_manager(config) as manager:
            # Test connection
            if not manager.test_connection():
                print_error("Failed to connect to Active Directory server")
                sys.exit(1)

            # Search for user
            user_info = manager.search_user(username)

            if user_info:
                print_success(f"User '{username}' found!")

                table = Table(title=f"User Information: {username}")
                table.add_column("Attribute", style="cyan", no_wrap=True)
                table.add_column("Value", style="magenta")

                table.add_row("Distinguished Name", user_info.dn)
                table.add_row("Username", user_info.username)

                # Add key attributes
                for attr_name, attr_value in user_info.attributes.items():
                    if attr_name in [
                        "displayName",
                        "mail",
                        "givenName",
                        "sn",
                        "userPrincipalName",
                    ]:
                        value = (
                            str(attr_value[0])
                            if isinstance(attr_value, list) and attr_value
                            else str(attr_value)
                        )
                        table.add_row(attr_name, value)

                console.print(table)
            else:
                print_warning(f"User '{username}' not found")

    except ADUserManagerError as e:
        print_error(f"AD User Manager Error: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if ctx.obj["verbose"]:
            console.print_exception()
        sys.exit(1)


@cli.command()
@click.option("--config-file", help="Path to configuration file")
@click.pass_context
def test_connection(ctx, config_file):
    """Test connection to Active Directory server."""

    try:
        # Load configuration
        if config_file:
            os.environ["AD_CONFIG_FILE"] = config_file

        config = ADConfig()

        print_info(
            f"Testing connection to AD server: {config.server.host}:{config.server.port}"
        )

        # Create user manager and test connection
        with create_ad_manager(config) as manager:
            if manager.test_connection():
                print_success("Connection to Active Directory server successful!")
            else:
                print_error("Failed to connect to Active Directory server")
                sys.exit(1)

    except ADUserManagerError as e:
        print_error(f"AD User Manager Error: {e}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        if ctx.obj["verbose"]:
            console.print_exception()
        sys.exit(1)


@cli.command()
@click.option("--first-name", "-f", required=True, help="First name")
@click.option("--last-name", "-l", required=True, help="Last name")
@click.option("--count", "-c", default=5, help="Number of suggestions to generate")
@click.pass_context
def suggest_usernames(ctx, first_name, last_name, count):
    """Generate username suggestions based on first and last name."""

    try:
        config = ADConfig()
        validator = UserValidator(config)

        suggestions = validator.generate_username_suggestions(
            first_name, last_name, count
        )

        if suggestions:
            print_info(f"Username suggestions for {first_name} {last_name}:")

            table = Table(title="Username Suggestions")
            table.add_column("#", style="cyan", no_wrap=True)
            table.add_column("Username", style="magenta")

            for i, suggestion in enumerate(suggestions, 1):
                table.add_row(str(i), suggestion)

            console.print(table)
        else:
            print_warning("No username suggestions could be generated")

    except Exception as e:
        print_error(f"Error generating suggestions: {e}")
        if ctx.obj["verbose"]:
            console.print_exception()
        sys.exit(1)


@cli.command()
@click.pass_context
def version(ctx):
    """Show detailed version information."""

    try:
        version_info = get_version_info()

        print_info(f"AD User Manager v{version_info['version']}")

        table = Table(title="Version Information", highlight=True)
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        table.add_row("Package Version", version_info["version"])
        table.add_row("Python Version", version_info["python_version"])
        table.add_row("Platform", version_info["platform"])
        table.add_row("System", version_info["system"])
        table.add_row("Architecture", version_info["architecture"])
        table.add_row("Installation Path", version_info["installation_path"])
        table.add_row(
            "PyPI URL (Documentation)",
            "https://pypi.org/project/ad-user-manager/",
            end_section=True,
        )

        console.print(table)

    except Exception as e:
        print_error(f"Error getting version information: {e}")
        if ctx.obj.get("verbose"):
            console.print_exception()
        sys.exit(1)


def run_automation(
    username: str,
    first_name: str,
    last_name: str,
    email: str,
    password: str | None = None,
    resolve_conflicts: bool = True,
    dry_run: bool = False,
    config_file: str | None = None,
    verbose: bool = False,
    additional_attributes: dict[str, Any] | None = None,
) -> UserCreationResult:
    """
    Automation function that runs user creation with all parameters.

    This function is designed to be called from automation tools when
    RUN_LOCALLY environment variable is not set or is false.

    Args:
        username: Username to create
        first_name: First name
        last_name: Last name
        email: Email address
        password: Initial password (optional)
        resolve_conflicts: Automatically resolve username conflicts
        dry_run: Show what would be done without making changes
        config_file: Path to configuration file
        verbose: Enable verbose output
        additional_attributes: Additional AD attributes to set

    Returns:
        UserCreationResult: Result of the user creation operation

    Raises:
        ADUserManagerError: If AD operation fails
        Exception: If unexpected error occurs
    """

    # Set up configuration
    if config_file:
        os.environ["AD_CONFIG_FILE"] = config_file

    config = ADConfig()

    # Create user manager (auto-detects PowerShell vs LDAP)
    with create_ad_manager(config) as manager:
        # Test connection
        if not manager.test_connection():
            raise ADUserManagerError("Failed to connect to Active Directory server")

        # Validate user data
        validator = UserValidator(config)
        validator.validate_user_data(username, first_name, last_name, email)

        # Create user
        result = manager.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            additional_attributes=additional_attributes,
            resolve_conflicts=resolve_conflicts,
            dry_run=dry_run,
        )

        return result


def main():
    """Main entry point for CLI."""
    # Check if running locally or in automation mode
    run_locally = os.getenv("RUN_LOCALLY", "true").lower() == "true"

    if run_locally:
        # Run normal CLI
        cli()
    else:
        # Automation mode - you can finish this logic
        # This is where you would handle automation parameters
        # For now, just run the CLI
        print_info("Running in automation mode")
        cli()


if __name__ == "__main__":
    main()

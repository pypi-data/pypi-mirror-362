"""
Utility functions for AD User Manager.
"""

import platform
import sys
import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

DEFAULT_VERSION = "0.1.0"


def get_version() -> str:
    try:
        return version("ad_user_manager")
    except PackageNotFoundError:
        try:
            # If package is not installed, read version from pyproject.toml
            print("Package not found, reading version from pyproject.toml...")
            return get_dev_version()
        except FileNotFoundError:
            # Fallback version if pyproject.toml is not found
            return DEFAULT_VERSION
        except KeyError:
            # Fallback version if version key is not found in pyproject.toml
            return DEFAULT_VERSION


def get_dev_version() -> str:
    """
    Read version from pyproject.toml.

    Returns:
        Version string from pyproject.toml

    Raises:
        FileNotFoundError: If pyproject.toml is not found
        KeyError: If version is not found in pyproject.toml
    """
    try:
        # Get path to pyproject.toml (one level up from package directory)
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        return data["project"]["version"]

    except FileNotFoundError:
        # Fallback version if pyproject.toml is not found
        return DEFAULT_VERSION
    except KeyError:
        # Fallback version if version key is not found
        return DEFAULT_VERSION


def get_version_info() -> dict[str, str]:
    """
    Get detailed version information including platform details.

    Returns:
        Dictionary containing version, Python version, platform, and installation path
    """
    package_version = get_version()
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )

    return {
        "version": package_version,
        "python_version": python_version,
        "platform": platform.platform(),
        "system": platform.system(),
        "architecture": platform.machine(),
        "installation_path": str(Path(__file__).parent.parent),
    }

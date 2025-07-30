from .cli import run_automation
from .config import ADConfig, ServerConfig
from .exceptions import (ADConnectionError, ADPermissionError,
                         ADUserManagerError, AuthenticationError,
                         ConfigurationError, LDAPOperationError,
                         PowerShellExecutionError, RetryableError, SearchError,
                         UserCreationError, UserExistsError, UserNotFoundError,
                         ValidationError)
from .factory import create_ad_manager
from .ldap_manager import ADUserManager
from .models import (ConflictResolutionConfig, DCServerConfig,
                     LDAPServerConfig, UserAttributeMapping,
                     UserCreationResult, UserInfo)
from .powershell_manager import PowerShellADManager
from .utils import get_version, get_version_info
from .validators import UserValidator

__version__ = get_version()

__all__ = [
    # Core classes
    "ADConfig",
    "ServerConfig",
    "ADUserManager",
    "PowerShellADManager",
    "UserValidator",
    # Configuration models
    "DCServerConfig",
    "LDAPServerConfig",
    "UserAttributeMapping",
    "ConflictResolutionConfig",
    # Data classes
    "UserCreationResult",
    "UserInfo",
    # Functions
    "create_ad_manager",
    "run_automation",
    # Exceptions
    "ADUserManagerError",
    "ADConnectionError",
    "AuthenticationError",
    "UserExistsError",
    "UserNotFoundError",
    "ValidationError",
    "ConfigurationError",
    "LDAPOperationError",
    "SearchError",
    "UserCreationError",
    "PowerShellExecutionError",
    "RetryableError",
    "ADPermissionError",
    # Metadata
    "get_version",
    "get_version_info",
    "__version__",
]

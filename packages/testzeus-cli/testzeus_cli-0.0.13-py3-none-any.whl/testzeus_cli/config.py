"""
Configuration management for TestZeus CLI.
"""

from pathlib import Path
from typing import Dict, Any, Optional, Tuple

try:
    import yaml
    import keyring
except ImportError:
    # Handle case where optional dependencies aren't installed
    pass

# Config directory and file paths
CONFIG_DIR = Path.home() / ".testzeus"
CONFIG_FILE = CONFIG_DIR / "config.yaml"
KEYRING_SERVICE = "testzeus-cli"


def ensure_config_dir() -> None:
    """Ensure config directory exists"""
    CONFIG_DIR.mkdir(exist_ok=True)


def get_config_path() -> Path:
    """Get the path to the config file"""
    ensure_config_dir()
    return CONFIG_FILE


def load_config() -> Dict[str, Any]:
    """Load config from file"""
    config_path = get_config_path()

    if not config_path.exists():
        # Create default config
        default_config = {"default": {"api_url": "https://pb.prod.testzeus.app"}}
        with open(config_path, "w") as f:
            yaml.dump(default_config, f)
        return default_config

    with open(config_path, "r") as f:
        return yaml.safe_load(f) or {}


def save_config(config: Dict[str, Any]) -> None:
    """Save config to file"""
    config_path = get_config_path()

    with open(config_path, "w") as f:
        yaml.dump(config, f)


def get_profile_config(profile: str = "default") -> Dict[str, Any]:
    """Get config for a specific profile"""
    config = load_config()

    if profile not in config:
        config[profile] = {"api_url": "https://pb.prod.testzeus.app"}
        save_config(config)

    return config[profile]


def update_config(profile: str, updates: Dict[str, Any]) -> None:
    """Update config for a specific profile"""
    config = load_config()

    if profile not in config:
        config[profile] = {}

    for key, value in updates.items():
        if key == "password":
            # Store password in keyring
            keyring.set_password(KEYRING_SERVICE, f"{profile}:password", value)
        else:
            config[profile][key] = value

    save_config(config)


def get_client_config(
    profile: str = "default", api_url: Optional[str] = None
) -> Tuple[Dict[str, Any], Optional[str], Optional[str], Optional[str]]:
    """
    Get config for creating a TestZeusClient and the saved token/tenant_id/user_id if available

    Args:
        profile: Configuration profile to use
        api_url: Optional API URL to override profile setting

    Returns:
        A tuple of (client_config, token, tenant_id, user_id) where token, tenant_id, and user_id may be None
    """
    profile_config = get_profile_config(profile)

    client_config: Dict[str, Any] = {}
    token = None
    tenant_id = None
    user_id = None

    # Use provided API URL or fall back to profile config
    if api_url:
        client_config["base_url"] = api_url
    elif "api_url" in profile_config:
        client_config["base_url"] = profile_config.get("api_url")

    # Add email if present in config
    if "email" in profile_config:
        client_config["email"] = profile_config.get("email")

    # Get token if available, but don't add to client_config
    # as the SDK doesn't accept it as a constructor parameter
    if "token" in profile_config:
        token = profile_config.get("token")

    # Get tenant_id if available
    if "tenant_id" in profile_config:
        tenant_id = profile_config.get("tenant_id")

    # Get user_id if available
    if "user_id" in profile_config:
        user_id = profile_config.get("user_id")

    # Try to get password from keyring
    try:
        password = keyring.get_password(KEYRING_SERVICE, f"{profile}:password")
        if password:
            client_config["password"] = password
    except Exception:
        # Ignore keyring errors - password will need to be provided another way
        pass

    return client_config, token, tenant_id, user_id


def clear_auth_data(profile: str = "default") -> None:
    """Clear authentication data for a profile"""
    config = load_config()

    if profile in config:
        # Remove token if present
        if "token" in config[profile]:
            del config[profile]["token"]

        # Remove tenant_id if present
        if "tenant_id" in config[profile]:
            del config[profile]["tenant_id"]

        # Remove user_id if present
        if "user_id" in config[profile]:
            del config[profile]["user_id"]

        # Try to remove password from keyring
        try:
            keyring.delete_password(KEYRING_SERVICE, f"{profile}:password")
        except Exception:
            # Ignore keyring errors
            pass

        save_config(config)

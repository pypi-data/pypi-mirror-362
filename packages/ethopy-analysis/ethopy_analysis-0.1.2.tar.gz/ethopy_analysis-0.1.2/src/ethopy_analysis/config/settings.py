"""
Configuration management for Ethopy analysis.

This module handles loading and managing configuration from various sources
including JSON files, environment variables, and default settings.
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union

logger = logging.getLogger(__name__)

# Default configuration values
DEFAULT_CONFIG = {
    "database": {
        "host": "",
        "user": "",
        "password": "",
        "schemas": {
            "experiment": "lab_experiments",
            "stimulus": "lab_stimuli",
            "behavior": "lab_behavior",
        },
    },
    "paths": {"output_dir": "./output", "config_dir": "./config"},
}


def load_config(config_path: Optional[Union[str, Path]] = None, display_path: Optional[bool] = None) -> Dict[str, Any]:
    """Load configuration from file or use defaults.

    Args:
        config_path: Path to configuration file (optional)
        display_path: Whether to display the config path (optional)

    Returns:
        Configuration dictionary
    """
    # Start with default configuration
    config = DEFAULT_CONFIG.copy()

    # Try to load from file
    if config_path:
        config_file = Path(config_path)
    else:
        # Search for config file in common locations
        config_file = find_config_file()

    if config_file and config_file.exists():
        try:
            with open(config_file, "r") as f:
                file_config = json.load(f)
            # Merge file config with defaults
            config = merge_configs(config, file_config)
            if display_path:
                print(f"Configuration loaded from: {config_file}")
            logger.info(f"Loaded configuration from: {config_file}")

        except Exception as e:
            logger.warning(f"Failed to load config from {config_file}: {e}")
            logger.info("Using default configuration")
    else:
        logger.info("No config file found, using defaults")

    # Override with environment variables
    config = apply_env_overrides(config)

    # Validate the final configuration
    if not validate_config(config):
        logger.warning(
            "Configuration validation failed. The configuration may have issues. "
            "Check the logs above for specific problems."
        )

    return config


def find_config_file() -> Optional[Path]:
    """Find configuration file in common locations.

    Returns:
        Path to config file if found, None otherwise
    """
    # Common config file names and locations
    config_names = ["ethopy_config.json", "config.json", "dj_conf.json"]
    search_paths = [
        Path.cwd(),  # Current directory
        Path.cwd() / "config",  # Config subdirectory
        Path.home() / ".ethopy",  # User home directory
        Path(__file__).parent.parent.parent.parent,  # Package root
    ]

    for path in search_paths:
        for config_name in config_names:
            config_file = path / config_name
            if config_file.exists():
                logger.debug(f"Found config file: {config_file}")
                return config_file

    return None


def merge_configs(
    base_config: Dict[str, Any], override_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Recursively merge two configuration dictionaries.

    Args:
        base_config: Base configuration dictionary
        override_config: Configuration to merge in

    Returns:
        Merged configuration dictionary
    """
    result = base_config.copy()

    for key, value in override_config.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            result[key] = merge_configs(result[key], value)
        else:
            # Override or add new key
            result[key] = value

    return result


def apply_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
    """Apply environment variable overrides to configuration.

    Args:
        config: Base configuration dictionary

    Returns:
        Configuration with environment overrides applied
    """
    result = config.copy()

    # Database configuration overrides
    if "DJ_HOST" in os.environ:
        result["database"]["host"] = os.environ["DJ_HOST"]

    if "DJ_USER" in os.environ:
        result["database"]["user"] = os.environ["DJ_USER"]

    if "DJ_PASSWORD" in os.environ:
        result["database"]["password"] = os.environ["DJ_PASSWORD"]

    if "ETHOPY_OUTPUT_DIR" in os.environ:
        result["paths"]["output_dir"] = os.environ["ETHOPY_OUTPUT_DIR"]

    return result


def get_database_config(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get database configuration.

    Args:
        config: Full configuration dictionary (optional, will load if None)

    Returns:
        Database configuration dictionary
    """
    if config is None:
        config = load_config()

    return config.get("database", {})




def set_default_config(new_defaults: Dict[str, Any]):
    """Update default configuration values.

    Args:
        new_defaults: Dictionary with new default values
    """
    global DEFAULT_CONFIG

    DEFAULT_CONFIG = merge_configs(DEFAULT_CONFIG, new_defaults)

    logger.info("Updated default configuration")


def save_config(config: Dict[str, Any], config_path: Union[str, Path]):
    """Save configuration to a JSON file.

    Args:
        config: Configuration dictionary to save
        config_path: Path where to save the configuration
    """
    config_file = Path(config_path)

    # Create directory if it doesn't exist
    config_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)

        logger.info(f"Configuration saved to: {config_file}")

    except Exception as e:
        logger.error(f"Failed to save configuration to {config_file}: {e}")
        raise


def validate_config(config: Dict[str, Any]) -> bool:
    """Validate configuration structure and values.

    Checks for:
    - Required sections and keys
    - Invalid value types
    - Security issues

    Args:
        config: Configuration dictionary to validate

    Returns:
        True if valid, False otherwise
    """
    is_valid = True

    # Check for required sections
    required_sections = ["database", "paths"]
    for section in required_sections:
        if section not in config:
            logger.error(f"Missing required configuration section: {section}")
            is_valid = False

    # Validate database config if present
    if "database" in config:
        db_config = config["database"]
        required_db_keys = ["host", "user", "schemas"]

        for key in required_db_keys:
            if key not in db_config:
                logger.error(f"Missing required database configuration key: {key}")
                is_valid = False

        # Validate schema mappings
        if "schemas" in db_config:
            if not isinstance(db_config["schemas"], dict):
                logger.error("database.schemas must be a dictionary")
                is_valid = False
            else:
                required_schemas = ["experiment", "stimulus", "behavior"]
                for schema in required_schemas:
                    if schema not in db_config["schemas"]:
                        logger.warning(f"Missing schema mapping for '{schema}'")

    if is_valid:
        logger.debug("Configuration validation passed")
    else:
        logger.error("Configuration validation failed")

    return is_valid


def load_config_with_source(config_path: Optional[Union[str, Path]] = None) -> tuple[Dict[str, Any], Optional[Path]]:
    """Load configuration and return both config and source file path.

    Args:
        config_path: Path to configuration file (optional)

    Returns:
        Tuple of (configuration dictionary, source file path or None)
    """
    # Start with default configuration
    config = DEFAULT_CONFIG.copy()
    config_source = None

    # Try to load from file
    if config_path:
        config_file = Path(config_path)
    else:
        # Search for config file in common locations
        config_file = find_config_file()

    if config_file and config_file.exists():
        try:
            with open(config_file, "r") as f:
                file_config = json.load(f)
            # Merge file config with defaults
            config = merge_configs(config, file_config)
            config_source = config_file
            logger.info(f"Loaded configuration from: {config_file}")

        except Exception as e:
            logger.warning(f"Failed to load config from {config_file}: {e}")
            logger.info("Using default configuration")
    else:
        logger.info("No config file found, using defaults")

    # Apply environment variable overrides
    config = apply_env_overrides(config)

    # Validate configuration
    if not validate_config(config):
        logger.warning("Configuration validation failed")

    return config, config_source


def get_config_summary() -> str:
    """Get a summary of the current configuration.

    Returns:
        String summary of configuration
    """
    config, config_source = load_config_with_source()

    summary = "Ethopy Analysis Configuration Summary:\n"
    summary += "=" * 50 + "\n"

    # Configuration source
    if config_source:
        summary += f"Configuration file: {config_source}\n"
    else:
        summary += "Configuration file: Using defaults (no file found)\n"
    
    # Check for environment variable overrides
    env_vars = ["DJ_HOST", "DJ_USER", "DJ_PASSWORD", "ETHOPY_OUTPUT_DIR"]
    active_env_vars = [var for var in env_vars if var in os.environ]
    if active_env_vars:
        summary += f"Environment overrides: {', '.join(active_env_vars)}\n"
    
    summary += "\n"

    # Database info (without password)
    db_config = config["database"]
    summary += f"Database Host: {db_config.get('host', 'Not set')}\n"
    summary += f"Database User: {db_config.get('user', 'Not set')}\n"
    password_status = "Set" if db_config.get('password') else "Not set"
    summary += f"Database Password: {password_status}\n"
    summary += f"Schemas: {len(db_config.get('schemas', {}))}\n"

    # List schema mappings
    if db_config.get('schemas'):
        summary += "Schema mappings:\n"
        for schema_type, schema_name in db_config['schemas'].items():
            summary += f"  {schema_type}: {schema_name}\n"

    # Paths info
    paths_config = config["paths"]
    summary += f"\nOutput Directory: {paths_config.get('output_dir', './output')}\n"

    return summary

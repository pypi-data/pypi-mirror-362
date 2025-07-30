"""
Interactive configuration management for Ethopy analysis.

This module handles interactive prompts for missing configuration values
and secure credential management.
"""

import os
import getpass
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from .settings import load_config, save_config, get_database_config

logger = logging.getLogger(__name__)


def prompt_for_database_credentials(
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Prompt user for missing database credentials and optionally save them.

    Args:
        config: Optional existing configuration. If None, loads current config.

    Returns:
        Updated configuration dictionary with credentials
    """
    save_config = False
    if config is None:
        config = load_config()

    db_config = config.get("database", {})

    # Get host and user, prompt if missing
    host = db_config.get("host") or os.environ.get("DJ_HOST")
    user = db_config.get("user") or os.environ.get("DJ_USER")

    # Always check environment for password, never save it to config
    password = os.environ.get("DJ_PASSWORD")
    if not host or not user:
        save_config = True

    # Prompt for missing values
    if not host:
        host = input("Enter database host (e.g., database.example.org:3306): ").strip()

    if not user:
        user = input("Enter database username: ").strip()

    if not password:
        password = getpass.getpass("Enter database password: ")

    # Validate we got all required values
    if not host or not user or not password:
        missing = []
        if not host:
            missing.append("host")
        if not user:
            missing.append("username")
        if not password:
            missing.append("password")
        raise ValueError(f"Missing required credentials: {', '.join(missing)}")

    # Update config with host and user (but NOT password)
    updated_config = config.copy()
    updated_config["database"]["host"] = host
    updated_config["database"]["user"] = user
    # Do NOT save password to config file

    # Ask if user wants to save the configuration (without password)
    if save_config:
        if _should_save_config(host, user):
            _save_config_securely(updated_config)

    # Return config with password for this session only
    session_config = updated_config.copy()
    session_config["database"]["password"] = password

    return session_config


def _should_save_config(host: str, user: str) -> bool:
    """Ask user if they want to save the configuration."""
    print("\nWould you like to save this configuration?")
    print(f"  Host: {host}")
    print(f"  User: {user}")
    print("  Note: Password will NOT be saved for security reasons")

    while True:
        choice = input("Save configuration? (y/n): ").lower().strip()
        if choice in ["y", "yes"]:
            return True
        elif choice in ["n", "no"]:
            return False
        else:
            print("Please enter 'y' or 'n'")


def _save_config_securely(config: Dict[str, Any]) -> None:
    """Save configuration without password to default location."""
    try:
        # Default config file location
        config_path = Path.cwd() / "ethopy_config.json"

        # Ensure password is not saved
        config_to_save = config.copy()
        if "password" in config_to_save["database"]:
            del config_to_save["database"]["password"]

        save_config(config_to_save, config_path)

        print(f"✅ Configuration saved to: {config_path}")
        print("💡 Set DJ_PASSWORD environment variable or you'll be prompted each time")

    except Exception as e:
        logger.error(f"Failed to save configuration: {e}")
        print(f"❌ Failed to save configuration: {e}")


def setup_configuration_interactive() -> Dict[str, Any]:
    """
    Interactive setup wizard for first-time configuration.

    Returns:
        Complete configuration dictionary ready for use
    """
    print("=== Ethopy Analysis Configuration Setup ===\n")

    # Check if config already exists
    try:
        config = load_config()
        db_config = get_database_config(config)

        if db_config.get("host") and db_config.get("user"):
            print("✅ Existing configuration found!")
            print(f"   Host: {db_config.get('host')}")
            print(f"   User: {db_config.get('user')}")

            use_existing = input("Use existing configuration? (y/n): ").lower().strip()
            if use_existing in ["y", "yes"]:
                # Still need to get password
                password = os.environ.get("DJ_PASSWORD")
                if not password:
                    password = getpass.getpass("Enter database password: ")

                session_config = config.copy()
                session_config["database"]["password"] = password
                return session_config

    except Exception:
        # No existing config or error loading it, proceed with setup
        pass

    print("Setting up new database configuration...\n")

    # Get database credentials
    host = input("Database host (e.g., database.example.org:3306): ").strip()
    user = input("Database username: ").strip()
    password = getpass.getpass("Database password: ")

    if not host or not user or not password:
        raise ValueError("All database credentials are required")

    # Create config with default values
    config = load_config()  # Gets defaults
    config["database"]["host"] = host
    config["database"]["user"] = user
    config["database"]["password"] = password  # Only for this session

    print("\n=== Configuration Summary ===")
    print(f"Host: {host}")
    print(f"User: {user}")
    print(f"Schemas: {list(config['database']['schemas'].keys())}")

    # Test connection
    print("\nTesting database connection...")
    try:
        from ..db.schemas import test_connection

        if test_connection(config["database"]):
            print("✅ Connection successful!")
        else:
            print("❌ Connection failed!")
            return config
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return config

    # Save configuration (without password)
    if _should_save_config(host, user):
        _save_config_securely(config)

    print("\n=== Setup Complete ===")
    print("💡 Tip: Set DJ_PASSWORD environment variable to avoid password prompts")
    print("💡 Example: export DJ_PASSWORD='your_password'")

    return config


def get_database_config_interactive() -> Dict[str, Any]:
    """
    Get database configuration with interactive prompts for missing values.

    This is the main function that should be used instead of get_database_config()
    when interactive prompts are acceptable.

    Returns:
        Complete database configuration dictionary
    """
    try:
        # Try to load existing config
        config = load_config()
        db_config = get_database_config(config)

        # Check if we have all required values
        host = db_config.get("host") or os.environ.get("DJ_HOST")
        user = db_config.get("user") or os.environ.get("DJ_USER")
        password = os.environ.get("DJ_PASSWORD")  # Never from config file

        if host and user and password:
            # All values available, return immediately
            complete_config = config.copy()
            complete_config["database"]["password"] = password
            return complete_config["database"]

        # Missing values, prompt for them
        logger.info("Missing database credentials, prompting user...")
        complete_config = prompt_for_database_credentials(config)
        return complete_config["database"]

    except Exception as e:
        logger.error(f"Failed to get database configuration: {e}")
        print(f"\nDatabase configuration error: {e}")
        print("Run setup wizard? (y/n): ", end="")

        choice = input().lower().strip()
        if choice in ["y", "yes"]:
            config = setup_configuration_interactive()
            return config["database"]
        else:
            raise

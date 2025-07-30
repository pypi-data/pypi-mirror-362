"""Configuration management utilities for MLflow Assistant.

This module provides functions for loading, saving, and accessing configuration
settings for MLflow Assistant, including MLflow URI and AI provider settings.
Configuration is stored in YAML format in the user's home directory.
"""
import os
import yaml
from pathlib import Path
from typing import Any
import logging

from .constants import (
    CONFIG_KEY_MLFLOW_URI,
    CONFIG_KEY_PROVIDER,
    CONFIG_KEY_TYPE,
    CONFIG_KEY_MODEL,
    CONFIG_KEY_URI,
    CONFIG_KEY_API_KEY,
    MLFLOW_URI_ENV,
    OPENAI_API_KEY_ENV,
    Provider,
    DEFAULT_OLLAMA_URI,
    CONFIG_DIRNAME,
    CONFIG_FILENAME,
)

logger = logging.getLogger("mlflow_assistant.utils.config")

# Support testing by allowing override via environment variable
CONFIG_DIR = Path(
    os.environ.get(
        "MLFLOW_ASSISTANT_CONFIG_DIR", str(Path.home() / CONFIG_DIRNAME),
    ),
)
CONFIG_FILE = CONFIG_DIR / CONFIG_FILENAME


def ensure_config_dir():
    """Ensure the configuration directory exists."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
        logger.info(f"Created configuration directory at {CONFIG_DIR}")


def load_config() -> dict[str, Any]:
    """Load configuration from file."""
    if not CONFIG_FILE.exists():
        logger.info(f"No configuration file found at {CONFIG_FILE}")
        return {}

    try:
        with open(CONFIG_FILE) as f:
            config = yaml.safe_load(f) or {}
            logger.debug(f"Loaded configuration: {config}")
            return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        return {}


def save_config(config: dict[str, Any]) -> bool:
    """Save configuration to file.

    Args:
        config: Configuration dictionary to save

    Returns:
        bool: True if successful, False otherwise

    """
    ensure_config_dir()

    try:
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(config, f)
        logger.info(f"Configuration saved to {CONFIG_FILE}")
        return True
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        return False


def get_mlflow_uri() -> str | None:
    """Get the MLflow URI from config or environment.

    Returns:
        Optional[str]: The MLflow URI or None if not configured

    """
    # Environment variable should take precedence
    if mlflow_uri_env := os.environ.get(MLFLOW_URI_ENV):
        return mlflow_uri_env

    # Fall back to config
    config = load_config()
    return config.get(CONFIG_KEY_MLFLOW_URI)


def get_provider_config() -> dict[str, Any]:
    """Get the AI provider configuration.

    Returns:
        Dict[str, Any]: The provider configuration

    """
    config = load_config()
    provider = config.get(CONFIG_KEY_PROVIDER, {})

    provider_type = provider.get(CONFIG_KEY_TYPE)

    if provider_type == Provider.OPENAI.value:
        # Environment variable should take precedence
        api_key = (os.environ.get(OPENAI_API_KEY_ENV) or
                   provider.get(CONFIG_KEY_API_KEY))
        return {
            CONFIG_KEY_TYPE: Provider.OPENAI.value,
            CONFIG_KEY_API_KEY: api_key,
            CONFIG_KEY_MODEL: provider.get(
                CONFIG_KEY_MODEL, Provider.get_default_model(Provider.OPENAI),
            ),
        }

    if provider_type == Provider.OLLAMA.value:
        return {
            CONFIG_KEY_TYPE: Provider.OLLAMA.value,
            CONFIG_KEY_URI: provider.get(CONFIG_KEY_URI, DEFAULT_OLLAMA_URI),
            CONFIG_KEY_MODEL: provider.get(
                CONFIG_KEY_MODEL, Provider.get_default_model(Provider.OLLAMA),
            ),
        }

    return {CONFIG_KEY_TYPE: None}

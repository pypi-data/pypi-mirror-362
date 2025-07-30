"""Validation utilities for MLflow Assistant configuration.

This module provides validation functions to check MLflow connections,
AI provider configurations, and overall system setup to ensure proper
operation of MLflow Assistant.
"""
import logging
from typing import Any
import requests

# Import from utils module
from mlflow_assistant.utils.constants import Provider, CONFIG_KEY_TYPE, CONFIG_KEY_API_KEY, OPENAI_API_KEY_ENV, MLFLOW_VALIDATION_ENDPOINTS, MLFLOW_CONNECTION_TIMEOUT, OLLAMA_CONNECTION_TIMEOUT, OLLAMA_TAGS_ENDPOINT

from mlflow_assistant.utils.config import get_mlflow_uri, get_provider_config

logger = logging.getLogger("mlflow_assistant.cli.validation")


def validate_setup(check_api_key: bool = True) -> tuple[bool, str]:
    """Validate that MLflow Assistant is properly configured.

    Args:
        check_api_key: Whether to check for API key if using OpenAI

    Returns:
        Tuple[bool, str]: (is_valid, error_message)

    """
    # Check MLflow URI
    mlflow_uri = get_mlflow_uri()
    if not mlflow_uri:
        return (
            False,
            "MLflow URI not configured. "
            "Run 'mlflow-assistant setup' first.",
        )

    # Get provider config
    provider_config = get_provider_config()
    if not provider_config or not provider_config.get(CONFIG_KEY_TYPE):
        return (
            False,
            "AI provider not configured. "
            "Run 'mlflow-assistant setup' first.",
        )

    # Ensure OpenAI has an API key if that's the configured provider
    if (
        check_api_key
        and provider_config.get(CONFIG_KEY_TYPE) == Provider.OPENAI.value
        and not provider_config.get(CONFIG_KEY_API_KEY)
    ):
        return (
            False,
            f"OpenAI API key not found in environment. "
            f"Set {OPENAI_API_KEY_ENV}.",
        )

    return True, ""


def validate_mlflow_uri(uri: str) -> bool:
    """Validate MLflow URI by attempting to connect.

    Args:
        uri: MLflow server URI

    Returns:
        bool: True if connection successful, False otherwise

    """
    for endpoint in MLFLOW_VALIDATION_ENDPOINTS:
        try:
            # Try with trailing slash trimmed
            clean_uri = uri.rstrip("/")
            url = f"{clean_uri}{endpoint}"
            logger.debug(f"Trying to connect to MLflow at: {url}")

            response = requests.get(url, timeout=MLFLOW_CONNECTION_TIMEOUT)
            if response.status_code == 200:
                logger.info(f"Successfully connected to MLflow at {url}")
                return True
            logger.debug(f"Response from {url}: {response.status_code}")
        except Exception as e:
            logger.debug(f"Failed to connect to {endpoint}: {e!s}")

    # If we get here, none of the endpoints worked
    logger.warning(
        f"Could not validate MLflow at {uri} on any standard endpoint",
    )
    return False


def validate_ollama_connection(uri: str) -> tuple[bool, dict[str, Any]]:
    """Validate Ollama connection and get available models.

    Args:
        uri: Ollama server URI

    Returns:
        Tuple[bool, Dict[str, Any]]: (is_valid, response_data)

    """
    try:
        response = requests.get(
            f"{uri}{OLLAMA_TAGS_ENDPOINT}", timeout=OLLAMA_CONNECTION_TIMEOUT,
        )
        if response.status_code == 200:
            try:
                models_data = response.json()
                available_models = [
                    m.get("name") for m in models_data.get("models", [])
                ]
                return True, {"models": available_models}
            except Exception as e:
                logger.debug(f"Error parsing Ollama models: {e}")
                return True, {"models": []}
        else:
            return False, {}
    except Exception as e:
        logger.debug(f"Error connecting to Ollama: {e}")
        return False, {}

"""Constants and enumerations for MLflow Assistant.

This module defines configuration keys, default values, API endpoints,
model definitions, and other constants used throughout MLflow Assistant.
It includes enums for AI providers (OpenAI, Ollama) and their supported models.
"""
from enum import Enum

# Configuration keys
CONFIG_KEY_MLFLOW_URI = "mlflow_uri"
CONFIG_KEY_PROVIDER = "provider"
CONFIG_KEY_TYPE = "type"
CONFIG_KEY_MODEL = "model"
CONFIG_KEY_URI = "uri"
CONFIG_KEY_API_KEY = "api_key"

# Environment variables
MLFLOW_URI_ENV = "MLFLOW_TRACKING_URI"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

# Default values
DEFAULT_MLFLOW_URI = "http://localhost:5000"
DEFAULT_OLLAMA_URI = "http://localhost:11434"

# Connection timeouts
MLFLOW_CONNECTION_TIMEOUT = 5  # seconds
OLLAMA_CONNECTION_TIMEOUT = 2  # seconds

# Status messages
DEFAULT_STATUS_NOT_CONFIGURED = "Not configured"
DEFAULT_STATUS_UNKNOWN = "Unknown"

# API endpoints
OLLAMA_TAGS_ENDPOINT = "/api/tags"
MLFLOW_VALIDATION_ENDPOINTS = [
    "/api/2.0/mlflow/experiments/list",  # Standard REST API
    "/ajax-api/2.0/mlflow/experiments/list",  # Alternative path
    "/",  # Root path (at least check if the server responds)
]

# Configuration
CONFIG_DIRNAME = ".mlflow-assistant"
CONFIG_FILENAME = "config.yaml"

# Logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


# Default model OpenAI names
class OpenAIModel(Enum):
    """OpenAI models supported by MLflow Assistant."""

    GPT35 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"
    GPT4_TURBO = "gpt-4-turbo"
    GPT4O = "gpt-4o"

    @classmethod
    def choices(cls):
        """Get all available OpenAI model choices."""
        return [model.value for model in cls]


# Default Ollama offered model names
class OllamaModel(Enum):
    """Default Ollama models supported by MLflow Assistant."""

    LLAMA32 = "llama3.2:latest"
    GEMMA2 = "gemma2:latest"
    PHI4 = "phi4:latest"

    @classmethod
    def choices(cls):
        """Get all available Ollama model choices."""
        return [model.value for model in cls]


# Provider types
class Provider(Enum):
    """AI provider types supported by MLflow Assistant."""

    OPENAI = "openai"
    OLLAMA = "ollama"

    @classmethod
    def get_default_model(cls, provider):
        """Get the default model for a provider."""
        defaults = {
            cls.OPENAI: OpenAIModel.GPT35.value,
            cls.OLLAMA: OllamaModel.LLAMA32.value,
        }
        return defaults.get(provider)


# Special commands for interactive chat sessions
class Command(Enum):
    """Special commands for interactive chat sessions."""

    EXIT = "/bye"
    HELP = "/help"
    CLEAR = "/clear"

    @property
    def description(self):
        """Get the description for a command."""
        descriptions = {
            self.EXIT: "Exit the chat session",
            self.HELP: "Show this help message",
            self.CLEAR: "Clear the screen",
        }
        return descriptions.get(self, "No description available")

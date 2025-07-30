"""Constants and definitions for the MLflow Assistant."""
from dataclasses import dataclass


# Environment variable names for MLflow connection
MLFLOW_TRACKING_URI_ENV = "MLFLOW_TRACKING_URI"

# Default values
DEFAULT_MLFLOW_TRACKING_URI = "http://localhost:5000"

# Connection types
LOCAL_CONNECTION = "local"
REMOTE_CONNECTION = "remote"


@dataclass
class MLflowConnectionConfig:
    """Configuration for MLflow connection."""

    tracking_uri: str

    @property
    def connection_type(self) -> str:
        """Return the connection type (local or remote)."""
        if self.tracking_uri.startswith(("http://", "https://")):
            return REMOTE_CONNECTION
        return LOCAL_CONNECTION

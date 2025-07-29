"""MLflow connection module for handling connections to MLflow Tracking Server.

This module provides functionality to connect to both local and remote MLflow Tracking Servers
using environment variables or direct configuration.
"""

import os
import logging
from typing import Any

import mlflow
from mlflow.tracking import MlflowClient

from mlflow_assistant.utils.definitions import (
    MLflowConnectionConfig,
    MLFLOW_TRACKING_URI_ENV,
    DEFAULT_MLFLOW_TRACKING_URI,
)
from mlflow_assistant.utils.exceptions import MLflowConnectionError

logger = logging.getLogger(__name__)


class MLflowConnection:
    """MLflow connection class to handle connections to MLflow Tracking Server.

    This class provides functionality to connect to both local and remote
    MLflow Tracking Servers.
    """

    def __init__(self, tracking_uri: str | None = None, client_factory=None):
        """Initialize MLflow connection.

        Args:
        ----
            tracking_uri: URI of the MLflow Tracking Server. If None, will try to get from environment.
            client_factory: A callable to create the MlflowClient instance. Defaults to MlflowClient.

        """
        self.config = self._load_config(tracking_uri=tracking_uri)
        self.client = None
        self.is_connected_flag = False
        self.client_factory = client_factory or MlflowClient

    def _load_config(self, tracking_uri: str | None = None) -> MLflowConnectionConfig:
        """Load configuration from environment variables or explicit parameters.

        Args:
        ----
            tracking_uri: URI of the MLflow Tracking Server. If None, will try to get from environment.

        Returns:
        -------
            MLflowConnectionConfig: Configuration for MLflow connection.

        """
        tracking_uri = tracking_uri or os.environ.get(MLFLOW_TRACKING_URI_ENV, DEFAULT_MLFLOW_TRACKING_URI)
        return MLflowConnectionConfig(tracking_uri=tracking_uri)

    def connect(self) -> tuple[bool, str]:
        """Connect to MLflow Tracking Server.

        Returns
        -------
            Tuple[bool, str]: (success, message)

        """
        try:
            logger.info(f"Connecting to MLflow Tracking Server at {self.config.tracking_uri}")
            mlflow.set_tracking_uri(self.config.tracking_uri)
            self.client = self.client_factory(tracking_uri=self.config.tracking_uri)
            self.client.search_experiments()  # Trigger connection attempt
            self.is_connected_flag = True
            logger.info(f"Successfully connected to MLflow Tracking Server at {self.config.tracking_uri}")
            return True, f"Successfully connected to MLflow Tracking Server at {self.config.tracking_uri}"
        except Exception as e:
            self.is_connected_flag = False
            logger.exception(f"Failed to connect to MLflow Tracking Server: {e}")
            return False, f"Failed to connect to MLflow Tracking Server: {e!s}"

    def get_client(self) -> MlflowClient:
        """Get MLflow client instance.

        Returns
        -------
            MlflowClient: MLflow client instance.

        Raises
        ------
            MLflowConnectionError: If not connected to MLflow Tracking Server.

        """
        if self.client is None:
            msg = "Not connected to MLflow Tracking Server. Call connect() first."
            raise MLflowConnectionError(msg)
        return self.client

    def is_connected(self) -> bool:
        """Check if connected to MLflow Tracking Server.

        Returns
        -------
            bool: True if connected, False otherwise.

        """
        return self.is_connected_flag

    def get_connection_info(self) -> dict[str, Any]:
        """Get connection information.

        Returns
        -------
            Dict[str, Any]: Connection information.

        """
        return {
            "tracking_uri": self.config.tracking_uri,
            "connection_type": self.config.connection_type,
            "is_connected": self.is_connected_flag,
        }

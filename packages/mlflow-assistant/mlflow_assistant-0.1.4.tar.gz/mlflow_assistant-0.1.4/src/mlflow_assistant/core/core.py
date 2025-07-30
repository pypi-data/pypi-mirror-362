"""Core utilities and functionality for MLflow Assistant.

This module provides foundational classes, functions, and utilities used across the
MLflow Assistant project, including shared logic for managing workflows and interactions
with the MLflow Tracking Server.
"""
from mlflow.tracking import MlflowClient


def get_mlflow_client():
    """Initialize and return an MLflow client instance.

    Returns
    -------
        MlflowClient: An instance of the MLflow client.

    """
    return MlflowClient()

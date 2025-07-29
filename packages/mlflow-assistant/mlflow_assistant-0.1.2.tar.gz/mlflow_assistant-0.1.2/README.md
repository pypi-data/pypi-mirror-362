# MLflow Assistant

[![CI/CD Pipeline](https://github.com/hugodscarvalho/mlflow-assistant/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/hugodscarvalho/mlflow-assistant/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/hugodscarvalho/mlflow-assistant/branch/main/graph/badge.svg)](https://codecov.io/gh/hugodscarvalho/mlflow-assistant)
[![PyPI version](https://img.shields.io/pypi/v/mlflow-assistant.svg)](https://pypi.org/project/mlflow-assistant/)
[![Python versions](https://img.shields.io/pypi/pyversions/mlflow-assistant.svg)](https://pypi.org/project/mlflow-assistant/)
[![License](https://img.shields.io/github/license/hugodscarvalho/mlflow-assistant.svg)](LICENSE)

`mlflow-assistant` is an MLflow plugin that enables natural language conversations with your MLflow server using LLM providers like OpenAI and Ollama.

## Features

- Interact with your MLflow server using natural language.
- Powered by large language models (LLMs).
- Easy integration with MLflow.

## Installation

To install the package, use:

```bash
pip install mlflow-assistant
```

## Requirements

- Python >= 3.9
- MLflow >= 2.21.0, < 3.0.0

## Usage

### Example: Initialize MLflow Client

You can use the `get_mlflow_client` function to initialize an MLflow client:

```python
from mlflow_assistant.core.core import get_mlflow_client

client = get_mlflow_client()
print(client)
```
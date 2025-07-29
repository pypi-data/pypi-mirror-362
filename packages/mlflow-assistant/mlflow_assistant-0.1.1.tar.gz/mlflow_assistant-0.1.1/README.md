# MLflow Assistant

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
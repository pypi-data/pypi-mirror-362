"""Setup wizard for MLflow Assistant configuration.

This module provides an interactive setup wizard that guides users through
configuring MLflow Assistant, including MLflow connection settings and
AI provider configuration (OpenAI or Ollama).
"""
import os
import click
import logging

from mlflow_assistant.utils.config import load_config, save_config
from .validation import validate_mlflow_uri, validate_ollama_connection
from mlflow_assistant.utils.constants import Provider, OpenAIModel, CONFIG_KEY_MLFLOW_URI, CONFIG_KEY_PROVIDER, CONFIG_KEY_TYPE, CONFIG_KEY_MODEL, CONFIG_KEY_URI, DEFAULT_MLFLOW_URI, DEFAULT_OLLAMA_URI, OPENAI_API_KEY_ENV

logger = logging.getLogger("mlflow_assistant.setup")


def setup_wizard():
    """Interactive setup wizard for mlflow-assistant."""
    click.echo("┌──────────────────────────────────────────────────────┐")
    click.echo("│             MLflow Assistant Setup Wizard            │")
    click.echo("└──────────────────────────────────────────────────────┘")

    click.echo("\nThis wizard will help you configure MLflow Assistant.")

    # Initialize config
    config = load_config()
    previous_provider = config.get(
        CONFIG_KEY_PROVIDER, {}).get(CONFIG_KEY_TYPE)

    # MLflow URI
    mlflow_uri = click.prompt(
        "Enter your MLflow URI",
        default=config.get(CONFIG_KEY_MLFLOW_URI, DEFAULT_MLFLOW_URI),
    )

    if not validate_mlflow_uri(mlflow_uri):
        click.echo("\n⚠️  Warning: Could not connect to MLflow URI.")
        click.echo(
            "    Please ensure MLflow is running.",
        )
        click.echo(
            "    Common MLflow URLs: http://localhost:5000, "
            "http://localhost:8080",
        )
        if not click.confirm(
            "Continue anyway? (Choose Yes if you're sure MLflow is running)",
        ):
            click.echo(
                "Setup aborted. "
                "Please ensure MLflow is running and try again.")
            return
        click.echo("Continuing with setup using the provided MLflow URI.")
    else:
        click.echo("✅ Successfully connected to MLflow!")

    config[CONFIG_KEY_MLFLOW_URI] = mlflow_uri

    # AI Provider
    provider_options = [p.value.capitalize() for p in Provider]
    provider_choice = click.prompt(
        "\nWhich AI provider would you like to use?",
        type=click.Choice(provider_options, case_sensitive=False),
        default=config.get(CONFIG_KEY_PROVIDER, {})
        .get(CONFIG_KEY_TYPE, Provider.OPENAI.value)
        .capitalize(),
    )

    current_provider_type = provider_choice.lower()
    provider_config = {}

    # Check if provider is changing and handle default models
    provider_changed = (previous_provider and
                        previous_provider != current_provider_type)

    if current_provider_type == Provider.OPENAI.value:
        # If switching from another provider, show a message
        if provider_changed:
            click.echo("\n✅ Switching to OpenAI provider")

        # Initialize provider config
        provider_config = {
            CONFIG_KEY_TYPE: Provider.OPENAI.value,
            CONFIG_KEY_MODEL: Provider.get_default_model(
                Provider.OPENAI,
            ),  # Will be updated after user selection
        }

        # Check for OpenAI API key
        api_key = os.environ.get(OPENAI_API_KEY_ENV)
        if not api_key:
            click.echo(
                "\n⚠️  OpenAI API key not found in environment variables.",
            )
            click.echo(
                f"Please export your OpenAI API key as {OPENAI_API_KEY_ENV}.",
            )
            click.echo(f"Example: export {OPENAI_API_KEY_ENV}='your-key-here'")
            if not click.confirm("Continue without API key?"):
                click.echo(
                    "Setup aborted. Please set the API key and try again.",
                )
                return
        else:
            click.echo("✅ Found OpenAI API key in environment!")

        # Always ask for model choice
        model_choices = OpenAIModel.choices()

        # If changing providers, suggest the default,
        # otherwise use previous config
        if provider_changed:
            suggested_model = Provider.get_default_model(Provider.OPENAI)
        else:
            current_model = config.get(CONFIG_KEY_PROVIDER, {}).get(
                CONFIG_KEY_MODEL, Provider.get_default_model(Provider.OPENAI),
            )
            suggested_model = (
                current_model
                if current_model in model_choices
                else Provider.get_default_model(Provider.OPENAI)
            )

        model = click.prompt(
            "Choose an OpenAI model",
            type=click.Choice(model_choices, case_sensitive=False),
            default=suggested_model,
        )
        provider_config[CONFIG_KEY_MODEL] = model

    elif current_provider_type == Provider.OLLAMA.value:
        # If switching from another provider, automatically set defaults
        if provider_changed:
            click.echo(
                "\n✅ Switching to Ollama provider with default URI and model",
            )

        # Ollama configuration - always ask for URI
        ollama_uri = click.prompt(
            "\nEnter your Ollama server URI",
            default=config.get(CONFIG_KEY_PROVIDER, {}).get(
                CONFIG_KEY_URI, DEFAULT_OLLAMA_URI,
            ),
        )

        # Initialize provider config with default model and user-specified URI
        provider_config = {
            CONFIG_KEY_TYPE: Provider.OLLAMA.value,
            CONFIG_KEY_URI: ollama_uri,
            CONFIG_KEY_MODEL: Provider.get_default_model(
                Provider.OLLAMA,
            ),  # Will be updated if user selects a different model
        }

        # Check if Ollama is running
        is_connected, ollama_data = validate_ollama_connection(ollama_uri)
        if is_connected:
            click.echo("✅ Ollama server is running!")

            # Get available models
            available_models = ollama_data.get("models", [])

            if available_models:
                click.echo(
                    f"\nAvailable Ollama models: {', '.join(available_models)}",
                )

                # If changing providers, suggest the default,
                # otherwise use previous config
                default_model = Provider.get_default_model(Provider.OLLAMA)
                if provider_changed:
                    suggested_model = (
                        default_model
                        if default_model in available_models
                        else available_models[0]
                    )
                else:
                    current_model = config.get(CONFIG_KEY_PROVIDER, {}).get(
                        CONFIG_KEY_MODEL,
                    )
                    suggested_model = (
                        current_model
                        if current_model in available_models
                        else default_model
                    )

                ollama_model = click.prompt(
                    "Choose an Ollama model",
                    type=click.Choice(available_models, case_sensitive=True),
                    default=suggested_model,
                )
                provider_config[CONFIG_KEY_MODEL] = ollama_model
            else:
                click.echo("\nNo models found. Using default model.")
                ollama_model = click.prompt(
                    "Enter the Ollama model to use",
                    default=config.get(CONFIG_KEY_PROVIDER, {}).get(
                        CONFIG_KEY_MODEL, Provider.get_default_model(
                            Provider.OLLAMA,
                        ),
                    ),
                )
                provider_config[CONFIG_KEY_MODEL] = ollama_model
        else:
            click.echo(
                "\n⚠️  Warning: Ollama server not running or"
                " not accessible at this URI.",
            )
            if not click.confirm("Continue anyway?"):
                click.echo(
                    "Setup aborted. Please start Ollama server and try again.",
                )
                return

            # Still prompt for model name
            ollama_model = click.prompt(
                "Enter the Ollama model to use",
                default=config.get(CONFIG_KEY_PROVIDER, {}).get(
                    CONFIG_KEY_MODEL, Provider.get_default_model(
                        Provider.OLLAMA,
                    ),
                ),
            )
            provider_config[CONFIG_KEY_MODEL] = ollama_model

    config[CONFIG_KEY_PROVIDER] = provider_config

    # Save the configuration
    save_config(config)

    click.echo("\n✅ Configuration saved successfully!")
    click.echo("\n┌──────────────────────────────────────────────────┐")
    click.echo("│               Getting Started                    │")
    click.echo("└──────────────────────────────────────────────────┘")
    click.echo(
        "\nYou can now use MLflow Assistant with the following commands:")
    click.echo(
        "  mlflow-assistant start     - Start an interactive chat "
        "session.",
    )
    click.echo(
        "  mlflow-assistant version   - Show version "
        "information.",
    )

    click.echo("\nFor more information, use 'mlflow-assistant --help'")

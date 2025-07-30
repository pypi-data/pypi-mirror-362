"""CLI commands for MLflow Assistant.

This module contains the main CLI commands for interacting with MLflow
using natural language queries through various AI providers.
"""
import click
import logging
from typing import Any

# Internal imports
from mlflow_assistant.utils.config import load_config, get_mlflow_uri, get_provider_config
from mlflow_assistant.utils.constants import Command, CONFIG_KEY_MLFLOW_URI, CONFIG_KEY_PROVIDER, CONFIG_KEY_TYPE, CONFIG_KEY_MODEL, DEFAULT_STATUS_NOT_CONFIGURED, LOG_FORMAT
from .setup import setup_wizard
from .validation import validate_setup

# Set up logging
logger = logging.getLogger("mlflow_assistant.cli")


def _handle_special_commands(query: str) -> str | None:
    """Handle special chat commands.

    Args:
        query: The user's input query

    Returns:
        Action to take ('exit', 'help', 'clear', 'continue') or None to process normally

    """
    query_lower = query.lower()

    if query_lower == Command.EXIT.value:
        click.echo("\nThank you for using MLflow Assistant! Goodbye.")
        return "exit"

    if query_lower == Command.HELP.value:
        click.echo("\nAvailable commands:")
        for cmd in Command:
            click.echo(f"  {cmd.value:<7} - {cmd.description}")
        return "continue"

    if query_lower == Command.CLEAR.value:
        # This is a simple approximation of clear screen
        click.echo("\n" * 50)
        return "continue"

    if not query:
        return "continue"  # Skip empty queries

    return None  # Process normally


def _process_user_query(query: str, provider_config: dict, verbose: bool) -> None:
    """Process a user query and display the response.

    Args:
        query: The user's query
        provider_config: The AI provider configuration
        verbose: Whether to show verbose output

    """
    try:
        # This is a mock function call
        result = mock_process_query(query, provider_config, verbose)

        # Display response
        click.echo(f"\n🤖 {result['response']}")

        # Show verbose info if requested
        if verbose:
            provider_type = provider_config.get(
                CONFIG_KEY_TYPE, DEFAULT_STATUS_NOT_CONFIGURED,
            )
            model = provider_config.get(
                CONFIG_KEY_MODEL, DEFAULT_STATUS_NOT_CONFIGURED,
            )
            click.echo("\n--- Debug Information ---")
            click.echo(f"Provider: {provider_type}")
            click.echo(f"Model: {model}")
            click.echo("Query processed with mock function")
            click.echo("-------------------------")

    except Exception as e:
        click.echo(f"\n❌ Error processing query: {e!s}")


# Mock function for process_query since it's not implemented yet
def mock_process_query(
    query: str, provider_config: dict[str, Any], verbose: bool = False,
) -> dict[str, Any]:
    """Mock function that simulates the query processing workflow.

    This will be replaced with the actual implementation later.

    Args:
        query: The user's query
        provider_config: The AI provider configuration
        verbose: Whether to show verbose output

    Returns:
        Dictionary with mock response information

    """
    # Create a mock response
    provider_type = provider_config.get(
        CONFIG_KEY_TYPE, DEFAULT_STATUS_NOT_CONFIGURED,
    )
    model = provider_config.get(
        CONFIG_KEY_MODEL, DEFAULT_STATUS_NOT_CONFIGURED,
    )

    response_text = (
        f"This is a mock response to: '{query}'\n\n"
        f"The MLflow integration will be implemented soon!"
    )

    if verbose:
        response_text += f"\n\nDebug: Using {provider_type} with {model}"

    return {
        "original_query": query,
        "provider_config": {
            CONFIG_KEY_TYPE: provider_type,
            CONFIG_KEY_MODEL: model,
        },
        "enhanced": False,
        "response": response_text,
    }


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
def cli(verbose):
    """MLflow Assistant: Interact with MLflow using LLMs.

    This CLI tool helps you to interact with MLflow using natural language.
    """
    # Configure logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format=LOG_FORMAT)


@cli.command()
def setup():
    """Run the interactive setup wizard.

    This wizard helps you configure MLflow Assistant.
    """
    setup_wizard()


@cli.command()
@click.option("--verbose", "-v", is_flag=True, help="Show verbose output")
def start(verbose):
    """Start an interactive chat session with MLflow Assistant.

    This opens an interactive chat session where you can ask questions about
    your MLflow experiments, models, and data. Type /bye to exit the session.

    Examples of questions you can ask:
    - What are my best performing models for classification?
    - Show me details of experiment 'customer_churn'
    - Compare runs abc123 and def456
    - Which hyperparameters should I try next for my regression model?

    Commands:
    - /bye: Exit the chat session
    - /help: Show help about available commands
    - /clear: Clear the screen
    """
    # Use validation function to check setup
    is_valid, error_message = validate_setup()
    if not is_valid:
        click.echo(f"❌ Error: {error_message}")
        return

    # Get provider config
    provider_config = get_provider_config()

    # Print welcome message and instructions
    provider_type = provider_config.get(
        CONFIG_KEY_TYPE, DEFAULT_STATUS_NOT_CONFIGURED,
        )
    model = provider_config.get(
        CONFIG_KEY_MODEL, DEFAULT_STATUS_NOT_CONFIGURED,
        )

    click.echo("\n🤖 MLflow Assistant Chat Session")
    click.echo(f"Connected to MLflow at: {get_mlflow_uri()}")
    click.echo(f"Using {provider_type.upper()} with model: {model}")
    click.echo("\nType your questions and press Enter.")
    click.echo(f"Type {Command.EXIT.value} to exit.")
    click.echo("=" * 70)

    # Start interactive loop
    while True:
        # Get user input with a prompt
        try:
            query = click.prompt("\n🧑", prompt_suffix="").strip()
        except (KeyboardInterrupt, EOFError):
            click.echo("\nExiting chat session...")
            break

        # Handle special commands
        action = _handle_special_commands(query)
        if action == "exit":
            break
        if action == "continue":
            continue

        # Process the query
        _process_user_query(query, provider_config, verbose)


@cli.command()
def version():
    """Show MLflow Assistant version information."""
    from mlflow_assistant import __version__

    click.echo(f"MLflow Assistant version: {__version__}")

    # Show configuration
    config = load_config()
    mlflow_uri = config.get(
        CONFIG_KEY_MLFLOW_URI, DEFAULT_STATUS_NOT_CONFIGURED,
        )
    provider = config.get(CONFIG_KEY_PROVIDER, {}).get(
        CONFIG_KEY_TYPE, DEFAULT_STATUS_NOT_CONFIGURED,
    )
    model = config.get(CONFIG_KEY_PROVIDER, {}).get(
        CONFIG_KEY_MODEL, DEFAULT_STATUS_NOT_CONFIGURED,
    )

    click.echo(f"MLflow URI: {mlflow_uri}")
    click.echo(f"Provider: {provider}")
    click.echo(f"Model: {model}")


if __name__ == "__main__":
    cli()

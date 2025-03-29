"""
Eidosian Ollama Model Browser
==============================

This script provides an efficient, modular, and extensible interface for browsing models on
Ollama using the Ollama API. It adheres to Eidosian principles for clarity, performance, and future-proofing.

Key Features:
- Efficient model search using the Ollama API.
- Filtering and sorting based on criteria.
- Clear, self-documenting code with strict type safety.
- Modular design for extensibility.

Requirements:
- Python 3.10 or higher
- `requests` library (`pip install requests`)

Author:
- Eidos, in collaboration with Lloyd Handyside
"""

from typing import Any, Dict, List

import requests

# Constants
OLLAMA_API_URL: str = "http://localhost:11434/api/tags"  # Assumes local Ollama server


# Exceptions
class OllamaAPIError(Exception):
    """Raised when the Ollama API returns an error."""

    pass


class ValidationError(Exception):
    """Raised for invalid input parameters."""

    pass


# API Functions
def fetch_models() -> List[Dict[str, Any]]:
    """
    Fetches available models from the Ollama API.

    Returns:
        List[Dict[str, Any]]: List of available model data as dictionaries.

    Raises:
        OllamaAPIError: If the API request fails.
    """
    try:
        response = requests.get(OLLAMA_API_URL)
        if response.status_code != 200:
            raise OllamaAPIError(f"API Error: {response.status_code} - {response.text}")
        return response.json().get("models", [])
    except requests.RequestException as e:
        raise OllamaAPIError(f"Network Error: {e}")


# Filtering and Sorting Functions
def filter_models(
    models: List[Dict[str, Any]], key: str, value: Any
) -> List[Dict[str, Any]]:
    """
    Filters a list of models based on a specific key-value pair.

    Args:
        models (List[Dict[str, Any]]): List of model dictionaries.
        key (str): Model dictionary key to filter by.
        value (Any): Desired value to match.

    Returns:
        List[Dict[str, Any]]: Filtered list of models.
    """
    return [model for model in models if model.get(key) == value]


def sort_models(
    models: List[Dict[str, Any]], key: str, reverse: bool = False
) -> List[Dict[str, Any]]:
    """
    Sorts a list of models based on a specific key.

    Args:
        models (List[Dict[str, Any]]): List of model dictionaries.
        key (str): Model dictionary key to sort by.
        reverse (bool): Sort in descending order if True.

    Returns:
        List[Dict[str, Any]]: Sorted list of models.
    """
    return sorted(models, key=lambda model: model.get(key, 0), reverse=reverse)


# Display Function
def display_models(models: List[Dict[str, Any]]) -> None:
    """
    Displays model information in a readable format.

    Args:
        models (List[Dict[str, Any]]): List of model dictionaries to display.
    """
    if not models:
        print("No models found.")
        return

    print(f"\nFound {len(models)} model(s):")
    for model in models:
        print(
            f"📌 Model: {model.get('name', 'Unknown')} | Digest: {model.get('digest', 'N/A')} | Size: {model.get('size', 'N/A')}"
        )


# Main Execution
def main() -> None:
    """
    Main entry point for executing the Ollama model browser.
    """
    print("Welcome to the Eidosian Ollama Model Browser")

    try:
        models = fetch_models()

        if not models:
            print("No models available on the Ollama server.")
            return

        # Display initial results
        display_models(models)

        # Optional filtering
        filter_choice = (
            input("Would you like to filter the models? (y/n): ").strip().lower()
        )
        if filter_choice == "y":
            filter_key = input(
                "Enter the key to filter by (e.g., 'name', 'digest'): "
            ).strip()
            filter_value = input(
                f"Enter the desired value for '{filter_key}': "
            ).strip()
            models = filter_models(models, filter_key, filter_value)
            display_models(models)

        # Optional sorting
        sort_choice = input("Sort models by size? (y/n): ").strip().lower()
        if sort_choice == "y":
            models = sort_models(models, key="size", reverse=True)
            display_models(models)

    except (OllamaAPIError, ValidationError) as e:
        print(f"Error: {e}")

    except KeyboardInterrupt:
        print("\nProcess interrupted. Goodbye.")


if __name__ == "__main__":
    main()

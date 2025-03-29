"""
Eidosian Model Manager
======================

Central coordination system for multi-source model management with unified interfaces
for searching, installing, and managing models from Ollama and Hugging Face.

Key Features:
- Universal search across all configured model sources
- Unified model installation regardless of source
- Efficient local model management with source-specific handlers
- Extensible architecture for adding new model sources
- Complete type safety with Protocol interfaces
"""

import asyncio
import json
import os
from dataclasses import asdict
from typing import Dict, List, Optional, Tuple

from ollama_forge.src.ollama_forge.models.browse_remote_huggingface_models import (
    HuggingFaceModelProvider,
)
from ollama_forge.src.ollama_forge.models.browse_remote_ollama_models import (
    OllamaRemoteModelProvider,
)
from ollama_forge.src.ollama_forge.models.list_local_ollama_models import (
    OllamaLocalModelProvider,
)

from . import ModelInfo, ModelInstaller, ModelProvider, ModelSource

# Type aliases
SearchResult = Tuple[int, ModelInfo]  # Score, Model
SearchResults = List[SearchResult]


class ModelManager:
    """Core manager for unified model operations across multiple sources."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the model manager with optional configuration.

        Args:
            config_path: Path to configuration file. If None, default config is used.
        """
        self.providers: Dict[ModelSource, ModelProvider] = {}
        self.installers: Dict[ModelSource, ModelInstaller] = {}

        # Cache of installed models
        self.installed_models: Dict[str, ModelInfo] = {}

        # Initialize default configuration
        self.config = self._load_config(config_path)

        # Register default providers and installers
        self._register_default_providers()

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or use defaults.

        Args:
            config_path: Path to configuration file

        Returns:
            Dict: Configuration dictionary
        """
        default_config = {
            "ollama_api_url": "http://localhost:11434/api",
            "cache_dir": os.path.expanduser("~/.ollama_forge/cache"),
            "index_path": os.path.expanduser("~/.ollama_forge/model_index.json"),
        }

        if not config_path or not os.path.exists(config_path):
            return default_config

        try:
            with open(config_path, "r") as f:
                user_config = json.load(f)
                # Update defaults with user configuration
                default_config.update(user_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Warning: Could not load config from {config_path}: {e}")

        return default_config

    def _register_default_providers(self) -> None:
        """Register the default model providers and installers."""
        # Ensure cache directory exists
        os.makedirs(self.config["cache_dir"], exist_ok=True)

        # Register Ollama local provider
        ollama_local = OllamaLocalModelProvider(
            api_base_url=self.config["ollama_api_url"]
        )
        self.register_provider(ModelSource.OLLAMA_LOCAL, ollama_local)
        self.register_installer(ModelSource.OLLAMA_LOCAL, ollama_local)

        # Register Ollama remote provider
        ollama_remote = OllamaRemoteModelProvider(
            index_path=os.path.join(
                self.config["cache_dir"], "ollama_remote_index.json"
            )
        )
        self.register_provider(ModelSource.OLLAMA_REMOTE, ollama_remote)

        # Register Hugging Face provider
        huggingface = HuggingFaceModelProvider()
        self.register_provider(ModelSource.HUGGINGFACE, huggingface)

    def register_provider(self, source: ModelSource, provider: ModelProvider) -> None:
        """Register a model provider for a specific source.

        Args:
            source: The model source
            provider: The provider implementation
        """
        self.providers[source] = provider

    def register_installer(
        self, source: ModelSource, installer: ModelInstaller
    ) -> None:
        """Register a model installer for a specific source.

        Args:
            source: The model source
            installer: The installer implementation
        """
        self.installers[source] = installer

    def search_models(
        self, query: str = "", sources: Optional[List[ModelSource]] = None, **kwargs
    ) -> List[ModelInfo]:
        """Search for models across multiple sources.

        Args:
            query: Search query string
            sources: List of sources to search, or None for all sources
            **kwargs: Additional source-specific parameters

        Returns:
            List[ModelInfo]: Matching models across all sources
        """
        if sources is None:
            sources = list(self.providers.keys())

        # First, refresh the cache of installed models
        self.refresh_installed_models()

        # Search across all requested sources
        all_results = []
        for source in sources:
            if source not in self.providers:
                print(f"⚠️ Warning: No provider registered for source {source}")
                continue

            provider = self.providers[source]
            try:
                models = provider.list_models(query=query, **kwargs)

                # Mark models as installed if they're in our installed cache
                for model in models:
                    if model.name in self.installed_models:
                        model.installed = True

                all_results.extend(models)
            except Exception as e:
                print(f"⚠️ Error searching in {source}: {e}")

        # Sort results by relevance to query
        if query:
            scored_results = self._score_search_results(query, all_results)
            all_results = [model for _, model in scored_results]

        return all_results

    def _score_search_results(
        self, query: str, models: List[ModelInfo]
    ) -> SearchResults:
        """Score and sort models based on relevance to query.

        Args:
            query: Search query
            models: List of models to score

        Returns:
            SearchResults: List of (score, model) tuples sorted by score
        """
        query_terms = query.lower().split()
        scored_results: SearchResults = []

        for model in models:
            score = 0
            name_lower = model.name.lower()
            desc_lower = model.description.lower()
            tags_lower = [tag.lower() for tag in model.tags]

            # Score each query term
            for term in query_terms:
                # Exact name match is highest priority
                if term in name_lower:
                    score += 10
                    if name_lower.startswith(term):
                        score += 5  # Bonus for prefix match

                # Tag matches are second priority
                if any(term in tag for tag in tags_lower):
                    score += 8

                # Description matches are lower priority
                if term in desc_lower:
                    score += 5

            # Boost installed models
            if model.installed:
                score += 3

            # Only include models with a positive score
            if score > 0:
                scored_results.append((score, model))

        # Sort by score, highest first
        scored_results.sort(reverse=True, key=lambda x: x[0])
        return scored_results

    def get_model_details(self, name: str, source: ModelSource) -> Optional[ModelInfo]:
        """Get detailed information about a specific model.

        Args:
            name: Model name
            source: Source to search in

        Returns:
            Optional[ModelInfo]: Model details or None if not found
        """
        if source not in self.providers:
            print(f"⚠️ Warning: No provider registered for source {source}")
            return None

        provider = self.providers[source]
        model = provider.get_model(name)

        # Check if the model is installed
        if model and name in self.installed_models:
            model.installed = True

        return model

    def install_model(self, model: ModelInfo) -> bool:
        """Install a model from its source.

        Args:
            model: Model to install

        Returns:
            bool: True if installation was successful
        """
        if model.source not in self.installers:
            print(f"⚠️ Error: No installer available for source {model.source}")
            return False

        installer = self.installers[model.source]
        success = installer.install_model(model)

        if success:
            # Update our cache of installed models
            self.refresh_installed_models()
            print(f"✅ Successfully installed {model.name}")
        else:
            print(f"❌ Failed to install {model.name}")

        return success

    def uninstall_model(self, model_name: str) -> bool:
        """Uninstall a model.

        Args:
            model_name: Name of the model to uninstall

        Returns:
            bool: True if uninstallation was successful
        """
        # Find the model in our installed cache
        if model_name not in self.installed_models:
            print(f"⚠️ Model {model_name} is not installed")
            return False

        model = self.installed_models[model_name]

        if model.source not in self.installers:
            print(f"⚠️ Error: No installer available for source {model.source}")
            return False

        installer = self.installers[model.source]
        success = installer.uninstall_model(model_name)

        if success:
            # Update our cache of installed models
            self.refresh_installed_models()
            print(f"✅ Successfully uninstalled {model_name}")
        else:
            print(f"❌ Failed to uninstall {model_name}")

        return success

    def list_installed_models(self) -> List[ModelInfo]:
        """List all installed models.

        Returns:
            List[ModelInfo]: List of installed models
        """
        self.refresh_installed_models()
        return list(self.installed_models.values())

    def refresh_installed_models(self) -> None:
        """Refresh the cache of installed models."""
        self.installed_models.clear()

        # Get installed models from each provider with an installer
        for source, provider in self.providers.items():
            if source not in self.installers:
                continue

            try:
                # We specifically want local/installed models here
                models = provider.list_models(installed_only=True)
                for model in models:
                    model.installed = True
                    self.installed_models[model.name] = model
            except Exception as e:
                print(f"⚠️ Error refreshing installed models from {source}: {e}")

    async def update_model_indices(self) -> None:
        """Update all remote model indices asynchronously."""
        tasks = []

        # Collect update tasks from providers that support it
        for source, provider in self.providers.items():
            if hasattr(provider, "update_index"):
                task = asyncio.create_task(provider.update_index())
                tasks.append(task)

        # Wait for all updates to complete
        if tasks:
            await asyncio.gather(*tasks)
            print("✅ All model indices updated successfully")

    def save_state(self) -> None:
        """Save current state to disk."""
        try:
            state = {
                "installed_models": [
                    asdict(model) for model in self.installed_models.values()
                ]
            }

            with open(self.config["index_path"], "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving state: {e}")

    def load_state(self) -> None:
        """Load state from disk."""
        if not os.path.exists(self.config["index_path"]):
            return

        try:
            with open(self.config["index_path"], "r") as f:
                state = json.load(f)

            # Process installed models
            if "installed_models" in state:
                self.installed_models = {}
                for model_dict in state["installed_models"]:
                    model = ModelInfo(**model_dict)
                    model.installed = True
                    self.installed_models[model.name] = model
        except Exception as e:
            print(f"⚠️ Error loading state: {e}")


# CLI interface for the model manager
def create_cli() -> None:
    """Create a CLI interface for the model manager."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Eidosian Model Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for models")
    search_parser.add_argument("query", nargs="?", default="", help="Search query")
    search_parser.add_argument(
        "--source",
        choices=["all", "ollama-local", "ollama-remote", "huggingface"],
        default="all",
        help="Source to search in",
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List installed models")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install a model")
    install_parser.add_argument("name", help="Model name to install")
    install_parser.add_argument(
        "--source",
        choices=["ollama-local", "ollama-remote", "huggingface"],
        required=True,
        help="Source to install from",
    )

    # Uninstall command
    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall a model")
    uninstall_parser.add_argument("name", help="Model name to uninstall")

    # Update index command
    update_parser = subparsers.add_parser("update-index", help="Update model indices")

    # Parse arguments
    args = parser.parse_args()

    # Create model manager
    manager = ModelManager()

    # Execute command
    if args.command == "search":
        # Map source string to ModelSource enum
        sources = []
        if args.source == "all":
            sources = list(ModelSource)
        elif args.source == "ollama-local":
            sources = [ModelSource.OLLAMA_LOCAL]
        elif args.source == "ollama-remote":
            sources = [ModelSource.OLLAMA_REMOTE]
        elif args.source == "huggingface":
            sources = [ModelSource.HUGGINGFACE]

        models = manager.search_models(args.query, sources)
        if not models:
            print("No models found.")
            return

        print(f"Found {len(models)} models:")
        for model in models:
            installed_mark = "📦 " if model.installed else "   "
            print(f"{installed_mark}{model.name} ({model.source.name})")
            print(f"   {model.description[:80]}...")
            if model.size:
                print(f"   Size: {model.size}")
            if model.parameters:
                print(f"   Parameters: {model.parameters}")
            print()

    elif args.command == "list":
        models = manager.list_installed_models()
        if not models:
            print("No models installed.")
            return

        print(f"Installed models ({len(models)}):")
        for model in models:
            print(f"📦 {model.name} ({model.source.name})")
            print(f"   {model.description[:80]}...")
            if model.size:
                print(f"   Size: {model.size}")
            print()

    elif args.command == "install":
        # Map source string to ModelSource enum
        source = None
        if args.source == "ollama-local":
            source = ModelSource.OLLAMA_LOCAL
        elif args.source == "ollama-remote":
            source = ModelSource.OLLAMA_REMOTE
        elif args.source == "huggingface":
            source = ModelSource.HUGGINGFACE

        if not source:
            print(f"Invalid source: {args.source}")
            return

        # Get model details
        model = manager.get_model_details(args.name, source)
        if not model:
            print(f"Model {args.name} not found in {args.source}")
            return

        # Install model
        success = manager.install_model(model)
        if not success:
            sys.exit(1)

    elif args.command == "uninstall":
        success = manager.uninstall_model(args.name)
        if not success:
            sys.exit(1)

    elif args.command == "update-index":
        try:
            # Run the update in an event loop
            asyncio.run(manager.update_model_indices())
        except Exception as e:
            print(f"Error updating indices: {e}")
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    create_cli()

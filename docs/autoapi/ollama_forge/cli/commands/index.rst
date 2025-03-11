:orphan:

ollama_forge.cli.commands
=========================

.. py:module:: ollama_forge.cli.commands

.. autoapi-nested-parse::

    CLI command implementations for Ollama Forge. ⚙️🔮⚡
   ╔═══════════════════════════════════════════════════════════╗
   ║ Eidosian Minimalism, Humor, Flow, and Self-Awareness      ║
   ╚═══════════════════════════════════════════════════════════╝
       All functionality remains intact, refined with clarity and style.



Functions

---------

.. autoapisummary::

    ollama_forge.cli.commands.create_parser
   ollama_forge.cli.commands.handle_generate
   ollama_forge.cli.commands.handle_chat
   ollama_forge.cli.commands.handle_chat_session
   ollama_forge.cli.commands.handle_embed
   ollama_forge.cli.commands.handle_list
   ollama_forge.cli.commands.handle_pull
   ollama_forge.cli.commands.generate_command
   ollama_forge.cli.commands.chat_command
   ollama_forge.cli.commands.embedding_command
   ollama_forge.cli.commands.models_command
   ollama_forge.cli.commands.health_command
   ollama_forge.cli.commands.main


Module Contents

---------------

.. py:function:: create_parser() -> argparse.ArgumentParser

    Create an elegant command parser with layered subcommand structure. 🏛️


.. py:function:: handle_generate(args: argparse.Namespace, client: ollama_forge.client.OllamaClient) -> int


    Eidosian text generation with streaming option.


.. py:function:: handle_chat(args: argparse.Namespace, client: ollama_forge.client.OllamaClient) -> int


    Eidosian chat command.


.. py:function:: handle_chat_session(args: argparse.Namespace, client: ollama_forge.client.OllamaClient) -> int


    Fluid, interactive chat session with color-coded prompts.
   Escape with 'exit' or 'quit'. 🎨🔮


.. py:function:: handle_embed(args: argparse.Namespace, client: ollama_forge.client.OllamaClient) -> int


    Eidosian embedding generation.


.. py:function:: handle_list(args: argparse.Namespace, client: ollama_forge.client.OllamaClient) -> int


    List available models with impeccable formatting.


.. py:function:: handle_pull(args: argparse.Namespace, client: ollama_forge.client.OllamaClient) -> int


    Pull a model with progress tracking.


.. py:function:: generate_command(args: argparse.Namespace) -> int


    Command function for text generation via the generate subcommand.
   Follows Eidosian principle of elegant delegation.
       :param args: Parsed command arguments

   :returns: Exit code (0 for success)


.. py:function:: chat_command(args: argparse.Namespace) -> int


    Command function for interactive chat via the chat subcommand.
   Follows Eidosian principle of elegant delegation.
       :param args: Parsed command arguments

   :returns: Exit code (0 for success)


.. py:function:: embedding_command(args: argparse.Namespace) -> int


    Command function for embedding generation via the embed subcommand.
   Follows Eidosian principle of elegant delegation.
       :param args: Parsed command arguments

   :returns: Exit code (0 for success)


.. py:function:: models_command(args: argparse.Namespace) -> int


    Command function for model management via the models subcommand.
   Follows Eidosian principle of elegant delegation.
       :param args: Parsed command arguments

   :returns: Exit code (0 for success)


.. py:function:: health_command(args: argparse.Namespace) -> int


    Command function for health check via the health subcommand.
   Follows Eidosian principle of elegant simplicity.
       :param args: Parsed command arguments

   :returns: Exit code (0 for success)


.. py:function:: main() -> int


    Main method guiding CLI invocation. 🏁🚀



:orphan:

ollama_forge.__main__
=====================

.. py:module:: ollama_forge.__main__

.. autoapi-nested-parse::

    Ollama Forge Module Execution Point

   This module serves as the direct execution entry point when the package is run with:
   `python -m ollama_forge`
       Following Eidosian principles of:
   - Contextual Integrity: Every component has a precise purpose
   - Flow Like a River: Seamless execution path
   - Structure as Control: Clear organization and responsibility delegation



Functions

---------

.. autoapisummary::

    ollama_forge.__main__.parse_args
   ollama_forge.__main__.command_router
   ollama_forge.__main__.main
   ollama_forge.__main__.module_entry


Module Contents

---------------

.. py:function:: parse_args(args: Optional[List[str]] = None) -> argparse.Namespace

    Parse command arguments with Eidosian precision and clarity.
   Each argument serves a purpose; no waste, no dilution.
       :param args: Command line arguments (uses sys.argv if None)

   :returns: Parsed arguments with perfect structure


.. py:function:: command_router() -> Dict[str, Callable]


    Maps commands to their handler functions.
   Follows the 'Structure as Control' principle with a single source of routing.
       :returns: Dictionary mapping command names to handler functions


.. py:function:: main() -> int


    Initiates command flow with Eidosian elegance.
   Each operation precisely executed, each error handled with wit.
       :returns: Exit code (0 for success, non-zero for errors)


.. py:function:: module_entry(args: Optional[List[str]] = None) -> int


    Pure entry point function for programmatic control.

   :param args: Command line arguments (uses sys.argv if None)

       :returns: Exit code (0 for success)


``
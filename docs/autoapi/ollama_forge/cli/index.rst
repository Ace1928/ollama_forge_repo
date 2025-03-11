:orphan:

ollama_forge.cli
================

.. py:module:: ollama_forge.cli

.. autoapi-nested-parse::

    Command Line Interface for Ollama Forge. 🎯🌟
   Eidosian synergy: minimal redundancy, immediate utility.



Submodules

----------

.. toctree::
   :maxdepth: 1
       /autoapi/ollama_forge/cli/commands/index


Classes

-------

.. autoapisummary::

    ollama_forge.cli.OllamaClient


Functions

---------

.. autoapisummary::

    ollama_forge.cli.create_parser
   ollama_forge.cli.handle_generate
   ollama_forge.cli.handle_chat
   ollama_forge.cli.handle_chat_session
   ollama_forge.cli.handle_embed
   ollama_forge.cli.handle_list
   ollama_forge.cli.handle_pull
   ollama_forge.cli.main


Package Contents

----------------

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


.. py:class:: OllamaClient(base_url: str = DEFAULT_OLLAMA_API_URL, timeout: int = DEFAULT_TIMEOUT, max_retries: int = 3, session: Optional[requests.Session] = None)


    Client for interacting with the Ollama API.

   This class provides a comprehensive interface to all Ollama API endpoints,
   with support for both synchronous and asynchronous requests, streaming responses,
   and robust error handling.
       .. attribute:: base_url

      Base URL for the Ollama API

          .. attribute:: timeout

      Request timeout in seconds

          .. attribute:: max_retries

      Maximum number of retries for failed requests

          Initialize the Ollama client.

   :param base_url: Base URL for the Ollama API
   :param timeout: Request timeout in seconds
   :param max_retries: Maximum number of retries for failed requests
   :param session: Optional requests.Session to use
       .. py:attribute:: base_url
      :value: ''
          .. py:attribute:: timeout


   .. py:attribute:: max_retries


       :value: 3



   .. py:attribute:: session



       .. py:attribute:: _thread_local


   .. py:method:: _with_retry(method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, stream: bool = False, headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]


       Make an HTTP request with retry logic.

      :param method: HTTP method (GET, POST, etc.)

          :param endpoint: API endpoint to call
      :param data: Request data
          :param stream: Whether to stream the response
      :param headers: Optional request headers
          :returns: Response object

      :raises ollama_forge.exceptions.ConnectionError: If connection fails after all retries

          :raises ollama_forge.exceptions.ModelNotFoundError: If the model is not found
      :raises ollama_forge.exceptions.ServerError: If the server returns a 5xx error
          :raises ollama_forge.exceptions.InvalidRequestError: If the request is invalid
      :raises ollama_forge.exceptions.TimeoutError: If the request times out
          :raises ollama_forge.exceptions.OllamaAPIError: For other API errors



   .. py:method:: _with_async_retry(method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, stream: bool = False, headers: Optional[Dict[str, str]] = None) -> Optional[httpx.Response]



       :async:



   .. py:method:: get_version() -> Dict[str, Any]



       Get the Ollama server version.

      :returns: Dictionary with version information

          :raises ollama_forge.exceptions.ConnectionError: If cannot connect to Ollama server
      :raises ollama_forge.exceptions.OllamaAPIError: If the response is invalid
          .. py:method:: list_models() -> Dict[str, List[Dict[str, Any]]]

      List available models.

          :returns: Dictionary with models information

      :raises ollama_forge.exceptions.ConnectionError: If cannot connect to Ollama server

          :raises ollama_forge.exceptions.OllamaAPIError: If the response is invalid



   .. py:method:: pull_model(model: str, stream: bool = True) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]



       Pull a model from the Ollama registry.

      :param model: Name of the model to pull

          :param stream: Whether to stream the progress

      :returns: If stream=True, a generator yielding progress updates

          If stream=False, a dictionary with pull result

      :raises ollama_forge.exceptions.ConnectionError: If cannot connect to Ollama server

          :raises ollama_forge.exceptions.InvalidRequestError: If the model name is invalid
      :raises ollama_forge.exceptions.OllamaAPIError: If the response is invalid
          .. py:method:: generate(model: str, prompt: str, options: Optional[Dict[str, Any]] = None, stream: bool = False) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]

      Generate text from a prompt.

          :param model: Name of the model to use
      :param prompt: The prompt to generate from
          :param options: Dictionary of generation options
      :param stream: Whether to stream the response
          :returns: If stream=True, a generator yielding response chunks
                If stream=False, a dictionary with the complete response
                    :raises ollama_forge.exceptions.ConnectionError: If cannot connect to Ollama server
      :raises ollama_forge.exceptions.ModelNotFoundError: If the model does not exist
          :raises ollama_forge.exceptions.InvalidRequestError: If the request is invalid



   .. py:method:: chat(model: str, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None, stream: bool = False) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]



       Chat with a model.

      :param model: Name of the model

          :param messages: List of message dictionaries (role, content)
      :param options: Chat options
          :param stream: Whether to stream the response

      :returns: If stream=True, a generator yielding response chunks

          If stream=False, a dictionary with the complete response

      :raises ollama_forge.exceptions.ConnectionError: If cannot connect to Ollama server

          :raises ollama_forge.exceptions.ModelNotFoundError: If the model does not exist
      :raises ollama_forge.exceptions.InvalidRequestError: If the messages format is invalid
          .. py:method:: create_embedding(model: str, prompt: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]

      Create an embedding vector for a text prompt.

          :param model: Name of the model
      :param prompt: Text to create embedding for
          :param options: Optional embedding parameters

      :returns: Dictionary with the embedding vector

          :raises ollama_forge.exceptions.ConnectionError: If cannot connect to Ollama server
      :raises ollama_forge.exceptions.ModelNotFoundError: If the model does not exist
          .. py:method:: batch_embeddings(model: str, prompts: List[str], options: Optional[Dict[str, Any]] = None, show_progress: bool = False) -> List[Dict[str, Any]]

      Create embeddings for multiple prompts.

          :param model: Name of the model
      :param prompts: List of texts to create embeddings for
          :param options: Optional embedding parameters
      :param show_progress: Whether to show a progress bar
          :returns: List of embedding vectors

      :raises ollama_forge.exceptions.ConnectionError: If cannot connect to Ollama server

          :raises ollama_forge.exceptions.ModelNotFoundError: If the model does not exist



   .. py:method:: delete_model(model: str) -> bool



       Delete a model.

      :param model: Name of the model to delete

          :returns: True if successful

      :raises ollama_forge.exceptions.ConnectionError: If cannot connect to Ollama server

          :raises ollama_forge.exceptions.ModelNotFoundError: If the model does not exist



   .. py:method:: copy_model(source: str, destination: str) -> Dict[str, Any]



       Copy a model.

      :param source: Source model name

          :param destination: Destination model name

      :returns: Dictionary with operation result

          :raises ollama_forge.exceptions.ConnectionError: If cannot connect to Ollama server
      :raises ollama_forge.exceptions.ModelNotFoundError: If the source model does not exist
          :raises ollama_forge.exceptions.InvalidRequestError: If the destination name is invalid



   .. py:method:: create_model(name: str, modelfile: str, stream: bool = True) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]



       Create a new model from a Modelfile.

      :param name: Name for the new model

          :param modelfile: Modelfile content
      :param stream: Whether to stream the creation progress
          :returns: If stream=True, a generator yielding progress updates
                If stream=False, a dictionary with creation result
                    :raises ollama_forge.exceptions.ConnectionError: If cannot connect to Ollama server
      :raises ollama_forge.exceptions.InvalidRequestError: If the Modelfile is invalid
          .. py:method:: fallback_context(operation: str)

      Context manager for automatic model fallback.

          :param operation: Operation type ("chat", "generate", "embedding")

      :Yields: None

          Example:

      .. code-block:: python

          with client.fallback_context("chat"):response = client.chat(model, messages)
      



   .. py:method:: get_fallback_info() -> Dict[str, Any]
      



       Get information about the current fallback state.

      :returns: Dictionary containing fallback depth, model name, and original error

          .. py:method:: agenerate(model: str, prompt: str, options: Optional[Dict[str, Any]] = None, stream: bool = False) -> Union[Dict[str, Any], AsyncIterator[Dict[str, Any]]]
      :async:
          .. py:method:: achat(model: str, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None, stream: bool = False) -> Union[Dict[str, Any], AsyncIterator[Dict[str, Any]]]
      :async:
          .. py:method:: acreate_embedding(model: str, prompt: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]
      :async:
          .. py:function:: main(args: Optional[List[str]] = None) -> int

   Main entry point for the CLI with perfect flow control.

       :param args: Command line arguments (uses sys.argv if None)

   :returns: Exit code (0 for success)



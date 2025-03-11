:orphan:

ollama_forge.exceptions
=======================

.. py:module:: ollama_forge.exceptions

.. autoapi-nested-parse::

    Exception classes for Ollama Forge.

   This module defines a precise, hierarchical exception system to provide
   detailed and actionable error information with perfect granularity.
   Following Eidosian principles of structure as control, contextual integrity,
   and precision as style.



Attributes

----------

.. autoapisummary::

    ollama_forge.exceptions.ERROR_CODE_MAP


Exceptions

----------

.. autoapisummary::

    ollama_forge.exceptions.OllamaAPIError
   ollama_forge.exceptions.ConnectionError
   ollama_forge.exceptions.TimeoutError
   ollama_forge.exceptions.ModelNotFoundError
   ollama_forge.exceptions.ServerError
   ollama_forge.exceptions.InvalidRequestError
   ollama_forge.exceptions.StreamingError
   ollama_forge.exceptions.ParseError
   ollama_forge.exceptions.ValidationError
   ollama_forge.exceptions.OllamaConnectionError
   ollama_forge.exceptions.OllamaModelNotFoundError
   ollama_forge.exceptions.OllamaServerError


Functions

---------

.. autoapisummary::

    ollama_forge.exceptions.get_exception_for_status


Module Contents

---------------

.. py:exception:: ollama_forge.exceptions.OllamaAPIError(message: str, response: Optional[Dict[str, Any]] = None)

    Bases: :py:obj:`Exception`


   Base exception for all Ollama API errors.


       Initialize self.  See help(type(self)) for accurate signature.


   .. py:attribute:: message


       .. py:attribute:: response
      :value: None
          .. py:method:: __str__() -> str

      Return str(self).



.. py:exception:: ollama_forge.exceptions.ConnectionError(message: str, response: Optional[Dict[str, Any]] = None)

``
   Bases: :py:obj:`OllamaAPIError`
       Raised when a connection to the Ollama server cannot be established.

   Initialize self.  See help(type(self)) for accurate signature.


.. py:exception:: ollama_forge.exceptions.TimeoutError(message: str, response: Optional[Dict[str, Any]] = None)

``
   Bases: :py:obj:`OllamaAPIError`
       Raised when a request to the Ollama server times out.

   Initialize self.  See help(type(self)) for accurate signature.


.. py:exception:: ollama_forge.exceptions.ModelNotFoundError(message: str, response: Optional[Dict[str, Any]] = None)

``
   Bases: :py:obj:`OllamaAPIError`
       Raised when the requested model does not exist.

   Initialize self.  See help(type(self)) for accurate signature.


.. py:exception:: ollama_forge.exceptions.ServerError(message: str, response: Optional[Dict[str, Any]] = None)

``
   Bases: :py:obj:`OllamaAPIError`
       Raised when the Ollama server returns a 5xx error.

   Initialize self.  See help(type(self)) for accurate signature.


.. py:exception:: ollama_forge.exceptions.InvalidRequestError(message: str, response: Optional[Dict[str, Any]] = None)

``
   Bases: :py:obj:`OllamaAPIError`
       Raised when the request is invalid (4xx error).

   Initialize self.  See help(type(self)) for accurate signature.


.. py:exception:: ollama_forge.exceptions.StreamingError(message: str, response: Optional[Dict[str, Any]] = None)

``
   Bases: :py:obj:`OllamaAPIError`
       Raised when an error occurs during streaming responses.

   Initialize self.  See help(type(self)) for accurate signature.


.. py:exception:: ollama_forge.exceptions.ParseError(message: str, response: Optional[Dict[str, Any]] = None)

``
   Bases: :py:obj:`OllamaAPIError`
       Raised when parsing a response fails.

   Initialize self.  See help(type(self)) for accurate signature.


.. py:exception:: ollama_forge.exceptions.ValidationError(message: str, response: Optional[Dict[str, Any]] = None)

``
   Bases: :py:obj:`OllamaAPIError`
       Raised when input validation fails.

   Initialize self.  See help(type(self)) for accurate signature.


.. py:exception:: ollama_forge.exceptions.OllamaConnectionError(message: str, response: Optional[Dict[str, Any]] = None)

``
   Bases: :py:obj:`ConnectionError`
       Legacy alias for ollama_forge.exceptions.ConnectionError for backwards compatibility.

   Initialize self.  See help(type(self)) for accurate signature.


.. py:exception:: ollama_forge.exceptions.OllamaModelNotFoundError(message: str, response: Optional[Dict[str, Any]] = None)

``
   Bases: :py:obj:`ModelNotFoundError`
       Legacy alias for ollama_forge.exceptions.ModelNotFoundError for backwards compatibility.

   Initialize self.  See help(type(self)) for accurate signature.


.. py:exception:: ollama_forge.exceptions.OllamaServerError(message: str, response: Optional[Dict[str, Any]] = None)

``
   Bases: :py:obj:`ServerError`
       Legacy alias for ollama_forge.exceptions.ServerError for backwards compatibility.

   Initialize self.  See help(type(self)) for accurate signature.


.. py:data:: ERROR_CODE_MAP
   :type:  dict[int, type[ollama_forge.exceptions.InvalidRequestError] | type[ollama_forge.exceptions.ModelNotFoundError] | type[ollama_forge.exceptions.TimeoutError] | type[ollama_forge.exceptions.ServerError]]

.. py:function:: get_exception_for_status(status_code: int, message: str, response: Optional[Dict[str, Any]] = None) -> ollama_forge.exceptions.OllamaAPIError

    Get the appropriate exception class for an HTTP status code.

   :param status_code: HTTP status code
   :param message: Error message
   :param response: Optional response data
       :returns: Instantiated exception of the appropriate type


``
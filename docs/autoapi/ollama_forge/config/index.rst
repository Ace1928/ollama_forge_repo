:orphan:

ollama_forge.config
===================

.. py:module:: ollama_forge.config

.. autoapi-nested-parse::

    Configuration module for Ollama Forge.

   This module serves as the central source of truth for all configuration
   parameters and versioning information used throughout the package.
   It embodies the Eidosian principles of Structure as Control and Contextual Integrity.
       Every constant, function, and docstring here stands on its own yet interlocks
   seamlessly with the larger system—a fractal reflection of purpose and clarity.



Attributes

----------

.. autoapisummary::

    ollama_forge.config.T
   ollama_forge.config.F
   ollama_forge.config.SYSTEM
   ollama_forge.config.IS_WINDOWS
   ollama_forge.config.IS_MACOS
   ollama_forge.config.IS_LINUX
   ollama_forge.config.IS_ARM64
   ollama_forge.config.IS_X86_64
   ollama_forge.config.CPU_COUNT
   ollama_forge.config.MEMORY_MB
   ollama_forge.config.IS_CONTAINER
   ollama_forge.config.IS_CI_ENV
   ollama_forge.config.PACKAGE_NAME
   ollama_forge.config.PACKAGE_NAME_NORMALIZED
   ollama_forge.config.VERSION_MAJOR
   ollama_forge.config.VERSION_MINOR
   ollama_forge.config.VERSION_PATCH
   ollama_forge.config.VERSION
   ollama_forge.config.VERSION_RELEASE_DATE
   ollama_forge.config.BUILD_TIMESTAMP
   ollama_forge.config.PACKAGE_BIRTHDAY
   ollama_forge.config.DEFAULT_OLLAMA_API_URL
   ollama_forge.config.DEFAULT_TIMEOUT
   ollama_forge.config.DEFAULT_MAX_RETRIES
   ollama_forge.config.DEFAULT_CHAT_MODEL
   ollama_forge.config.BACKUP_CHAT_MODEL
   ollama_forge.config.DEFAULT_EMBEDDING_MODEL
   ollama_forge.config.BACKUP_EMBEDDING_MODEL
   ollama_forge.config.DEFAULT_MIN_CONTEXT
   ollama_forge.config.RECOMMENDED_CONTEXT
   ollama_forge.config.AUTHORS
   ollama_forge.config.DEBUG_MODE
   ollama_forge.config.VERBOSE_MODE
   ollama_forge.config.LOG_LEVEL
   ollama_forge.config.DISABLE_PROGRESS_BARS
   ollama_forge.config.user_dirs
   ollama_forge.config.USER_CONFIG_DIR
   ollama_forge.config.USER_CACHE_DIR
   ollama_forge.config.USER_DATA_DIR
   ollama_forge.config.API_ENDPOINTS
   ollama_forge.config.runtime_config


Functions

---------

.. autoapisummary::

    ollama_forge.config.safe_sysconf
   ollama_forge.config.calculate_timeout
   ollama_forge.config.calculate_context_size
   ollama_forge.config.configure_log_level
   ollama_forge.config.configure_progress_bars
   ollama_forge.config.configure_user_directories
   ollama_forge.config.validate_input
   ollama_forge.config.safe_dict_get
   ollama_forge.config.get_version_string
   ollama_forge.config.get_version_tuple
   ollama_forge.config.get_release_date
   ollama_forge.config.get_build_age
   ollama_forge.config.get_package_age
   ollama_forge.config.get_author_string
   ollama_forge.config.get_email_string
   ollama_forge.config.is_string
   ollama_forge.config.get_default_api_endpoint
   ollama_forge.config.is_debug_mode
   ollama_forge.config.get_system_info
   ollama_forge.config.get_optimal_batch_size
   ollama_forge.config.update_runtime_config
   ollama_forge.config.get_runtime_config
   ollama_forge.config.reset_runtime_config
   ollama_forge.config.get_config_summary


Module Contents

---------------

.. py:data:: T

.. py:data:: F

.. py:data:: SYSTEM

.. py:data:: IS_WINDOWS

.. py:data:: IS_MACOS

.. py:data:: IS_LINUX

.. py:data:: IS_ARM64

.. py:data:: IS_X86_64

.. py:data:: CPU_COUNT

.. py:function:: safe_sysconf(name: Union[int, str], default: int = 4096) -> int

    Safely get system configuration values with proper fallback. 🔒
   Accepts both string constants and integer values for maximum flexibility.


.. py:data:: MEMORY_MB
   :value: 16


.. py:data:: IS_CONTAINER
   :value: False


.. py:data:: IS_CI_ENV

.. py:data:: PACKAGE_NAME
   :value: 'Ollama Forge'


.. py:data:: PACKAGE_NAME_NORMALIZED
   :value: 'ollama_forge'


.. py:data:: VERSION_MAJOR
   :value: 0


.. py:data:: VERSION_MINOR
   :value: 1


.. py:data:: VERSION_PATCH
   :value: 9


.. py:data:: VERSION
   :value: '0.1.9'


.. py:data:: VERSION_RELEASE_DATE
   :value: '2025-01-15'


.. py:data:: BUILD_TIMESTAMP

.. py:data:: PACKAGE_BIRTHDAY
   :value: 1704067200


.. py:data:: DEFAULT_OLLAMA_API_URL
   :value: 'http://localhost:11434'


.. py:function:: calculate_timeout() -> int


    Calculate optimal timeout based on system specs - adaptive intelligence! ⚡


.. py:data:: DEFAULT_TIMEOUT

.. py:data:: DEFAULT_MAX_RETRIES
   :value: 3


.. py:data:: DEFAULT_CHAT_MODEL
   :value: 'deepseek-r1:1.5b'


.. py:data:: BACKUP_CHAT_MODEL
   :value: 'qwen2.5:0.5b-Instruct'


.. py:data:: DEFAULT_EMBEDDING_MODEL
   :value: 'deepseek-r1:1.5b'


.. py:data:: BACKUP_EMBEDDING_MODEL
   :value: 'qwen2.5:0.5b-Instruct'


.. py:data:: DEFAULT_MIN_CONTEXT
   :value: 2048


.. py:function:: calculate_context_size() -> int


    Calculate optimal context size - more RAM = bigger thoughts! 🧠


.. py:data:: RECOMMENDED_CONTEXT

.. py:data:: AUTHORS

.. py:data:: DEBUG_MODE

.. py:data:: VERBOSE_MODE

.. py:function:: configure_log_level() -> str

    Configure optimal log level based on environment. 📊


.. py:data:: LOG_LEVEL

.. py:function:: configure_progress_bars() -> bool

    Configure progress bars for optimal user experience. 📊


.. py:data:: DISABLE_PROGRESS_BARS

.. py:function:: configure_user_directories() -> Dict[str, str]

    Configure user directories based on platform. 🗂️


.. py:data:: user_dirs

.. py:data:: USER_CONFIG_DIR

.. py:data:: USER_CACHE_DIR

.. py:data:: USER_DATA_DIR

.. py:data:: API_ENDPOINTS

.. py:function:: validate_input(validator: Callable[Ellipsis, bool], error_msg: Optional[str] = None) -> Callable[[F], F]

    Decorator for input validation with humor-infused error messages.

   :param validator: Function returning bool indicating if input is valid
   :param error_msg: Optional custom error message
       :returns: Decorated function with validation


.. py:function:: safe_dict_get(d: Dict[str, T], key: str, default: Optional[T] = None) -> Optional[T]


    Safely retrieve a value from a dict - no KeyErrors here! 🛡️

   :param d: Dictionary to retrieve from
   :param key: Key to look up
   :param default: Value to return if key is missing
       :returns: Value from dict or default


.. py:function:: get_version_string() -> str


    Return the full version string with optimal caching. ✨


.. py:function:: get_version_tuple() -> Tuple[int, int, int]


    Return version as a tuple of (major, minor, patch). 📊


.. py:function:: get_release_date() -> str


    Return the release date of the current version. 📅


.. py:function:: get_build_age() -> int


    Return the age of the build in seconds - how old is your code? 👴


.. py:function:: get_package_age() -> int


    Return the age of the package in days since inception. 🎂


.. py:function:: get_author_string() -> str


    Return a formatted author string with optimal caching. 👥


.. py:function:: get_email_string() -> str


    Return a formatted email string with optimal caching. 📧


.. py:function:: is_string(op: Any) -> bool


    Check if value is a string. Simple yet essential! 📝


.. py:function:: get_default_api_endpoint(operation: str) -> str


    Get the API endpoint for a specific operation.

   :param operation: API operation name (e.g., 'chat', 'generate')

       :returns: Endpoint URL path or empty string if not found


.. py:function:: is_debug_mode() -> bool


    Check if debug mode is enabled - are we wearing our X-ray specs? 🕶️


.. py:function:: get_system_info() -> Dict[str, Any]


    Return detailed system information for optimal configuration.
   Like a digital doctor's checkup for your environment! 🩺


.. py:function:: get_optimal_batch_size() -> int


    Calculate optimal batch size based on system resources.
   Because one size definitely doesn't fit all! 📏


.. py:data:: runtime_config
   :type:  Dict[str, Any]

.. py:function:: update_runtime_config(key: str, value: Any) -> bool

    Update a runtime configuration value with change tracking.

   :param key: Configuration key to update
   :param value: New value to set
       :returns: True if update successful, False if key unknown


.. py:function:: get_runtime_config(key: str, default: Any = None) -> Any


    Get a runtime configuration value with intelligent defaults.

   :param key: Configuration key to retrieve
   :param default: Fallback value if key doesn't exist
       :returns: The configuration value or default


.. py:function:: reset_runtime_config() -> None


    Reset runtime configuration to optimal defaults.
   Like hitting the cosmic reset button! 🔄


.. py:function:: get_config_summary() -> Dict[str, Any]


    Generate a summary of current configuration state.
   The TL;DR of your setup! 📋



# File: crewplus/services/tracing_manager.py

from typing import Any, Optional, List, Protocol
import os
import logging

# Langfuse imports with graceful fallback. This allows the application to run
# even if the langfuse library is not installed.
try:
    from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    LangfuseCallbackHandler = None

class TracingContext(Protocol):
    """
    A protocol that defines a formal contract for a model to be "traceable."

    This protocol ensures that any class using the TracingManager provides the
    necessary attributes and methods for the manager to function correctly. By
    using a Protocol, we leverage Python's static analysis tools (like mypy)
    to enforce this contract, preventing runtime errors and making the system
    more robust and self-documenting.

    It allows the TracingManager to be completely decoupled from any specific
    model implementation, promoting clean, compositional design.

    A class that implements this protocol must provide:
    - A `logger` attribute for logging.
    - An `enable_tracing` attribute to control tracing.
    - A `get_model_identifier` method to describe itself for logging purposes.
    """
    logger: logging.Logger
    enable_tracing: Optional[bool]
    
    def get_model_identifier(self) -> str:
        """
        Return a string that uniquely identifies the model instance for logging.
        
        Example:
            "GeminiChatModel (model='gemini-1.5-flash')"
            
        Note:
            The '...' (Ellipsis) is the standard way in a Protocol to indicate
            that this method must be implemented by any class that conforms to
            this protocol, but has no implementation in the protocol itself.
        """
        ...

class TracingManager:
    """
    Manages the initialization and injection of tracing handlers for chat models.
    
    This class uses a composition-based approach, taking a context object that
    fulfills the TracingContext protocol. This design is highly extensible,
    allowing new tracing providers (e.g., Helicone, OpenTelemetry) to be added
    with minimal, isolated changes.
    """
    
    def __init__(self, context: TracingContext):
        """
        Args:
            context: An object (typically a chat model instance) that conforms
                     to the TracingContext protocol.
        """
        self.context = context
        self._handlers: List[Any] = []
        self._initialize_handlers()
    
    def _initialize_handlers(self):
        """
        Initializes all supported tracing handlers. This is the central point
        for adding new observability tools.
        """
        self._handlers = []
        self._initialize_langfuse()
        # To add a new handler (e.g., Helicone), you would add a call to
        # self._initialize_helicone() here.
    
    def _initialize_langfuse(self):
        """Initializes the Langfuse handler if it's available and enabled."""
        if not LANGFUSE_AVAILABLE:
            if self.context.enable_tracing is True:
                self.context.logger.warning("Langfuse is not installed; tracing will be disabled. Install with: pip install langfuse")
            return
        
        # Determine if Langfuse should be enabled via an explicit flag or
        # by detecting its environment variables.
        enable_langfuse = self.context.enable_tracing
        if enable_langfuse is None: # Auto-detect if not explicitly set
            langfuse_env_vars = ["LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"]
            enable_langfuse = any(os.getenv(var) for var in langfuse_env_vars)
        
        if enable_langfuse:
            try:
                handler = LangfuseCallbackHandler()
                self._handlers.append(handler)
                self.context.logger.info(f"Langfuse tracing enabled for {self.context.get_model_identifier()}")
            except Exception as e:
                self.context.logger.warning(f"Failed to initialize Langfuse: {e}")
    
    def add_callbacks_to_config(self, config: Optional[dict]) -> dict:
        """
        Adds all registered tracing handlers to the request configuration.
        
        This method is idempotent; it will not add a handler if one of the
        same type is already present in the configuration's callback list. It
        also respects a `tracing_disabled` flag in the metadata.
        
        Args:
            config: The request configuration dictionary from a LangChain call.
            
        Returns:
            The updated configuration dictionary with tracing callbacks added.
        """
        if config is None:
            config = {}
        
        # Respect a global disable flag for this specific call.
        if not self._handlers or config.get("metadata", {}).get("tracing_disabled"):
            return config
        
        # Use an empty list as a safe default if 'callbacks' is missing or None.
        callbacks = config.get("callbacks") or []
        new_callbacks = list(callbacks)
        
        for handler in self._handlers:
            if not any(isinstance(cb, type(handler)) for cb in new_callbacks):
                new_callbacks.append(handler)
        
        # Only create a new config dictionary if callbacks were actually added.
        if len(new_callbacks) > len(callbacks):
            return {**config, "callbacks": new_callbacks}
        
        return config

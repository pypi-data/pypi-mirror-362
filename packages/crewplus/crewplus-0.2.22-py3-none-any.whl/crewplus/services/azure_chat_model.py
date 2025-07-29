import os
import logging
from typing import Any, Optional

from langchain_openai.chat_models.azure import AzureChatOpenAI
from pydantic import Field

# Langfuse imports with graceful fallback
try:
    from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    LangfuseCallbackHandler = None

class TracedAzureChatOpenAI(AzureChatOpenAI):
    """
    Wrapper for AzureChatOpenAI that integrates with Langfuse for tracing.
    
    This class automatically handles Langfuse callback integration, making it easier
    to trace and debug your interactions with the Azure OpenAI service.

    **Langfuse Integration:**
    Langfuse tracing is automatically enabled when environment variables are set:
    - LANGFUSE_PUBLIC_KEY: Your Langfuse public key
    - LANGFUSE_SECRET_KEY: Your Langfuse secret key  
    - LANGFUSE_HOST: Langfuse host URL (optional, defaults to https://cloud.langfuse.com)
    
    You can also configure it explicitly or disable it. Session and user tracking 
    can be set per call via metadata in the `config` argument.

    Attributes:
        logger (Optional[logging.Logger]): An optional logger instance.
        enable_langfuse (Optional[bool]): Enable/disable Langfuse tracing (auto-detect if None).

    Example:
        .. code-block:: python

            # Set Langfuse environment variables (optional)
            import os
            os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
            os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."

            from crewplus.services.azure_chat_model import TracedAzureChatOpenAI
            from langchain_core.messages import HumanMessage

            # Initialize the model
            model = TracedAzureChatOpenAI(
                azure_deployment="your-deployment",
                api_version="2024-05-01-preview",
            )

            # --- Text-only usage (automatically traced if env vars set) ---
            response = model.invoke("Hello, how are you?")
            print("Text response:", response.content)

            # --- Langfuse tracing with session/user tracking ---
            response = model.invoke(
                "What is AI?",
                config={
                    "metadata": {
                        "langfuse_session_id": "chat-session-123",
                        "langfuse_user_id": "user-456"
                    }
                }
            )
            
            # --- Disable Langfuse for specific calls ---
            response = model.invoke(
                "Hello without tracing",
                config={"metadata": {"langfuse_disabled": True}}
            )

            # --- Asynchronous Streaming Usage ---
            import asyncio
            from langchain_core.messages import HumanMessage

            async def main():
                messages = [HumanMessage(content="Tell me a short story about a brave robot.")]
                print("\nAsync Streaming response:")
                async for chunk in model.astream(messages):
                    print(chunk.content, end="", flush=True)
                print()

            # In a real application, you would run this with:
            # asyncio.run(main())
    """
    logger: Optional[logging.Logger] = Field(default=None, description="Optional logger instance", exclude=True)
    enable_langfuse: Optional[bool] = Field(default=None, description="Enable Langfuse tracing (auto-detect if None)")
    
    langfuse_handler: Optional[LangfuseCallbackHandler] = Field(default=None, exclude=True)

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        
        # Initialize logger
        if self.logger is None:
            self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
            if not self.logger.handlers:
                self.logger.addHandler(logging.StreamHandler())
                self.logger.setLevel(logging.INFO)
        
        # Initialize Langfuse handler
        self._initialize_langfuse()

    def _initialize_langfuse(self):
        """Initialize Langfuse handler if enabled and available."""
        if not LANGFUSE_AVAILABLE:
            if self.enable_langfuse is True:
                self.logger.warning("Langfuse is not installed. Install with: pip install langfuse")
            return
        
        # Auto-detect if Langfuse should be enabled
        if self.enable_langfuse is None:
            langfuse_env_vars = ["LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"]
            self.enable_langfuse = any(os.getenv(var) for var in langfuse_env_vars)
        
        if not self.enable_langfuse:
            return
        
        try:
            self.langfuse_handler = LangfuseCallbackHandler()
            self.logger.info(f"Langfuse tracing enabled for TracedAzureChatOpenAI with deployment: {self.deployment_name}")
        except Exception as e:
            self.logger.warning(f"Failed to initialize Langfuse: {e}")
            self.langfuse_handler = None

    def invoke(self, input, config=None, **kwargs):
        """Override invoke to add Langfuse callback automatically."""
        if config is None:
            config = {}
        
        if self.langfuse_handler:
            # Do not trace if disabled via metadata
            if config.get("metadata", {}).get("langfuse_disabled"):
                return super().invoke(input, config=config, **kwargs)

            callbacks = config.get("callbacks", [])
            has_langfuse = any(isinstance(callback, LangfuseCallbackHandler) for callback in callbacks)
            
            if not has_langfuse:
                callbacks = callbacks + [self.langfuse_handler]
                config = {**config, "callbacks": callbacks}
        
        return super().invoke(input, config=config, **kwargs)

    async def ainvoke(self, input, config=None, **kwargs):
        """Override ainvoke to add Langfuse callback automatically."""
        if config is None:
            config = {}
        
        if self.langfuse_handler:
            # Do not trace if disabled via metadata
            if config.get("metadata", {}).get("langfuse_disabled"):
                return await super().ainvoke(input, config=config, **kwargs)

            callbacks = config.get("callbacks", [])
            has_langfuse = any(isinstance(callback, LangfuseCallbackHandler) for callback in callbacks)
            
            if not has_langfuse:
                callbacks = callbacks + [self.langfuse_handler]
                config = {**config, "callbacks": callbacks}
        
        return await super().ainvoke(input, config=config, **kwargs)

    def stream(self, input, config=None, **kwargs):
        """Override stream to add Langfuse callback and request usage metadata."""
        if config is None:
            config = {}

        # Add stream_options to get usage data for Langfuse
        stream_options = kwargs.get("stream_options", {})
        stream_options["include_usage"] = True
        kwargs["stream_options"] = stream_options

        # Add Langfuse callback if enabled and not already present
        if self.langfuse_handler and not config.get("metadata", {}).get("langfuse_disabled"):
            callbacks = config.get("callbacks", [])
            if not any(isinstance(c, LangfuseCallbackHandler) for c in callbacks):
                config["callbacks"] = callbacks + [self.langfuse_handler]
        
        yield from super().stream(input, config=config, **kwargs)

    async def astream(self, input, config=None, **kwargs) :
        """Override astream to add Langfuse callback and request usage metadata."""
        if config is None:
            config = {}

        # Add stream_options to get usage data for Langfuse
        stream_options = kwargs.get("stream_options", {})
        stream_options["include_usage"] = True
        kwargs["stream_options"] = stream_options
        
        # Add Langfuse callback if enabled and not already present
        if self.langfuse_handler and not config.get("metadata", {}).get("langfuse_disabled"):
            callbacks = config.get("callbacks", [])
            if not any(isinstance(c, LangfuseCallbackHandler) for c in callbacks):
                config["callbacks"] = callbacks + [self.langfuse_handler]

        async for chunk in super().astream(input, config=config, **kwargs):
            yield chunk

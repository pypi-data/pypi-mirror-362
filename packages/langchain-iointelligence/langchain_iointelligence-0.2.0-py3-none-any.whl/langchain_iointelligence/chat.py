"""Enhanced IOIntelligenceChatModel implementation for LangChain."""

import os
from typing import Any, Dict, Iterator, List, Optional

from dotenv import load_dotenv
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import (AIMessage, BaseMessage, HumanMessage,
                                     SystemMessage)
from langchain_core.messages.ai import UsageMetadata
from langchain_core.outputs import (ChatGeneration, ChatGenerationChunk,
                                    ChatResult)

try:
    from .exceptions import (IOIntelligenceError,
                             IOIntelligenceInvalidResponseError)
    from .http_client import IOIntelligenceHTTPClient
    from .streaming import IOIntelligenceStreamer
    from .utils import IOIntelligenceUtils
except ImportError:
    # Fallback for basic functionality if enhanced modules aren't available
    IOIntelligenceHTTPClient = None
    IOIntelligenceStreamer = None
    IOIntelligenceError = Exception
    IOIntelligenceInvalidResponseError = Exception
    IOIntelligenceUtils = None

    import requests
    from langchain_core.exceptions import \
        OutputParserException as GenerationError

# Load environment variables from .env file
load_dotenv()


class IOIntelligenceChatModel(BaseChatModel):
    """Enhanced LangChain ChatModel wrapper for io Intelligence API."""

    # Declare all fields that will be used
    io_api_key: str = ""
    io_api_url: str = ""
    model: str = "meta-llama/Llama-3.3-70B-Instruct"
    max_tokens: int = 1000
    temperature: float = 0.7
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    streaming: bool = False

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        base_url: Optional[str] = None,  # OpenAI-compatible base_url
        model: str = "meta-llama/Llama-3.3-70B-Instruct",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        streaming: bool = False,
        **kwargs,
    ):
        """Initialize IOIntelligenceChatModel.

        Args:
            api_key: io Intelligence API key (optional, defaults to IO_API_KEY env var)
            api_url: io Intelligence API URL (optional, defaults to IO_API_URL env var)
            base_url: Base URL for OpenAI-compatible interface (auto-adds /v1/chat/completions)
            model: Model name to use (default: "meta-llama/Llama-3.3-70B-Instruct")
            max_tokens: Maximum tokens to generate (default: 1000)
            temperature: Temperature for generation (default: 0.7)
            timeout: Request timeout in seconds (default: 30)
            max_retries: Maximum number of retries (default: 3)
            retry_delay: Initial retry delay in seconds (default: 1.0)
            streaming: Enable streaming responses (default: False)
        """
        # Extract and set API credentials
        api_key = api_key or os.getenv("IO_API_KEY")
        
        # Handle base_url vs api_url
        if base_url and not api_url:
            # Auto-detect and append endpoint if needed
            if base_url.endswith('/chat/completions'):
                api_url = base_url
            elif base_url.endswith('/v1'):
                api_url = f"{base_url}/chat/completions"
            else:
                api_url = f"{base_url}/v1/chat/completions"
        else:
            api_url = api_url or os.getenv("IO_API_URL")

        if not api_key:
            raise ValueError(
                "IO_API_KEY must be provided either as parameter or environment variable"
            )
        if not api_url:
            raise ValueError(
                "IO_API_URL must be provided either as parameter or environment variable"
            )

        # Set field values explicitly
        kwargs.update(
            {
                "io_api_key": api_key,
                "io_api_url": api_url,
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "timeout": timeout,
                "max_retries": max_retries,
                "retry_delay": retry_delay,
                "streaming": streaming,
            }
        )

        super().__init__(**kwargs)

        # Initialize enhanced features if available
        self._http_client: Optional[Any] = None
        self._streamer: Optional[Any] = None
        self._utils: Optional[Any] = None

    @property
    def _llm_type(self) -> str:
        """Return identifier of LLM type."""
        return "io_intelligence_chat"

    @property
    def http_client(self):
        """Get or create HTTP client."""
        if IOIntelligenceHTTPClient is not None and self._http_client is None:
            self._http_client = IOIntelligenceHTTPClient(
                api_key=self.io_api_key,
                api_url=self.io_api_url,
                timeout=self.timeout,
                max_retries=self.max_retries,
                retry_delay=self.retry_delay,
            )
        return self._http_client

    @property
    def streamer(self):
        """Get or create streaming client."""
        if IOIntelligenceStreamer and self._streamer is None:
            self._streamer = IOIntelligenceStreamer(
                api_key=self.io_api_key, api_url=self.io_api_url, timeout=self.timeout
            )
        return self._streamer

    @property
    def utils(self):
        """Get or create utilities client."""
        if IOIntelligenceUtils and self._utils is None:
            self._utils = IOIntelligenceUtils(
                api_key=self.io_api_key, api_url=self.io_api_url, timeout=self.timeout
            )
        return self._utils

    def _convert_messages_to_api_format(self, messages: List[BaseMessage]) -> List[Dict[str, str]]:
        """Convert LangChain messages to API format."""
        api_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                api_messages.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                api_messages.append({"role": "assistant", "content": message.content})
            elif isinstance(message, SystemMessage):
                api_messages.append({"role": "system", "content": message.content})
            else:
                # Generic message - default to user
                api_messages.append({"role": "user", "content": message.content})

        return api_messages

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Run the LLM on the given messages."""
        # Convert messages to API format
        api_messages = self._convert_messages_to_api_format(messages)

        # Prepare request data
        data = {
            "model": self.model,
            "messages": api_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        # Add stop words if provided
        if stop:
            data["stop"] = stop

        # Add any additional kwargs
        data.update(kwargs)

        try:
            # Use enhanced HTTP client if available, otherwise fallback
            if self.http_client is not None:
                response_data = self.http_client.post_with_retry(data)
            else:
                response_data = self._fallback_request(data)

            # Parse response - supports both Chat and Completion formats
            if "choices" not in response_data or not response_data["choices"]:
                error_class = (
                    IOIntelligenceInvalidResponseError
                    if IOIntelligenceInvalidResponseError != Exception
                    else GenerationError
                )
                raise error_class("No choices in API response")

            choice = response_data["choices"][0]

            # Chat format: choices[0].message.content
            if "message" in choice and "content" in choice["message"]:
                content = choice["message"]["content"]
            # Completion format: choices[0].text
            elif "text" in choice:
                content = choice["text"]
            else:
                error_class = (
                    IOIntelligenceInvalidResponseError
                    if IOIntelligenceInvalidResponseError != Exception
                    else GenerationError
                )
                raise error_class(
                    "Unsupported response schema - expected 'message.content' or 'text' in choices"
                )

            # Create AIMessage with the response
            raw_usage = response_data.get("usage", {})
            
            # Create LangChain standard UsageMetadata
            usage_metadata = UsageMetadata(
                input_tokens=raw_usage.get("prompt_tokens", 0),
                output_tokens=raw_usage.get("completion_tokens", 0),
                total_tokens=raw_usage.get("total_tokens", 0),
            )
            
            # Create AIMessage with proper usage_metadata and response_metadata
            message = AIMessage(
                content=content,
                usage_metadata=usage_metadata,
                response_metadata={
                    "token_usage": raw_usage,
                    "model": response_data.get("model", self.model),
                    "finish_reason": choice.get("finish_reason"),
                    "id": response_data.get("id"),
                    "created": response_data.get("created"),
                },
            )

            generation = ChatGeneration(
                message=message,
                generation_info={
                    "model": self.model,
                    "usage": raw_usage,  # Backward compatibility
                    "finish_reason": choice.get("finish_reason"),
                    "response_id": response_data.get("id"),
                    "created": response_data.get("created"),
                },
            )

            return ChatResult(
                generations=[generation],
                llm_output={
                    "token_usage": usage_metadata,
                    "model_name": self.model,
                }
            )

        except Exception as e:
            # Re-raise IOIntelligence-specific errors as-is
            if IOIntelligenceError != Exception and isinstance(e, IOIntelligenceError):
                raise
            # Convert other errors to appropriate types with consistent prefix
            elif IOIntelligenceError != Exception:
                raise IOIntelligenceError(f"API request failed: {str(e)}")
            else:
                raise GenerationError(f"API request failed: {str(e)}")

    def _fallback_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback HTTP request without enhanced features."""
        headers = {
            "Authorization": f"Bearer {self.io_api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(self.io_api_url, headers=headers, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        """Stream the LLM on the given messages."""
        # If streaming is available, use it
        if self.streamer:
            api_messages = self._convert_messages_to_api_format(messages)

            data = {
                "model": self.model,
                "messages": api_messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "stream": True,
            }

            if stop:
                data["stop"] = stop
            data.update(kwargs)

            try:
                for chunk in self.streamer.stream_chat_completion(data):
                    if run_manager:
                        run_manager.on_llm_new_token(chunk.message.content or "")
                    yield chunk
            except Exception as e:
                error_class = (
                    IOIntelligenceError if IOIntelligenceError != Exception else GenerationError
                )
                raise error_class(f"API request failed: Streaming error - {str(e)}")
        else:
            # Fallback: use non-streaming and yield complete response
            result = self._generate(messages, stop, run_manager, **kwargs)
            chunk = ChatGenerationChunk(
                message=result.generations[0].message,
                generation_info=result.generations[0].generation_info,
            )
            yield chunk

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "streaming": self.streaming,
        }


# Alias for backward compatibility
IOIntelligenceChat = IOIntelligenceChatModel

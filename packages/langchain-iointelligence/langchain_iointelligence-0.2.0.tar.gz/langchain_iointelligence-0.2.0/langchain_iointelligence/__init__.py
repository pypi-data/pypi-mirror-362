"""LangChain wrapper for io Intelligence LLM API."""

from .chat import IOIntelligenceChat, IOIntelligenceChatModel
from .exceptions import (IOIntelligenceAPIError,
                         IOIntelligenceAuthenticationError,
                         IOIntelligenceConnectionError, IOIntelligenceError,
                         IOIntelligenceInvalidResponseError,
                         IOIntelligenceRateLimitError,
                         IOIntelligenceServerError, IOIntelligenceTimeoutError)
from .llm import IOIntelligenceLLM
from .utils import (IOIntelligenceUtils, is_model_available,
                    list_available_models)

__version__ = "0.2.0"
__all__ = [
    "IOIntelligenceLLM",
    "IOIntelligenceChatModel",
    "IOIntelligenceChat",
    "IOIntelligenceError",
    "IOIntelligenceAPIError",
    "IOIntelligenceRateLimitError",
    "IOIntelligenceServerError",
    "IOIntelligenceAuthenticationError",
    "IOIntelligenceTimeoutError",
    "IOIntelligenceConnectionError",
    "IOIntelligenceInvalidResponseError",
    "IOIntelligenceUtils",
    "list_available_models",
    "is_model_available",
]

"""IOIntelligence specific exceptions for better error handling."""

from langchain_core.exceptions import OutputParserException as GenerationError


class IOIntelligenceError(GenerationError):
    """Base exception for io Intelligence API errors."""

    pass


class IOIntelligenceAPIError(IOIntelligenceError):
    """General API error."""

    def __init__(self, message: str, status_code: int = None, response_text: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class IOIntelligenceRateLimitError(IOIntelligenceAPIError):
    """Rate limit exceeded (HTTP 429)."""

    pass


class IOIntelligenceServerError(IOIntelligenceAPIError):
    """Server error (HTTP 5xx)."""

    pass


class IOIntelligenceAuthenticationError(IOIntelligenceAPIError):
    """Authentication failed (HTTP 401/403)."""

    pass


class IOIntelligenceTimeoutError(IOIntelligenceError):
    """Request timeout error."""

    pass


class IOIntelligenceConnectionError(IOIntelligenceError):
    """Connection error."""

    pass


class IOIntelligenceInvalidResponseError(IOIntelligenceError):
    """Invalid response format error."""

    pass


def classify_api_error(status_code: int, response_text: str = "") -> IOIntelligenceAPIError:
    """Classify HTTP error into specific exception type."""
    if status_code == 429:
        return IOIntelligenceRateLimitError(
            "Rate limit exceeded. Please try again later.", status_code, response_text
        )
    elif status_code in (401, 403):
        return IOIntelligenceAuthenticationError(
            "Authentication failed. Please check your API key.", status_code, response_text
        )
    elif 500 <= status_code < 600:
        return IOIntelligenceServerError(
            f"Server error (HTTP {status_code}). Please try again later.",
            status_code,
            response_text,
        )
    elif 400 <= status_code < 500:
        return IOIntelligenceAPIError(
            f"Client error (HTTP {status_code}): {response_text}", status_code, response_text
        )
    else:
        return IOIntelligenceAPIError(
            f"HTTP {status_code} error: {response_text}", status_code, response_text
        )

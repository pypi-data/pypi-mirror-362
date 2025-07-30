"""HTTP client with retry logic for io Intelligence API."""

import time
from typing import Any, Dict

import requests

from .exceptions import (
    IOIntelligenceConnectionError,
    IOIntelligenceError,
    IOIntelligenceRateLimitError,
    IOIntelligenceServerError,
    IOIntelligenceTimeoutError,
    classify_api_error,
)


class IOIntelligenceHTTPClient:
    """HTTP client with retry logic and detailed error handling."""

    def __init__(
        self,
        api_key: str,
        api_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        self.api_key = api_key
        self.api_url = api_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )

    def post_with_retry(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Post request with automatic retry logic."""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.post(self.api_url, json=data, timeout=self.timeout)

                # Handle HTTP errors with detailed classification
                if not response.ok:
                    error = classify_api_error(response.status_code, response.text)

                    # Retry on rate limit or server errors
                    if isinstance(error, (IOIntelligenceRateLimitError, IOIntelligenceServerError)):
                        if attempt < self.max_retries:
                            retry_delay = self.retry_delay * (2**attempt)  # Exponential backoff
                            if isinstance(error, IOIntelligenceRateLimitError):
                                retry_delay = max(retry_delay, 60)  # Minimum 60s for rate limits

                            time.sleep(retry_delay)
                            continue

                    raise error

                return response.json()

            except requests.exceptions.Timeout:
                last_exception = IOIntelligenceTimeoutError(
                    f"Request timeout after {self.timeout} seconds"
                )
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2**attempt))
                    continue

            except requests.exceptions.ConnectionError as e:
                last_exception = IOIntelligenceConnectionError(f"Connection error: {str(e)}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2**attempt))
                    continue

            except requests.exceptions.RequestException as e:
                last_exception = IOIntelligenceError(f"Request failed: {str(e)}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2**attempt))
                    continue

            except ValueError as e:  # JSON decode error
                last_exception = IOIntelligenceError(f"Invalid JSON response: {str(e)}")
                break  # Don't retry on JSON errors

        # If we get here, all retries failed
        raise last_exception or IOIntelligenceError("All retry attempts failed")

    def close(self):
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

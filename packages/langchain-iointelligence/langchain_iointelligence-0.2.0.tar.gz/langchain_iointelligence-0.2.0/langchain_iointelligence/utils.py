"""Utility functions for io Intelligence API."""

import os
from typing import Any, Dict, List, Optional

import requests
from dotenv import load_dotenv

from .exceptions import IOIntelligenceError, classify_api_error

load_dotenv()


class IOIntelligenceUtils:
    """Utility class for io Intelligence API operations."""

    def __init__(
        self, api_key: Optional[str] = None, api_url: Optional[str] = None, timeout: int = 30
    ):
        """Initialize utility client.

        Args:
            api_key: API key (defaults to IO_API_KEY env var)
            api_url: API base URL (defaults to IO_API_URL env var)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or os.getenv("IO_API_KEY")
        self.api_url = api_url or os.getenv("IO_API_URL")
        self.timeout = timeout

        if not self.api_key:
            raise ValueError("API key must be provided or set in IO_API_KEY environment variable")
        if not self.api_url:
            raise ValueError("API URL must be provided or set in IO_API_URL environment variable")

        # Extract base URL for models endpoint
        if "/chat/completions" in self.api_url:
            self.base_url = self.api_url.replace("/chat/completions", "")
        else:
            self.base_url = self.api_url.rstrip("/")

    def list_models(self) -> List[Dict[str, Any]]:
        """List available models from the API.

        Returns:
            List of model information dictionaries

        Raises:
            IOIntelligenceError: If the API request fails
        """
        models_url = f"{self.base_url}/models"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(models_url, headers=headers, timeout=self.timeout)

            if not response.ok:
                error = classify_api_error(response.status_code, response.text)
                raise error

            data = response.json()

            # Handle OpenAI-compatible format
            if "data" in data:
                return data["data"]
            # Handle direct list format
            elif isinstance(data, list):
                return data
            else:
                raise IOIntelligenceError("Unexpected models response format")

        except requests.exceptions.RequestException as e:
            raise IOIntelligenceError(f"Failed to fetch models: {str(e)}")

    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific model.

        Args:
            model_id: The model identifier

        Returns:
            Model information dictionary

        Raises:
            IOIntelligenceError: If the model is not found or API request fails
        """
        try:
            models = self.list_models()
            for model in models:
                if model.get("id") == model_id or model.get("name") == model_id:
                    return model

            raise IOIntelligenceError(f"Model '{model_id}' not found")

        except IOIntelligenceError:
            raise
        except Exception as e:
            raise IOIntelligenceError(f"Failed to get model info: {str(e)}")

    def validate_model(self, model_id: str) -> bool:
        """Check if a model exists and is available.

        Args:
            model_id: The model identifier to validate

        Returns:
            True if model exists, False otherwise
        """
        try:
            self.get_model_info(model_id)
            return True
        except IOIntelligenceError:
            return False

    def get_recommended_models(self) -> List[str]:
        """Get list of recommended model IDs for common use cases.

        Returns:
            List of recommended model identifiers
        """
        try:
            models = self.list_models()
            recommended = []

            # Look for common high-quality models
            preferred_patterns = [
                "llama-3.3-70b",
                "llama-3.1-405b",
                "llama-3.1-70b",
                "llama-3-70b",
                "mixtral-8x7b",
            ]

            for model in models:
                model_id = model.get("id", "").lower()
                for pattern in preferred_patterns:
                    if pattern in model_id:
                        recommended.append(model.get("id"))
                        break

            # If no specific patterns found, return first few models
            if not recommended and models:
                recommended = [m.get("id") for m in models[:3] if m.get("id")]

            return recommended

        except Exception:
            # Fallback to known good models
            return [
                "meta-llama/Llama-3.3-70B-Instruct",
                "meta-llama/Llama-3.1-405B-Instruct",
                "meta-llama/Llama-3.1-70B-Instruct",
            ]


# Convenience function for quick model listing
def list_available_models(
    api_key: Optional[str] = None, api_url: Optional[str] = None
) -> List[str]:
    """Quick function to list available model IDs.

    Args:
        api_key: API key (optional, uses environment variable)
        api_url: API URL (optional, uses environment variable)

    Returns:
        List of available model IDs
    """
    utils = IOIntelligenceUtils(api_key, api_url)
    models = utils.list_models()
    return [model.get("id") for model in models if model.get("id")]


# Convenience function for model validation
def is_model_available(
    model_id: str, api_key: Optional[str] = None, api_url: Optional[str] = None
) -> bool:
    """Quick function to check if a model is available.

    Args:
        model_id: Model identifier to check
        api_key: API key (optional, uses environment variable)
        api_url: API URL (optional, uses environment variable)

    Returns:
        True if model is available, False otherwise
    """
    try:
        utils = IOIntelligenceUtils(api_key, api_url)
        return utils.validate_model(model_id)
    except Exception:
        return False

"""Test cases for IOIntelligenceLLM."""

import os
from unittest.mock import Mock, patch

import pytest
from langchain_core.exceptions import OutputParserException as GenerationError

from langchain_iointelligence.llm import IOIntelligenceLLM


class TestIOIntelligenceLLM:
    """Test cases for IOIntelligenceLLM class."""

    def test_init_with_env_vars(self):
        """Test initialization with environment variables."""
        with patch.dict(
            os.environ,
            {
                "IO_API_KEY": "test_key",
                "IO_API_URL": "https://test.api.com/v1/chat/completions"
            },
        ):
            llm = IOIntelligenceLLM()
            assert llm.io_api_key == "test_key"
            assert llm.io_api_url == "https://test.api.com/v1/chat/completions"

    def test_init_with_params(self):
        """Test initialization with explicit parameters."""
        llm = IOIntelligenceLLM(
            api_key="param_key",
            api_url="https://param.api.com/v1/chat/completions",
            model="custom-model",
            max_tokens=2000,
            temperature=0.5,
        )
        assert llm.io_api_key == "param_key"
        assert llm.io_api_url == "https://param.api.com/v1/chat/completions"
        assert llm.model == "custom-model"
        assert llm.max_tokens == 2000
        assert llm.temperature == 0.5

    def test_init_missing_api_key(self):
        """Test initialization fails when API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(
                ValueError, match="IO_API_KEY must be provided"
            ):
                IOIntelligenceLLM()

    def test_init_missing_api_url(self):
        """Test initialization fails when API URL is missing."""
        with patch.dict(os.environ, {"IO_API_KEY": "test_key"}, clear=True):
            with pytest.raises(
                ValueError, match="IO_API_URL must be provided"
            ):
                IOIntelligenceLLM()

    def test_llm_type(self):
        """Test _llm_type property."""
        llm = IOIntelligenceLLM(
            api_key="test_key",
            api_url="https://test.api.com/v1/chat/completions"
        )
        assert llm._llm_type == "io_intelligence"

    def test_identifying_params(self):
        """Test _identifying_params property."""
        llm = IOIntelligenceLLM(
            api_key="test_key",
            api_url="https://test.api.com/v1/chat/completions",
            model="test-model",
            max_tokens=1500,
            temperature=0.8,
        )
        params = llm._identifying_params
        assert params["model"] == "test-model"
        assert params["max_tokens"] == 1500
        assert params["temperature"] == 0.8

    @patch("langchain_iointelligence.llm.requests.post")
    def test_call_success(self, mock_post):
        """Test successful API call."""
        # Mock successful response - Chat format
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "This is a test response"}}]
        }
        mock_post.return_value = mock_response

        llm = IOIntelligenceLLM(
            api_key="test_key",
            api_url="https://test.api.com/v1/chat/completions"
        )

        result = llm._call("Test prompt")
        assert result == "This is a test response"

        # Verify API call was made correctly - Chat format
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[1]["headers"]["Authorization"] == "Bearer test_key"
        assert "messages" in call_args[1]["json"]
        assert call_args[1]["json"]["messages"][0]["content"] == "Test prompt"
        assert (
            call_args[1]["json"]["model"] == "meta-llama/Llama-3.3-70B-Instruct"
        )
        assert call_args[1]["json"]["max_tokens"] == 1000
        assert call_args[1]["json"]["temperature"] == 0.7

    @patch("langchain_iointelligence.llm.requests.post")
    def test_call_with_stop_words(self, mock_post):
        """Test API call with stop words."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Response with stop"}}]
        }
        mock_post.return_value = mock_response

        llm = IOIntelligenceLLM(
            api_key="test_key",
            api_url="https://test.api.com/v1/chat/completions"
        )

        result = llm._call("Test prompt", stop=["stop", "end"])
        assert result == "Response with stop"

        # Verify stop words were included
        call_args = mock_post.call_args
        assert call_args[1]["json"]["stop"] == ["stop", "end"]

    @patch("langchain_iointelligence.llm.requests.post")
    def test_call_request_exception(self, mock_post):
        """Test API call with request exception."""
        import requests
        mock_post.side_effect = requests.exceptions.RequestException(
            "Connection error"
        )

        llm = IOIntelligenceLLM(
            api_key="test_key",
            api_url="https://test.api.com/v1/chat/completions"
        )

        with pytest.raises(GenerationError, match="API request failed"):
            llm._call("Test prompt")

    @patch("langchain_iointelligence.llm.requests.post")
    def test_call_invalid_response_format(self, mock_post):
        """Test API call with invalid response format."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"invalid": "response"}
        mock_post.return_value = mock_response

        llm = IOIntelligenceLLM(
            api_key="test_key",
            api_url="https://test.api.com/v1/chat/completions"
        )

        with pytest.raises(
            GenerationError, match="No choices in API response"
        ):
            llm._call("Test prompt")

    @patch("langchain_iointelligence.llm.requests.post")
    def test_call_empty_choices(self, mock_post):
        """Test API call with empty choices."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"choices": []}
        mock_post.return_value = mock_response

        llm = IOIntelligenceLLM(
            api_key="test_key",
            api_url="https://test.api.com/v1/chat/completions"
        )

        with pytest.raises(
            GenerationError, match="No choices in API response"
        ):
            llm._call("Test prompt")

    def test_integration_example(self):
        """Test integration with LangChain components (mock)."""
        # This is a mock integration test to show how it would work
        with patch("langchain_iointelligence.llm.requests.post") as mock_post:
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {
                "choices": [
                    {"message": {"content": "Integration test response"}}
                ]
            }
            mock_post.return_value = mock_response

            llm = IOIntelligenceLLM(
                api_key="test_key",
                api_url="https://test.api.com/v1/chat/completions"
            )

            # Test direct call (using invoke instead of deprecated __call__)
            result = llm.invoke("Test integration prompt")
            assert result == "Integration test response"

    @patch.dict(
        os.environ,
        {
            "IO_API_KEY": "env_test_key",
            "IO_API_URL": "https://env.test.api.com/v1/chat/completions",
        },
    )
    @patch("langchain_iointelligence.llm.requests.post")
    def test_env_loading_integration(self, mock_post):
        """Test that environment variables are loaded correctly."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Env test response"}}]
        }
        mock_post.return_value = mock_response

        llm = IOIntelligenceLLM()
        result = llm.invoke("Test env prompt")

        assert result == "Env test response"

        # Verify correct API key was used
        call_args = mock_post.call_args
        assert (
            call_args[1]["headers"]["Authorization"] == "Bearer env_test_key"
        )
        assert (
            call_args[0][0] == "https://env.test.api.com/v1/chat/completions"
        )


if __name__ == "__main__":
    pytest.main([__file__])

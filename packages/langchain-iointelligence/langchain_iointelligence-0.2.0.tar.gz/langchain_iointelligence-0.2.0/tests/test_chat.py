"""Test cases for IOIntelligenceChatModel."""

import os
from unittest.mock import Mock, patch, PropertyMock

import pytest
from langchain_core.exceptions import OutputParserException as GenerationError
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from langchain_iointelligence.chat import IOIntelligenceChatModel
from langchain_iointelligence.exceptions import IOIntelligenceConnectionError, IOIntelligenceInvalidResponseError


class TestIOIntelligenceChatModel:
    """Test cases for IOIntelligenceChatModel class."""

    def test_init_with_env_vars(self):
        """Test initialization with environment variables."""
        with patch.dict(
            os.environ,
            {"IO_API_KEY": "test_key", "IO_API_URL": "https://test.api.com/v1/chat/completions"},
        ):
            chat = IOIntelligenceChatModel()
            assert chat.io_api_key == "test_key"
            assert chat.io_api_url == "https://test.api.com/v1/chat/completions"

    def test_init_with_params(self):
        """Test initialization with explicit parameters."""
        chat = IOIntelligenceChatModel(
            api_key="param_key",
            api_url="https://param.api.com/v1/chat/completions",
            model="custom-model",
            max_tokens=2000,
            temperature=0.5,
            timeout=60,
            max_retries=5,
        )
        assert chat.io_api_key == "param_key"
        assert chat.io_api_url == "https://param.api.com/v1/chat/completions"
        assert chat.model == "custom-model"
        assert chat.max_tokens == 2000
        assert chat.temperature == 0.5
        assert chat.timeout == 60
        assert chat.max_retries == 5

    def test_init_missing_api_key(self):
        """Test initialization fails when API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="IO_API_KEY must be provided"):
                IOIntelligenceChatModel()

    def test_llm_type(self):
        """Test _llm_type property."""
        chat = IOIntelligenceChatModel(
            api_key="test_key", api_url="https://test.api.com/v1/chat/completions"
        )
        assert chat._llm_type == "io_intelligence_chat"

    def test_convert_messages_to_api_format(self):
        """Test message conversion to API format."""
        chat = IOIntelligenceChatModel(
            api_key="test_key", api_url="https://test.api.com/v1/chat/completions"
        )

        messages = [
            SystemMessage(content="You are a helpful assistant"),
            HumanMessage(content="Hello"),
            AIMessage(content="Hi there!"),
        ]

        api_messages = chat._convert_messages_to_api_format(messages)

        expected = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]

        assert api_messages == expected

    def test_generate_success(self):
        """Test successful chat generation."""
        chat = IOIntelligenceChatModel(
            api_key="test_key", api_url="https://test.api.com/v1/chat/completions"
        )

        # Mock the http_client property to return a mock client
        mock_client = Mock()
        mock_client.post_with_retry.return_value = {
            "choices": [
                {"message": {"content": "This is a test response"}, "finish_reason": "stop"}
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        }

        # Use PropertyMock to mock the property correctly
        with patch.object(type(chat), 'http_client', new_callable=PropertyMock) as mock_http_client:
            mock_http_client.return_value = mock_client
            
            messages = [HumanMessage(content="Test message")]
            result = chat._generate(messages)

            assert len(result.generations) == 1
            generation = result.generations[0]
            assert isinstance(generation.message, AIMessage)
            assert generation.message.content == "This is a test response"
            assert generation.generation_info["finish_reason"] == "stop"
            assert generation.generation_info["usage"]["total_tokens"] == 15
            
            # Check usage_metadata is properly set
            assert generation.message.usage_metadata["input_tokens"] == 10
            assert generation.message.usage_metadata["output_tokens"] == 5
            assert generation.message.usage_metadata["total_tokens"] == 15

            # Verify API call was made correctly
            mock_client.post_with_retry.assert_called_once()
            call_args = mock_client.post_with_retry.call_args[0][0]
            assert "messages" in call_args
            assert call_args["messages"][0]["content"] == "Test message"

    def test_generate_with_stop_words(self):
        """Test generation with stop words."""
        chat = IOIntelligenceChatModel(
            api_key="test_key", api_url="https://test.api.com/v1/chat/completions"
        )

        mock_client = Mock()
        mock_client.post_with_retry.return_value = {
            "choices": [{"message": {"content": "Response with stop"}}]
        }

        with patch.object(type(chat), 'http_client', new_callable=PropertyMock) as mock_http_client:
            mock_http_client.return_value = mock_client
            
            messages = [HumanMessage(content="Test prompt")]
            result = chat._generate(messages, stop=["stop", "end"])

            assert result.generations[0].message.content == "Response with stop"

            # Verify stop words were included
            call_args = mock_client.post_with_retry.call_args[0][0]
            assert call_args["stop"] == ["stop", "end"]

    def test_generate_completion_format(self):
        """Test generation with completion format response."""
        chat = IOIntelligenceChatModel(
            api_key="test_key", api_url="https://test.api.com/v1/chat/completions"
        )

        mock_client = Mock()
        mock_client.post_with_retry.return_value = {"choices": [{"text": "Completion format response"}]}

        with patch.object(type(chat), 'http_client', new_callable=PropertyMock) as mock_http_client:
            mock_http_client.return_value = mock_client
            
            messages = [HumanMessage(content="Test message")]
            result = chat._generate(messages)

            assert result.generations[0].message.content == "Completion format response"

    def test_generate_request_exception(self):
        """Test generation with request exception."""
        chat = IOIntelligenceChatModel(
            api_key="test_key", api_url="https://test.api.com/v1/chat/completions"
        )

        mock_client = Mock()
        mock_client.post_with_retry.side_effect = IOIntelligenceConnectionError("Connection error")

        with patch.object(type(chat), 'http_client', new_callable=PropertyMock) as mock_http_client:
            mock_http_client.return_value = mock_client
            
            messages = [HumanMessage(content="Test message")]

            with pytest.raises(IOIntelligenceConnectionError, match="Connection error"):
                chat._generate(messages)

    def test_generate_invalid_response(self):
        """Test generation with invalid response format."""
        chat = IOIntelligenceChatModel(
            api_key="test_key", api_url="https://test.api.com/v1/chat/completions"
        )

        mock_client = Mock()
        mock_client.post_with_retry.return_value = {"invalid": "response"}

        with patch.object(type(chat), 'http_client', new_callable=PropertyMock) as mock_http_client:
            mock_http_client.return_value = mock_client
            
            messages = [HumanMessage(content="Test message")]

            # Should raise IOIntelligenceInvalidResponseError or GenerationError
            with pytest.raises((IOIntelligenceInvalidResponseError, GenerationError), match="No choices in API response"):
                chat._generate(messages)

    def test_invoke_integration(self):
        """Test invoke method integration."""
        chat = IOIntelligenceChatModel(
            api_key="test_key", api_url="https://test.api.com/v1/chat/completions"
        )

        mock_client = Mock()
        mock_client.post_with_retry.return_value = {
            "choices": [{"message": {"content": "Integration test response"}}]
        }

        with patch.object(type(chat), 'http_client', new_callable=PropertyMock) as mock_http_client:
            mock_http_client.return_value = mock_client
            
            messages = [HumanMessage(content="Test integration")]
            result = chat.invoke(messages)

            assert isinstance(result, AIMessage)
            assert result.content == "Integration test response"

    def test_identifying_params(self):
        """Test _identifying_params property."""
        chat = IOIntelligenceChatModel(
            api_key="test_key",
            api_url="https://test.api.com/v1/chat/completions",
            model="test-model",
            max_tokens=1500,
            temperature=0.8,
            timeout=45,
            max_retries=2,
        )
        params = chat._identifying_params
        assert params["model"] == "test-model"
        assert params["max_tokens"] == 1500
        assert params["temperature"] == 0.8
        assert params["timeout"] == 45
        assert params["max_retries"] == 2


if __name__ == "__main__":
    pytest.main([__file__])

"""Test usage metadata mapping functionality."""

from unittest.mock import Mock, PropertyMock, patch

import pytest
from langchain_core.messages import HumanMessage

from langchain_iointelligence.chat import IOIntelligenceChatModel


class TestUsageMetadata:
    """Test usage metadata mapping."""

    def test_usage_metadata_mapping(self):
        """Test that usage data is correctly mapped to AIMessage.usage_metadata."""
        chat = IOIntelligenceChatModel(
            api_key="test_key",
            api_url="https://test.api.com/v1/chat/completions"
        )

        mock_client = Mock()
        mock_client.post_with_retry.return_value = {
            "choices": [
                {"message": {"content": "Test response"}, "finish_reason": "stop"}
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        }

        with patch.object(type(chat), 'http_client', new_callable=PropertyMock) as mock_http_client:
            mock_http_client.return_value = mock_client
            
            messages = [HumanMessage(content="Test message")]
            result = chat._generate(messages)

            # Check that usage_metadata is correctly set on AIMessage
            ai_message = result.generations[0].message
            assert hasattr(ai_message, 'usage_metadata')
            assert ai_message.usage_metadata["input_tokens"] == 10
            assert ai_message.usage_metadata["output_tokens"] == 20
            assert ai_message.usage_metadata["total_tokens"] == 30
            
            # Check response_metadata
            assert hasattr(ai_message, 'response_metadata')
            assert ai_message.response_metadata["token_usage"]["prompt_tokens"] == 10
            assert ai_message.response_metadata["model"] == "meta-llama/Llama-3.3-70B-Instruct"

    def test_usage_metadata_partial_data(self):
        """Test usage metadata mapping with partial data."""
        chat = IOIntelligenceChatModel(
            api_key="test_key",
            api_url="https://test.api.com/v1/chat/completions"
        )

        mock_client = Mock()
        mock_client.post_with_retry.return_value = {
            "choices": [
                {"message": {"content": "Test response"}}
            ],
            "usage": {
                "total_tokens": 30
                # Missing prompt_tokens and completion_tokens
            }
        }

        with patch.object(type(chat), 'http_client', new_callable=PropertyMock) as mock_http_client:
            mock_http_client.return_value = mock_client
            
            messages = [HumanMessage(content="Test message")]
            result = chat._generate(messages)

            # Check that only available usage data is mapped, others default to 0
            ai_message = result.generations[0].message
            assert ai_message.usage_metadata["total_tokens"] == 30
            assert ai_message.usage_metadata["input_tokens"] == 0  # Default when missing
            assert ai_message.usage_metadata["output_tokens"] == 0  # Default when missing

    def test_usage_metadata_no_usage_data(self):
        """Test usage metadata when no usage data is provided."""
        chat = IOIntelligenceChatModel(
            api_key="test_key",
            api_url="https://test.api.com/v1/chat/completions"
        )

        mock_client = Mock()
        mock_client.post_with_retry.return_value = {
            "choices": [
                {"message": {"content": "Test response"}}
            ]
            # No usage field
        }

        with patch.object(type(chat), 'http_client', new_callable=PropertyMock) as mock_http_client:
            mock_http_client.return_value = mock_client
            
            messages = [HumanMessage(content="Test message")]
            result = chat._generate(messages)

            # Check that usage_metadata defaults to 0 when no usage data
            ai_message = result.generations[0].message
            assert ai_message.usage_metadata["input_tokens"] == 0
            assert ai_message.usage_metadata["output_tokens"] == 0
            assert ai_message.usage_metadata["total_tokens"] == 0


if __name__ == "__main__":
    pytest.main([__file__])

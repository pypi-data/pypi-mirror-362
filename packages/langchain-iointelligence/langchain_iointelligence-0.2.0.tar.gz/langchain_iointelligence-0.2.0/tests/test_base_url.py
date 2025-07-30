"""Test base_url functionality."""

import pytest
from langchain_iointelligence.chat import IOIntelligenceChatModel


class TestBaseURL:
    """Test base_url parameter functionality."""

    def test_base_url_auto_append_v1_chat_completions(self):
        """Test that base_url automatically appends /v1/chat/completions."""
        chat = IOIntelligenceChatModel(
            api_key="test_key",
            base_url="https://api.example.com"
        )
        
        assert chat.io_api_url == "https://api.example.com/v1/chat/completions"

    def test_base_url_auto_append_chat_completions(self):
        """Test that base_url with /v1 automatically appends /chat/completions."""
        chat = IOIntelligenceChatModel(
            api_key="test_key",
            base_url="https://api.example.com/v1"
        )
        
        assert chat.io_api_url == "https://api.example.com/v1/chat/completions"

    def test_base_url_full_endpoint_no_change(self):
        """Test that full endpoint URL is used as-is."""
        chat = IOIntelligenceChatModel(
            api_key="test_key",
            base_url="https://api.example.com/v1/chat/completions"
        )
        
        assert chat.io_api_url == "https://api.example.com/v1/chat/completions"

    def test_api_url_takes_precedence_over_base_url(self):
        """Test that explicit api_url takes precedence over base_url."""
        chat = IOIntelligenceChatModel(
            api_key="test_key",
            api_url="https://explicit.api.com/v1/chat/completions",
            base_url="https://base.api.com"
        )
        
        assert chat.io_api_url == "https://explicit.api.com/v1/chat/completions"


if __name__ == "__main__":
    pytest.main([__file__])

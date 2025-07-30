"""Simple test without langsmith dependencies."""

from unittest.mock import Mock, patch


# Skip langsmith-related tests
def test_basic_import():
    """Test that the package can be imported."""
    from langchain_iointelligence import IOIntelligenceLLM

    assert IOIntelligenceLLM is not None


def test_llm_initialization():
    """Test LLM initialization."""
    from langchain_iointelligence.llm import IOIntelligenceLLM

    llm = IOIntelligenceLLM(api_key="test_key", api_url="https://test.api.com/v1/completions")
    assert llm.io_api_key == "test_key"
    assert llm.io_api_url == "https://test.api.com/v1/completions"
    assert llm._llm_type == "io_intelligence"


@patch("langchain_iointelligence.llm.requests.post")
def test_basic_call(mock_post):
    """Test basic API call."""
    from langchain_iointelligence.llm import IOIntelligenceLLM

    # Mock successful response
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"choices": [{"text": "Test response"}]}
    mock_post.return_value = mock_response

    llm = IOIntelligenceLLM(api_key="test_key", api_url="https://test.api.com/v1/completions")

    result = llm._call("Test prompt")
    assert result == "Test response"


if __name__ == "__main__":
    test_basic_import()
    test_llm_initialization()
    print("✅ Basic tests passed!")

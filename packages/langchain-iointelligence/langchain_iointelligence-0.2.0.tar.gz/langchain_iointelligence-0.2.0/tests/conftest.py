"""Test configuration and fixtures for GitHub Actions."""

import os
from unittest.mock import patch

import pytest


# GitHub Actions用のテスト環境変数設定
@pytest.fixture(autouse=True)
def setup_test_env():
    """テスト用環境変数を自動設定"""
    with patch.dict(
        os.environ,
        {
            "IO_API_KEY": "test_api_key_for_github_actions",
            "IO_API_URL": "https://test.example.com/v1/chat/completions",
        },
    ):
        yield


# dotenvの読み込みを無効化（CIでは不要）
@pytest.fixture(autouse=True)
def disable_dotenv():
    """dotenvの読み込みを無効化"""
    with patch("langchain_iointelligence.llm.load_dotenv"):
        with patch("langchain_iointelligence.chat.load_dotenv"):
            yield

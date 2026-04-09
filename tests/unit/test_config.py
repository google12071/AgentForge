"""Test configuration module"""

import pytest
from src.utils.config import Settings


def test_settings_default_values():
    """Test default settings values"""
    settings = Settings()

    assert settings.llm_provider == "qwen"
    assert settings.qwen_model == "qwen-plus"
    assert settings.qwen_embedding_model == "text-embedding-v3"
    assert settings.deepseek_model == "deepseek-chat"
    assert settings.chroma_persist_directory == "data/chroma_db"
    assert settings.log_level == "INFO"
    assert settings.agent_max_iterations == 10


def test_settings_can_be_customized():
    """Test settings can be customized via environment"""
    # Note: In real tests, use pytest fixtures to set env vars
    settings = Settings(llm_provider="deepseek", log_level="DEBUG")

    assert settings.llm_provider == "deepseek"
    assert settings.log_level == "DEBUG"
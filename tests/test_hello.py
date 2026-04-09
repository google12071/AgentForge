"""Hello World test for LLM connection"""

import pytest

from src.utils.llm_client import get_llm_client
from src.utils.logger import get_logger

logger = get_logger("test_hello")


def test_llm_connection():
    """Test basic LLM API connection"""
    client = get_llm_client()

    response = client.simple_chat("你好，请回复'Hello AgentForge'")

    assert response is not None
    assert len(response) > 0

    logger.info(f"LLM Response: {response}")
    print(f"\n✅ LLM连接成功！\n响应: {response}")


def test_llm_chat():
    """Test multi-turn chat capability"""
    client = get_llm_client()

    messages = [
        {"role": "system", "content": "你是一个AI助手，请用简洁的语言回答问题。"},
        {"role": "user", "content": "什么是Agent？请用一句话解释。"},
    ]

    response = client.chat(messages)

    assert response is not None
    assert len(response) > 0

    logger.info(f"Chat Response: {response}")
    print(f"\n✅ 多轮对话测试成功！\n响应: {response}")
"""LLM Client wrapper supporting Qwen and DeepSeek"""

from typing import Optional, List, Dict, Any

import dashscope
from dashscope import Generation
from openai import OpenAI

from .config import settings
from .logger import get_logger

logger = get_logger("llm_client")


class LLMClient:
    """Unified LLM client for Qwen and DeepSeek"""

    def __init__(self) -> None:
        self.provider = settings.llm_provider
        self._init_client()
        logger.info(f"LLM client initialized with provider: {self.provider}")

    def _init_client(self) -> None:
        """Initialize the appropriate LLM client based on provider"""
        if self.provider == "qwen":
            if not settings.qwen_api_key:
                raise ValueError("QWEN_API_KEY is not set in .env file")
            dashscope.api_key = settings.qwen_api_key
            self.model = settings.qwen_model
        elif self.provider == "deepseek":
            if not settings.deepseek_api_key:
                raise ValueError("DEEPSEEK_API_KEY is not set in .env file")
            self.client = OpenAI(
                api_key=settings.deepseek_api_key,
                base_url="https://api.deepseek.com/v1",
            )
            self.model = settings.deepseek_model
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Send chat messages and get response

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response

        Returns:
            LLM response text
        """
        temp = temperature or 0.7
        tokens = max_tokens or 4096

        try:
            if self.provider == "qwen":
                response = Generation.call(
                    model=self.model,
                    messages=messages,
                    temperature=temp,
                    max_tokens=tokens,
                    result_format="message",
                )
                if response.status_code != 200:
                    raise RuntimeError(f"Qwen API error: {response.code} - {response.message}")
                return response.output.choices[0].message.content

            elif self.provider == "deepseek":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temp,
                    max_tokens=tokens,
                )
                return response.choices[0].message.content

        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            raise

    def simple_chat(self, prompt: str) -> str:
        """Simple single-turn chat

        Args:
            prompt: User input prompt

        Returns:
            LLM response text
        """
        return self.chat([{"role": "user", "content": prompt}])


# Global client instance
llm_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create LLM client instance"""
    global llm_client
    if llm_client is None:
        llm_client = LLMClient()
    return llm_client
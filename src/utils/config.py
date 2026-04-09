"""Configuration management using Pydantic Settings"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM Provider - 通义千问 / DeepSeek
    llm_provider: str = Field(default="qwen", description="LLM provider: qwen or deepseek")

    # 通义千问 API
    qwen_api_key: str = Field(default="", description="通义千问 API Key")
    qwen_model: str = Field(default="qwen-plus", description="通义千问模型名称")
    qwen_embedding_model: str = Field(default="text-embedding-v3", description="通义嵌入模型")

    # DeepSeek API
    deepseek_api_key: str = Field(default="", description="DeepSeek API Key")
    deepseek_model: str = Field(default="deepseek-chat", description="DeepSeek 模型名称")

    # ChromaDB
    chroma_persist_directory: str = Field(default="data/chroma_db", description="向量数据库存储路径")

    # Logging
    log_level: str = Field(default="INFO", description="日志级别")
    log_file: str = Field(default="logs/agentforge.log", description="日志文件路径")

    # Agent
    agent_max_iterations: int = Field(default=10, description="Agent 最大迭代次数")
    agent_timeout: float = Field(default=30.0, description="Agent 超时时间（秒）")


# Global settings instance
settings = Settings()
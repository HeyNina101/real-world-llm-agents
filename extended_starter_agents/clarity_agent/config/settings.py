from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    # API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # LLM Configuration
    default_llm_provider: Literal["openai", "anthropic"] = "openai"
    openai_model: str = "gpt-3.5-turbo"
    anthropic_model: str = "claude-3-sonnet-20240229"
    
    # API Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Agent Configuration
    max_topic_length: int = 200
    max_pros_cons: int = 10
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
import os
from dotenv import load_dotenv
from llm.platforms.openai import OpenAIProvider
from llm.platforms.anthropic import AnthropicProvider

load_dotenv()

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "openai")
    model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    api_key = os.getenv("LLM_API_KEY")

    if not api_key:
        raise ValueError("Missing LLM_API_KEY")

    if provider == "openai":
        return OpenAIProvider(api_key, model)
    elif provider == "anthropic":
        return AnthropicProvider(api_key, model)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

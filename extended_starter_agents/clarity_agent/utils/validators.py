from typing import Dict, Any
from config.settings import settings


def validate_topic_length(topic: str) -> Dict[str, Any]:
    """Validates that the topic has an appropriate length."""
    if len(topic.strip()) < 3:
        return {
            "valid": False,
            "message": "Topic must have at least 3 characters"
        }
    
    if len(topic) > settings.max_topic_length:
        return {
            "valid": False,
            "message": f"Topic cannot exceed {settings.max_topic_length} characters"
        }
    
    return {
        "valid": True,
        "message": "Valid topic"
    }


def validate_api_key(api_key: str, provider: str) -> Dict[str, Any]:
    """Validates that the API key has the correct format."""
    if not api_key:
        return {
            "valid": False,
            "message": f"API key required for {provider}"
        }
    
    if provider == "openai" and not api_key.startswith("sk-"):
        return {
            "valid": False,
            "message": "OpenAI API key must start with 'sk-'"
        }
    
    if provider == "anthropic" and not api_key.startswith("sk-ant-"):
        return {
            "valid": False,
            "message": "Anthropic API key must start with 'sk-ant-'"
        }
    
    return {
        "valid": True,
        "message": "Valid API key"
    }
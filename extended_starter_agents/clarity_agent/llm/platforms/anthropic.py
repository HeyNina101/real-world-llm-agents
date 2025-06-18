from anthropic import AsyncAnthropic
from typing import Dict, Any, Optional
from ..base_llm import BaseLLMProvider, LLMResponse
from utils.logger import logger


class AnthropicProvider(BaseLLMProvider):
    """Provider for Anthropic models (Claude)."""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        self.client: AsyncAnthropic = AsyncAnthropic(api_key=api_key)
        super().__init__(api_key, model)
    
    def _validate_credentials(self) -> None:
        """Validates Anthropic credentials."""
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        
        self.client = AsyncAnthropic(api_key=self.api_key)
        logger.info(f"Anthropic provider initialized with model: {self.model}")
    
    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Generates response using Anthropic Claude."""
        try:
            kwargs = {
                "model": self.model,
                "max_tokens": 1000,
                "temperature": 0.7,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            if system_prompt:
                kwargs["system"] = system_prompt
            
            response = await self.client.messages.create(**kwargs)
            
            return LLMResponse(
                content=response.content[0].text,
                model=self.model,
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating Anthropic response: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Returns Anthropic model information."""
        return {
            "provider": "anthropic",
            "model": self.model,
            "max_tokens": 200000,  # Claude 3 context window
            "supports_system_messages": True
        }

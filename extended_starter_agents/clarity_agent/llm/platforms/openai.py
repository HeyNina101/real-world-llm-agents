from openai import AsyncOpenAI
from typing import Dict, Any, Optional
from ..base_llm import BaseLLMProvider, LLMResponse
from utils.logger import logger
from typing import Any, cast


class OpenAIProvider(BaseLLMProvider):
    """Provider for OpenAI models."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=self.api_key)
    
    def _validate_credentials(self) -> None:
        """Validates OpenAI credentials."""
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        logger.info(f"OpenAI provider initialized with model: {self.model}")
    
    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Generates response using OpenAI."""
        try:
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            response: Any  = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return LLMResponse(
               content=cast(str, response.choices[0].message.content),
                model=self.model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Returns OpenAI model information."""
        return {
            "provider": "openai",
            "model": self.model,
            "max_tokens": 4096 if "gpt-3.5" in self.model else 8192,
            "supports_system_messages": True
        }
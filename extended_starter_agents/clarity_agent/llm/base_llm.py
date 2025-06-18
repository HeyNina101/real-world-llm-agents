from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class LLMResponse(BaseModel):
    content: str
    model: str
    usage: Dict[str, Any] = {}


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers."""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self._validate_credentials()
    
    @abstractmethod
    def _validate_credentials(self) -> None:
        """Validates provider credentials."""
        pass
    
    @abstractmethod
    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """Generates a response using the LLM model."""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Returns information about the current model."""
        pass
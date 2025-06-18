from abc import ABC, abstractmethod
from typing import Dict, Any
from pydantic import BaseModel
from llm.base_llm import BaseLLMProvider


class AgentResponse(BaseModel):
    """Standard agent response."""
    success: bool
    data: Dict[str, Any]
    message: str = ""
    metadata: Dict[str, Any] = {}


class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, llm_provider: BaseLLMProvider):
        self.llm_provider = llm_provider
    
    @abstractmethod
    async def process(self, input_data: str) -> AgentResponse:
        """Processes input and returns a response."""
        pass
    
    @abstractmethod
    def get_agent_info(self) -> Dict[str, Any]:
        """Returns information about the agent."""
        pass
    
    def _validate_input(self, input_data: str) -> bool:
        """Validates user input."""
        return bool(input_data and input_data.strip())
import json
from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentResponse
from utils.logger import logger
from utils.validators import validate_topic_length


class ClarityAgent(BaseAgent):
    """Clarity Agent that analyzes topics and presents pros and cons."""

    def __init__(self, llm_provider):
        super().__init__(llm_provider)
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Builds the system prompt for the clarity agent."""
        return """You are an expert clarity agent specialized in critical analysis. Your task is to analyze any topic presented to you and provide a balanced list of pros and cons.

INSTRUCTIONS:
1. Analyze the topic objectively and impartially
2. Provide between 3-8 pros and between 3-8 cons
3. Each point should be clear, concise and relevant
4. Maintain balance between both perspectives
5. Use accessible but professional language

RESPONSE FORMAT (JSON):
{
    "topic": "analyzed topic",
    "analysis": {
        "pros": ["pro 1", "pro 2", "pro 3"],
        "cons": ["con 1", "con 2", "con 3"]
    },
    "summary": "brief analysis summary"
}

Respond ONLY with the JSON, no additional text."""
    
    async def process(self, topic: str) -> AgentResponse:
        """Processes the topic and generates pros and cons analysis."""
        try:
            # Validate input
            if not self._validate_input(topic):
                return AgentResponse(
                    success=False,
                    data={},
                    message="Topic cannot be empty"
                )
            
            # Validate topic length
            validation_result = validate_topic_length(topic)
            if not validation_result["valid"]:
                return AgentResponse(
                    success=False,
                    data={},
                    message=validation_result["message"]
                )
            
            # Build user prompt
            user_prompt = f"Analyze the following topic: {topic}"
            
            # Generate LLM response
            llm_response = await self.llm_provider.generate_response(
                prompt=user_prompt,
                system_prompt=self.system_prompt
            )
            
            # Parse JSON response
            try:
                analysis_data = json.loads(llm_response.content)
            except json.JSONDecodeError:
                logger.error(f"Error parsing JSON response: {llm_response.content}")
                return AgentResponse(
                    success=False,
                    data={},
                    message="Error processing model response"
                )
            
            # Validate response structure
            if not self._validate_analysis_structure(analysis_data):
                return AgentResponse(
                    success=False,
                    data={},
                    message="Invalid response structure"
                )
            
            return AgentResponse(
                success=True,
                data=analysis_data,
                message="Analysis completed successfully",
                metadata={
                    "model_used": llm_response.model,
                    "tokens_used": llm_response.usage.get("total_tokens", 0),
                    "provider": self.llm_provider.get_model_info()["provider"]
                }
            )
            
        except Exception as e:
            logger.error(f"Error in ClarityAgent.process: {str(e)}")
            return AgentResponse(
                success=False,
                data={},
                message=f"Internal error: {str(e)}"
            )
    
    def _validate_analysis_structure(self, data: Dict[str, Any]) -> bool:
        """Validates that the response has the correct structure."""
        required_keys = ["topic", "analysis", "summary"]
        if not all(key in data for key in required_keys):
            return False
        
        analysis = data.get("analysis", {})
        if not isinstance(analysis.get("pros"), list) or not isinstance(analysis.get("cons"), list):
            return False
        
        return len(analysis["pros"]) > 0 and len(analysis["cons"]) > 0
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Returns information about the clarity agent."""
        return {
            "name": "ClarityAgent",
            "description": "Analyzes topics and provides balanced pros and cons",
            "version": "1.0.0",
            "llm_provider": self.llm_provider.get_model_info(),
            "capabilities": [
                "Critical topic analysis",
                "Pros and cons generation",
                "Balanced thinking"
            ]
        }
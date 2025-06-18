from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Literal
from config.settings import settings
from agent.clarity_agents import ClarityAgent
from llm.platforms.openai import OpenAIProvider
from llm.platforms.anthropic import AnthropicProvider
from utils.logger import logger
from typing import Optional, Literal



# Input and output models
class AnalysisRequest(BaseModel):
    topic: str
    llm_provider: Optional[Literal["openai", "anthropic"]] = None


class AnalysisResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    message: str
    metadata: Dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    version: str
    available_providers: list


# FastAPI instance
app = FastAPI(
    title="Clarity Agent",
    description="API for clarity analysis of topics with pros and cons",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Factory to create LLM providers
def create_llm_provider(provider_name: Optional[Literal["openai", "anthropic"]] = None):
    """Factory to create LLM provider instances."""
    provider = provider_name or settings.default_llm_provider
    
    try:
        if provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            return OpenAIProvider(settings.openai_api_key, settings.openai_model)
        
        elif provider == "anthropic":
            if not settings.anthropic_api_key:
                raise ValueError("Anthropic API key not configured")
            return AnthropicProvider(settings.anthropic_api_key, settings.anthropic_model)
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    except Exception as e:
        logger.error(f"Error creating LLM provider {provider}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error configuring provider {provider}")


# Dependency to create agent
def get_clarity_agent(provider: Optional[Literal["openai", "anthropic"]] = None) -> ClarityAgent:
    """Dependency that creates a clarity agent instance."""
    llm_provider = create_llm_provider(provider)
    return ClarityAgent(llm_provider)


# Endpoints
@app.get("/", response_model=HealthResponse)
async def health_check():
    """API health check endpoint."""
    available_providers = []
    
    if settings.openai_api_key:
        available_providers.append("openai")
    if settings.anthropic_api_key:
        available_providers.append("anthropic")
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        available_providers=available_providers
    )


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_topic(request: AnalysisRequest):
    """Main endpoint to analyze a topic."""
    try:
        logger.info(f"Analyzing topic: {request.topic[:50]}...")
        
        # Create agent with specified provider
        agent = get_clarity_agent(request.llm_provider)
        
        # Process the topic
        result = await agent.process(request.topic)
        
        logger.info(f"Analysis completed. Success: {result.success}")
        
        return AnalysisResponse(
            success=result.success,
            data=result.data,
            message=result.message,
            metadata=result.metadata
        )
    
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agent/info")
async def get_agent_info(provider: Optional[Literal["openai", "anthropic"]] = None):
    """Gets information about the agent and current LLM provider."""
    try:
        agent = get_clarity_agent(provider)
        return agent.get_agent_info()
    
    except Exception as e:
        logger.error(f"Error getting agent info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/providers")
async def list_providers():
    """Lists available LLM providers."""
    providers = []
    
    if settings.openai_api_key:
        providers.append({
            "name": "openai",
            "model": settings.openai_model,
            "status": "available"
        })
    
    if settings.anthropic_api_key:
        providers.append({
            "name": "anthropic",
            "model": settings.anthropic_model,
            "status": "available"
        })
    
    return {"providers": providers}


# Global error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled error: {str(exc)}")
    return HTTPException(status_code=500, detail="Internal server error")
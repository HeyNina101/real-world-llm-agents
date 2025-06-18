import uvicorn
from api.api import app
from config.settings import settings
from utils.logger import logger


def main():
    """Main function to start the server."""
    logger.info("Starting Clarity Agent...")
    logger.info(f"Configuration: Host={settings.host}, Port={settings.port}")
    logger.info(f"Default provider: {settings.default_llm_provider}")
    
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info"
    )


if __name__ == "__main__":
    main()

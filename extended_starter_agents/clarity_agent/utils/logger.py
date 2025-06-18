from loguru import logger
import sys
from config.settings import settings

# Configure the logger
logger.remove()  # Remove default handler

# Configure custom format
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# Add console handler
logger.add(
    sys.stdout,
    format=log_format,
    level="DEBUG" if settings.debug else "INFO",
    colorize=True
)

# Add file handler (optional)
logger.add(
    "logs/clarity_agent.log",
    format=log_format,
    level="DEBUG",
    rotation="10 MB",
    retention="1 week",
    compression="zip"
)

# Export configured logger
__all__ = ["logger"]